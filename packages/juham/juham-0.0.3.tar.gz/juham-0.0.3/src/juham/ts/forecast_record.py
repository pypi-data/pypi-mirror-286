import json
from juham.base import Base
from influxdb_client_3 import Point


class ForecastRecord(Base):
    """Forecast database record.

    This class listens the forecast topic and writes to the time series
    database.
    """

    _class_id = ""

    def __init__(self, name="forecastrecord"):
        """Construct forecast record object with the given name."""

        super().__init__(name)

    def on_connect(self, client, userdata, flags, rc):
        """Standard mqtt connect notification.

        This method is called when the client connection with the MQTT
        broker is established.
        """
        super().on_connect(client, userdata, flags, rc)
        self.subscribe(Base.mqtt_root_topic + "/forecast")
        self.debug(f"Subscribed to {Base.mqtt_root_topic}/forecast")

    def on_message(self, client, userdata, msg):
        """Standard mqtt message notification method.

        This method is called upon new arrived message.
        """

        m = json.loads(msg.payload.decode())
        for h in m:
            ts = h["ts"]
            temperature = h["temperature"]
            wind_speed = h["windspeed"]
            solarenergy = h["solarenergy"]

            try:
                point = (
                    Point("forecast")
                    .field("wind_speed", wind_speed)
                    .field("temperature", temperature)
                    .field("solarenergy", solarenergy)
                    .time(self.epoc2utc(ts))
                )
                self.write(point)

            except Exception as e:
                self.error("Cannot write forecast time series", str(e))

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Base.register()
            cls.initialize_class()
