import json
from typing import Any
from juham.base import Base, MqttMsg

# TODO: rewrite and implement heat sensors to publish boiler temperatures
# in device independent format and more


class RPowerPlan(Base):
    """Automation class for optimized control of home energy consumers e.g hot
    water boilers. Reads spot prices, boiler water temperatures and controls
    heating radiators.

    """

    _class_id = ""
    topic_spot = Base.mqtt_root_topic + "/spot"
    topic_forecast = Base.mqtt_root_topic + "/forecast"
    topic_temperature = Base.mqtt_root_topic + "/temperature/102"
    topic_powerplan = Base.mqtt_root_topic + "/powerplan"
    topic_power = Base.mqtt_root_topic + "/power"
    topic_in_powerconsumption = Base.mqtt_root_topic + "/powerconsumption"
    uoi_limit = 0.75
    maximum_boiler_temperature = 70
    minimum_boiler_temperature = 45

    def __init__(self, name="rpowerplan"):
        super().__init__(name)
        self.main_boiler_temperature = 100
        self.pre_boiler_temperature = 0
        self.current_heating_plan = 0
        self.heating_plan = None
        self.power_plan = None
        self.ranked_spot_prices = None
        self.ranked_solarpower = None
        self.relay = 0
        self.relay_started = 0
        self.current_power = 0

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_spot)
            self.subscribe(self.topic_forecast)
            self.subscribe(self.topic_temperature)
            self.subscribe(self.topic_in_powerconsumption)

    def sort_by_rank(self, hours: list, ts_utc_now: float) -> list:
        """Sort the given electricity prices by their rank value. Given a list
        of electricity prices, return a sorted list from the cheapest to the
        most expensive hours. Entries that represent electricity prices in the
        past are excluded.

        Args:
            hours (list): list of hourly electricity prices
            ts_utc_now (float): current time

        Returns:
            list: sorted list of electricity prices
        """
        sh = sorted(hours, key=lambda x: x["Rank"])
        ranked_hours = []
        for h in sh:
            utc_ts = h["Timestamp"]
            if utc_ts > ts_utc_now:
                ranked_hours.append(h)

        return ranked_hours

    def sort_by_power(self, solarpower: list, ts_utc_now: float) -> list:
        """Sort forecast of solarpower to decreasing order.

        Args:
            solarpower (list): list of entries describing hourly solar energy forecast
            ts_utc_now (float): curren time, for exluding entries that are in the past

        Returns:
            list: list from the highest solarenergy to lowest.
        """
        self.debug(
            f"Sorting {len(solarpower)} days of forecast starting at {self.timestampstr(ts_utc_now)}"
        )
        sh = sorted(solarpower, key=lambda x: x["solarenergy"], reverse=True)
        self.debug(f"Sorted {len(sh)} days of forecast")
        ranked_hours = []
        for h in sh:
            utc_ts: float = float(h["ts"])
            if utc_ts > ts_utc_now:
                ranked_hours.append(h)
        self.debug(f"Forecast sorted for the next {str(len(ranked_hours))} days")
        return ranked_hours

    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        m = None
        ts_utc_now = self.timestamp()
        if msg.topic == self.topic_spot:
            self.ranked_spot_prices = self.sort_by_rank(
                json.loads(msg.payload.decode()), ts_utc_now
            )
            self.info(
                f"Spot prices received and ranked for {len(self.ranked_spot_prices)} hours"
            )
            self.power_plan = None  # reset power plan, it depends on spot prices
            return
        elif msg.topic == self.topic_forecast:
            self.ranked_solarpower = self.sort_by_power(
                json.loads(msg.payload.decode()), ts_utc_now
            )
            self.info(
                f"Solar energy forecast received and ranked for {len(self.ranked_solarpower)} hours"
            )
            self.power_plan = None  # reset power plan, it depends on forecast
            return
        elif msg.topic == self.topic_temperature:
            m = json.loads(msg.payload.decode())
            self.main_boiler_temperature = m["temperature"]
            self.info(
                f"Boiler temperature reading { self.main_boiler_temperature}C received"
            )
        elif msg.topic == self.topic_in_powerconsumption:
            m = json.loads(msg.payload.decode())
            self.current_power = m["real_total"]
            self.debug(f"Current power {self.current_power/1000.0} kW")
        else:
            super().on_message(client, userdata, msg)
            return
        self.on_powerplan(ts_utc_now)

    def on_powerplan(self, ts_utc_now: float) -> None:
        """Apply power plan.

        Args:
            ts_utc_now (float): utc time
        """
        if self.ranked_solarpower is None:
            self.debug("waiting forecast ...", "")
            return

        if self.ranked_spot_prices is None:
            self.debug("Waiting  spot prices...", "")
            return

        if self.power_plan is None:
            self.power_plan = self.create_power_plan()
            self.heating_plan = None
            self.info(
                f"Power plan of length {len(self.power_plan)} created",
                str(self.power_plan),
            )

        if self.power_plan is None:
            self.error("Failed to create a power plan", "")
            return

        if len(self.power_plan) < 4:
            self.warning(
                f"Suspiciously short {len(self.power_plan)}  power plan, wait more data ..",
                "",
            )
            self.heating_plan = None
            self.power_plan = None
            return

        if self.ranked_solarpower is None or len(self.ranked_solarpower) < 4:
            self.warning("No forecast, optimization compromized..", "")

        if self.heating_plan is None:
            self.heating_plan = self.create_heating_plan()
            self.info(f"Heating plan of length {len(self.heating_plan)} created", "")
        if self.heating_plan is None:
            self.error("Failed to create heating plan")
            return
        if len(self.heating_plan) < 4:
            self.info("Ditch remaining short heating plan ..", "")
            self.heating_plan = None
            self.power_plan = None
            return

        if ts_utc_now - self.relay_started < 10:
            self.info(
                f"Suspend relay update, started just {int(ts_utc_now - self.relay_started)} s ago"
            )
            return
        self.relay_started = ts_utc_now
        relay = self.consider_heating(ts_utc_now)
        heat = {"Unit": "main_boiler", "Timestamp": ts_utc_now, "State": relay}
        self.publish(self.topic_power, json.dumps(heat), 1, True)
        self.info(f"Heating state published with relay state {relay}", "")

    def consider_heating(self, ts: float) -> int:
        """Consider whether the target boiler needs heating.

        Args:
            ts (float): current UTC time

        Returns:
            int: 1 if heating is needed, 0 if not
        """
        if self.main_boiler_temperature < 45.0:
            self.info(
                f"Low temp, force heating because {self.main_boiler_temperature} is less than {self.minimum_boiler_temperature}"
            )
            return 1

        if self.main_boiler_temperature > self.maximum_boiler_temperature:
            self.info(
                f"Temperature beyond maximum already {self.main_boiler_temperature}"
            )
            return 0

        # Check if heating plan has FOM > 0
        if self.heating_plan[0]["FOM"] > self.uoi_limit:
            self.info(
                f"Best UOI is {self.heating_plan[0]['FOM']}, good enough to proceed..."
            )
            for p in self.heating_plan:
                if ts > float(p["Timestamp"]) and ts < float(p["Timestamp"]) + 3600:
                    if float(p["FOM"]) > 1.5:
                        self.info(
                            f"Cheap electricity at {self.timestampstr(p['Timestamp'])} UOI > {p['FOM']}"
                        )
                        return 1

            # sorted by price, sheapest hours at the head
            tplan = self.heating_plan[0:4]
            plan = sorted(tplan, key=lambda x: x["Timestamp"])
            ts_utc_start = plan[0]["Timestamp"]
            ts_utc_stop = plan[-1]["Timestamp"]

            if ts > ts_utc_stop:
                self.error(
                    f"Run out of heating plan { self.timestampstr(ts_utc_start)}  ...  {self.timestampstr(ts_utc_stop)}"
                )
                self.heating_plan = None
                self.power_plan = None
                return 0

            if ts < ts_utc_start:
                self.info(f"Heating will start at {self.timestampstr(ts_utc_start)}")
                return 0

            # check the current plan slot and if FOM > 1 then yes
            for p in plan:
                if ts > p["Timestamp"] and ts < ts > p["Timestamp"] + 3600:
                    if p["FOM"] > self.uoi_limit:
                        self.info(
                            f"Heat {self.timestampstr(p['Timestamp'])} because UOI > {p['FOM']}"
                        )
                        return 1
                    else:
                        self.info(
                            f"No heating: {self.timestampstr(p['Timestamp'])}, because UOI > {p['FOM']}"
                        )
                        return 0
        else:
            self.info(
                f"Expensive hours, no heating as UOI < {self.uoi_limit}",
                self.heating_plan,
            )
            return 0
        return 0

    # compute figure of merit (FOM) for each hour
    # the higher the solarenergy and the lower the spot the higher the FOM

    # compute fom
    def compute_fom(self, solpower: float, spot: float) -> float:
        """Compute UOI - utilization optimization index.

        Args:
            solpower (float): current solar power forecast
            spot (float): spot price

        Returns:
            float: utilization optimization index
        """
        # total solar power is 6kW and max pow consumption about twice as much
        # so when sun is shining with full power nearly half of the energy comes for free

        if spot < 0.001:
            return 2  # use
        elif spot > 0.1:
            return 0  # try not to use
        else:
            fom = 2 * (0.101 - spot) / 0.1
            return fom

    def create_power_plan(self) -> list:
        """Create power plan.

        Returns:
            list: list of utilization entries
        """
        ts_now = self.timestamp()
        self.info(
            f"Creating new powerplan from {len(self.ranked_spot_prices)}  hourly spot prices",
            "",
        )

        # syncronize spot and solarenergy by timestamp
        spots = []
        for s in self.ranked_spot_prices:
            if s["Timestamp"] > ts_now:
                spots.append(
                    {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
                )
        self.info(
            f"Have spot prices for the next {len(spots)} hours",
            "",
        )
        powers = []
        self.debug(f"Current time is : {self.timestampstr(ts_now)}")
        for s in self.ranked_solarpower:
            if s["ts"] > ts_now:
                powers.append({"Timestamp": s["ts"], "Solarenergy": s["solarenergy"]})
            else:
                self.debug(
                    f"Skipped past solar forecast hour {self.timestampstr(s['ts'])}"
                )

        self.info(
            f"Have solar forecast  for the next {len(powers)} hours",
            "",
        )
        hplan = []
        for spot, solar in zip(spots, powers):
            # maximum FOM is if spot is negative
            solarenergy = solar["Solarenergy"]
            spotprice = spot["PriceWithTax"]
            fom = self.compute_fom(solarenergy, spotprice)
            plan = {"Timestamp": spot["Timestamp"], "FOM": fom}
            hplan.append(plan)

        shplan = sorted(hplan, key=lambda x: x["FOM"], reverse=True)

        self.info(f"Powerplan of {len(shplan)} hours created", str(shplan))
        return shplan

    def create_heating_plan(self) -> list:
        """Create heating plan.

        Returns:
            int: list of heating entries
        """
        self.info("Creating heating plan", "")
        state = 0
        heating_plan = []

        hours = 0
        needed_hours = 5

        for hp in self.power_plan:
            fom = hp["FOM"]
            if float(fom) >= self.uoi_limit and hours < needed_hours:
                state = 1
            else:
                state = 0
            heat = {
                "Unit": "main_boiler",
                "Timestamp": hp["Timestamp"],
                "State": state,
                "FOM": fom,
                "UOI": fom,
            }
            self.publish(self.topic_powerplan, json.dumps(heat), 1, True)
            heating_plan.append(hp)
            hours = hours + 1

        self.info(
            "Heating plan published starting "
            + self.timestampstr(heating_plan[0]["Timestamp"]),
            "",
        )
        return heating_plan

    @classmethod
    def register(cls) -> None:
        if cls._class_id == "":
            Base.register()
            cls.initialize_class()
            cls.register_topic(Base.mqtt_root_topic + "/powerplan")
            cls.register_topic(Base.mqtt_root_topic + "/power")
