import json
from influxdb_client_3 import Point

from juham.base import Base


class EnergyCostCalculator(Base):
    """Energy revenue/cost calculator for calculating energy balance between
    produced and consumed energy.

    Subscribes to spot and power MQTT topics, calculates per hour, per
    day, per month and per year costs and  writes them the it to the
    time series database.
    """

    _class_id = ""
    topic_in_spot = Base.mqtt_root_topic + "/spot"
    topic_in_powerconsumption = Base.mqtt_root_topic + "/powerconsumption"
    to_joule_coeff = 1.0 / (1000.0 * 3600)

    def __init__(self, name="ecc"):
        super().__init__(name)
        self.current_ts = 0
        self.current_cost = 0

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_in_spot)
            self.subscribe(self.topic_in_powerconsumption)

    def on_message(self, client, userdata, msg):
        """Handle MQTT message.

        Args:
            client (object) : client
            userdata (any): user data
            msg (object): mqtt message
        """
        ts_now = self.timestamp()

        m = json.loads(msg.payload.decode())
        if msg.topic == self.topic_in_spot:
            self.on_spot(m)
        elif msg.topic == self.topic_in_powerconsumption:
            self.on_powerconsumption(ts_now, m)
        else:
            self.error(f"Unknown event {msg.topic}")

    def on_spot(self, spot):
        """Stores the received per hour electricity prices to spots list.

        Args:
            spot (list): list of hourly spot prices
        """
        self.spots = []
        for s in spot:
            self.spots.append(
                {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
            )

    def map_prices_to_joules(self, price):
        """Convert the given electricity price in kWh to Watt seconds (J)
        Args:
            price (float): electricity price given as kWh
        Returns:
            Electricity price per watt second (J)
        """
        return price * self.to_joule_coeff

    def get_prices(self, ts_prev, ts_now):
        """Fetch the electricity prices for the given two subsequent time
        stamps.

        Args:
            ts_prev (timestamp): previous time
            ts_now (timestamp): current time
        Returns:
            Electricity prices for the given interval
        """
        prev_price = None
        current_price = None

        for i in range(0, len(self.spots) - 1):
            r0 = self.spots[i]
            r1 = self.spots[i + 1]
            ts0 = r0["Timestamp"]
            ts1 = r1["Timestamp"]
            if ts_prev >= ts0 and ts_prev <= ts1:
                prev_price = r0["PriceWithTax"]
            if ts_now >= ts0 and ts_now <= ts1:
                current_price = r0["PriceWithTax"]
            if prev_price is not None and current_price is not None:
                return prev_price, current_price
        self.error("PANIC: run out of spot prices")
        return 0.0, 0.0

    def calculate_net_energy_cost(self, ts_prev, ts_now, energy):
        """Given time interval as start and stop Calculate the cost over the
        given time period. Positive values indicate revenue, negative cost.

        Args:
            ts_prev (timestamp): beginning time stamp of the interval
            ts_now (timestamp): end of the interval
            energy (float): energy consumed during the time interval
        Returns:
            Cost or revenue
        """
        cost = 0
        prev = ts_prev
        while prev < ts_now:
            elapsed_seconds = ts_now - prev
            if elapsed_seconds > 3600:
                elapsed_seconds = 3600
            now = prev + elapsed_seconds
            start_per_kwh, stop_per_kwh = self.get_prices(prev, now)
            start_price = self.map_prices_to_joules(start_per_kwh)
            stop_price = self.map_prices_to_joules(stop_per_kwh)
            if abs(stop_price - start_price) < 1e-24:
                cost = cost + energy * elapsed_seconds * start_price
                self.debug(
                    f"Energy cost {str(cost)} e = {str(energy)} J x {str(start_price)} e/J x {str(elapsed_seconds)} s"
                )
            else:
                # calcualte cost over hour boundary
                ts_0 = (now // 3600.0) * 3600
                t1 = (ts_0 - prev) / (now - prev)
                t2 = (now - ts_0) / (now - prev)
                cost = (
                    cost
                    + energy
                    * ((1.0 - t1) * start_price + t2 * stop_price)
                    * elapsed_seconds
                )
                self.debug(
                    f"Cost over hour boundary {str(cost)} e = {str(energy)} J x {str(start_price)} e/J x {str(t1)} s + {str(stop_price)}e x {str(t2)} s"
                )
            prev = prev + elapsed_seconds
        return cost

    def on_powerconsumption(self, ts_now, m):
        """Update energy consumption.

        Args:
           ts_now (timestamp): time stamp of the energy consumed
           m (dictionary): Juham MQTT message holding energy reading
        """
        current_power = m["real_total"]
        if self.spots is None:
            self.info("Waiting for electricity prices...")
        elif self.current_ts == 0:
            self.current_ts = ts_now
            self.info("Energy cost calculator initialized")
        else:
            dp = self.calculate_net_energy_cost(self.current_ts, ts_now, current_power)
            self.current_cost = self.current_cost + dp
            self.current_ts = ts_now
            self.record_energycost(ts_now, self.name, self.current_cost)

    def record_energycost(self, ts_now, site, cost):
        """Record energy cost/revenue to data storage. Positive values represent
        revenue whereas negative cost.
        Args:
            ts_now (float): timestamp
            site ([type]): site
            cost ([type]): cost or revenue.
        """
        try:
            point = (
                Point("energycost")
                .tag("site", site)
                .field("cost", cost)
                .time(self.epoc2utc(ts_now))
            )
            self.write(point)

        except Exception as e:
            self.error(f"Cannot write energycost at{self.timestampstr(ts_now)}", str(e))

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Base.register()
            cls.initialize_class()
            cls.register_topic(Base.mqtt_root_topic + "/spot")
            cls.register_topic(Base.mqtt_root_topic + "/powerconsumption")
