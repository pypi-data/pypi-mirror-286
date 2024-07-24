from juham.base import Base
import json


class WaterCirculator(Base):
    """Hot Water Circulation Controller.

    Uses motion sensor data to determine if someone is at home. If so,
    it runs the water circulator pump to ensure that hot water is
    instantly available when the tap is turned on.
    """

    _class_id = ""
    uptime = 60 * 5
    min_temperature = 37
    relay_topic = "shellyplus1-a0a3b3c309c4/command/switch:0"
    temperature_topic = Base.mqtt_root_topic + "/temperature/103"
    motion_sensor_topic = "shellies/shellymotion2/info"
    motion_topics = "shellies/shellymotion2/#"

    def __init__(self, name="rwatercirculator"):
        super().__init__(name)
        self.current_motion = 0
        self.relay_started_ts = 0
        self.water_temperature = 0
        self.water_temperature_updated = 0

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.motion_topics)
            self.subscribe(self.temperature_topic)

    def on_message(self, client, userdata, msg):
        if msg.topic == self.temperature_topic:
            m = json.loads(msg.payload.decode())
            self.on_temperature_sensor(m, self.timestamp())
        elif msg.topic == self.motion_sensor_topic:
            m = json.loads(msg.payload.decode())
            self.on_motion_sensor(m, self.timestamp())
        else:
            super().on_message(client, userdata, msg)

    def on_temperature_sensor(self, m: dict, ts_utc_now: float) -> None:
        """Handle message from the hot water pipe temperature sensor.

        Records the temperature and updates the water_temperature_updated attribute.

        Args:
            m (dict): temperature reading from the hot water blump sensor
            ts_utc_now (float): _current utc time
        """

        self.water_temperature = m["temperature"]
        self.water_temperature_updated = ts_utc_now
        self.debug(
            f"Temperature of circulating water updated to {self.water_temperature} C"
        )

    def on_motion_sensor(self, m: dict, ts_utc_now: float) -> None:
        """Control the water cirulator bump.

        Given message from the motion sensor consider switching the
        circulator bump on.

        Args:
            msg (dict): directionary holding motion sensor data
            ts_utc_now (float): current time stamp
        """
        sensor = m["sensor"]
        vibration = sensor["vibration"]
        motion = sensor["motion"]

        if motion == True:
            if not self.current_motion:
                temp_check_ok = False
                if ts_utc_now - self.water_temperature_updated < 15 * 60:
                    temp_check_ok = True
                if (
                    self.water_temperature > self.min_temperature
                ) and temp_check_ok is True:
                    self.debug(
                        f"Motion detected but water is warm enough already {self.water_temperature} C"
                    )
                else:
                    self.current_motion = True
                    self.relay_started_ts = ts_utc_now
                    self.publish(self.relay_topic, "on", 1)
                    self.info(
                        f"Water circulator pump switched on for {int(self.uptime / 60)} minutes "
                    )
            else:
                self.debug(
                    f"Circulator pump has been running for {str(int(ts_utc_now - self.relay_started_ts)/60)} minutes",
                    " ",
                )
        else:
            if self.current_motion == True:
                if ts_utc_now - self.relay_started_ts > self.uptime:
                    self.publish(self.relay_topic, "off", 1)
                    self.info("Water circulator pump switched off", "")
                    self.current_motion = False
                else:
                    self.debug(
                        f"Pump shutdown countdown {str(int(self.uptime - (ts_utc_now - self.relay_started_ts ))/60)} min"
                    )
            else:
                self.debug(
                    f"Pump off already, temperature {self.water_temperature} C", ""
                )

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Base.register()
            cls.initialize_class()
            cls.register_topic(cls.relay_topic)
