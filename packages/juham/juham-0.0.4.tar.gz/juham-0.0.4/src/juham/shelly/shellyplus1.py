import json
from influxdb_client_3 import Point
from juham.base import Base
from juham.shelly.jshelly import JShelly


class ShellyPlus1(JShelly):
    """Shelly Plus 1 smart relay time series record.

    Listens MQTT messages from DS18B20 temperature sensors attached to
    Shelly 1 PM Add on module and writes them to time series database.
    """

    _class_id = ""
    shelly_topic = "/events/rpc"  # source topic
    temperature_topic = Base.mqtt_root_topic + "/temperature/"  # target topic

    def __init__(self, name="shellyplus1-a0a3b3c309c4"):
        super().__init__(name)
        self.relay_started = 0

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.mqtt_prefix + self.shelly_topic)

    def on_message(self, client, userdata, msg):
        # optimize out excessive notifications
        tsnow = self.timestamp()
        if tsnow - self.relay_started < 60:
            return 0
        self.relay_started = tsnow

        m = json.loads(msg.payload.decode())
        mth = m["method"]
        if mth == "NotifyStatus":
            params = m["params"]
            self.on_sensor(params)
        else:
            self.warning("Unknown method " + mth, str(m))

    def on_sensor(self, params: dict) -> None:
        """Map Shelly Plus 1 specific event to juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """
        ts = params["ts"]
        for key, value in params.items():
            if key.startswith("temperature:"):
                sensor_id = key.split(":")[1]
                temperature_reading = value
                # temperature_id = temperature_reading["id"]
                temperature_celsius = temperature_reading["tC"]

                msg = {
                    "sensor": sensor_id,
                    "timestamp": ts,
                    "temperature": int(temperature_celsius),
                }
                self.publish(
                    self.temperature_topic + sensor_id, json.dumps(msg), 1, True
                )
                self.debug(
                    f"Temperature reading { self.temperature_topic + sensor_id} published"
                )

                try:
                    point = (
                        Point("boiler")
                        .tag("sensor", sensor_id)
                        .field("s" + sensor_id, temperature_celsius)
                        .time(self.epoc2utc(ts))
                    )
                    self.write(point)
                    self.debug(
                        f"Temperature { str(sensor_id)}  { str(temperature_celsius)} recorded",
                        "",
                    )
                except Exception as e:
                    self.error(f"Writing to influx failed {str(e)}")

    def to_dict(self):
        data = super().to_dict()
        data["_shellyplus1"] = {
            "shelly_topic": self.shelly_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    def from_dict(self, data):
        super().from_dict(data)
        if "_shellyplus1" in data:
            for key, value in data["_shellyplus1"].items():
                setattr(self, key, value)

    @classmethod
    def register(cls):
        if cls._class_id == "":
            JShelly.register()
            cls.initialize_class()
            cls.register_topic(cls.temperature_topic)
            cls.register_topic(cls.temperature_topic + "100")
            cls.register_topic(cls.temperature_topic + "101")
            cls.register_topic(cls.temperature_topic + "102")
            cls.register_topic(cls.temperature_topic + "103")
            cls.register_topic(cls.temperature_topic + "104")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic + "/100")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic + "/101")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic + "/102")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic + "/103")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic + "/104")
            cls.register_topic("shellyplus1-a0a3b3c309c4" + cls.shelly_topic)
