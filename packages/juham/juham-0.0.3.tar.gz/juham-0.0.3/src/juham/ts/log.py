from juham.base import Base
from influxdb_client_3 import Point
import json


class LogRecord(Base):
    """Time series class for log events.

    Records all log events to time series database.
    """

    _class_id = ""

    def __init__(self, name="log_record"):
        """Creates mqtt client for recording log events to time series
        database.

        Args:
            name (str): name for the client
        """
        super().__init__(name)

    def on_connect(self, client, userdata, flags, rc):
        """Connects the client to mqtt broker.

        Args:
            client (obj): client to be connected
            userdata (any): caller specific data
            flags (int): implementation specific shit

        Returns:
            rc (bool): True if succesful
        """
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(Base.mqtt_root_topic + "/log")

    def on_message(self, client, userdata, msg):
        m = json.loads(msg.payload.decode())
        ts = self.epoc2utc(m["Timestamp"])

        point = (
            Point("log")
            .tag("class", m["Class"])
            .field("source", m["Source"])
            .field("msg", m["Msg"])
            .field("details", m["Details"])
            .field("Timestamp", m["Timestamp"])
            .time(ts)
        )
        try:
            self.write(point)
        except Exception as e:
            self.log_message("Error", f"Cannot write log event {m['Msg']}", str(e))

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Base.register()
            cls._class_id = cls.__name__
