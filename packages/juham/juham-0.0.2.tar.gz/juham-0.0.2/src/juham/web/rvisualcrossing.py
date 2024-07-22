from datetime import datetime, timedelta
import json
from typing import override
from influxdb_client_3 import Point
from juham.base import Base
from juham.web import RCloud, RCloudThread


class RVisualCrossingThread(RCloudThread):
    """Asynchronous thread for acquiring forecast from the VisualCrossing
    site."""

    _class_id = None
    forecast_topic = ""
    base_url = ""
    poll_interval: float = 60.0
    apiKey = ""
    location = ""
    interval: float = 60

    def __init__(self, client=None):
        """Construct with the given mqtt client. Acquires data from the visual
        crossing web service and publishes the forecast data to
        ```forecast_topic```.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client = client

    def update_interval(self) -> float:
        return self.interval

    @override
    def make_url(self) -> str:
        unit_group = "metric"
        now = datetime.now()
        end = now + timedelta(days=1)
        start_date = now.strftime("%Y-%m-%d")
        end_date = end.strftime("%Y-%m-%d")
        content_type = "json"
        include = "hours"
        api_query = self.base_url + self.location
        api_query += "/" + start_date
        api_query += "/" + end_date
        api_query += "?"
        api_query += "&unitGroup=" + unit_group
        api_query += "&contentType=" + content_type
        api_query += "&include=" + include
        api_query += "&key=" + self.apiKey
        return api_query

    def process_data(self, data):

        # TODO: replace deprecated datetime.utcfromtimestamp(ts) deprecated
        super().process_data(data)
        data = data.json()
        # tzoffset = data["tzoffset"]   obsolete
        forecast = []

        for day in data["days"]:
            for hour in day["hours"]:
                ts = int(hour["datetimeEpoch"])
                forecast.append(
                    {
                        "id": "weather",
                        "hour": datetime.utcfromtimestamp(ts).strftime("%H"),
                        "ts": ts,
                        "day": datetime.utcfromtimestamp(ts).strftime("%Y%m%d%H"),
                        "uvindex": hour["uvindex"],
                        "solarradiation": hour["solarradiation"],
                        "solarenergy": hour["solarenergy"],
                        "cloudcover": hour["cloudcover"],
                        "snow": hour["snow"],
                        "snowdepth": hour["snowdepth"],
                        "pressure": hour["pressure"],
                        "temperature": hour["temp"],
                        "humidity": hour["humidity"],
                        "windspeed": hour["windspeed"],
                        "winddir": hour["winddir"],
                        "dew": hour["dew"],
                    }
                )
        msg = json.dumps(forecast)
        self.mqtt_client.publish(self.forecast_topic, msg, qos=1, retain=True)
        self.info("Forecast published")

    @classmethod
    def register(cls):
        if cls._class_id is None:
            RCloudThread.register()
            RCloud.register_class(cls._class_id, cls)
            cls.initialize_class()


class RVisualCrossing(RCloud):
    """This class constructs a data acquisition object for reading weather
    forecasts from the VisualCrossing web service. It subscribes to the
    forecast topic and writes hourly data such as solar energy, temperature,
    and other attributes relevant to home automation into a time series
    database.

    Spawns an asynchronous thread to run queries at the specified
    update_interval.
    """

    _class_id = None
    workerThreadId = RVisualCrossingThread.get_class_id()
    forecast_topic = Base.mqtt_root_topic + "/forecast"
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    update_interval = 12 * 3600
    api_key = "[someapikey]"
    location = "lahti,finland"

    def __init__(self, name="visualcrossing"):
        super().__init__(name)

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.forecast_topic)

    def on_message(self, client, userdata, msg):
        if msg.topic == self.forecast_topic:
            em = json.loads(msg.payload.decode())
            self.on_forecast(em)
        else:
            super().on_message(client, userdata, msg)

    def on_forecast(self, em: dict) -> None:
        """Handle weather forecast data. Writes the received hourly forecast
        data to timeseries database.

        Args:
            em (dict): forecast
        """
        for m in em:
            point = (
                Point("forecast")
                .tag("hour", m["hour"])
                .field("hr", m["hour"])
                .field("ts", m["ts"])
                .field("solarradiation", m["solarradiation"])
                .field("solarenergy", m["solarenergy"])
                .field("cloudcover", m["cloudcover"])
                .field("snow", m["snowdepth"])
                .field("uvindex", m["uvindex"])
                .field("pressure", m["pressure"])
                .field("humidity", m["humidity"])
                .field("windspeed", m["windspeed"])
                .field("winddir", m["winddir"])
                .time(self.epoc2utc(m["ts"]))
            )
            self.write(point)

    def run(self):
        # create, initialize and start the asynchronous thread for acquiring forecast
        self.worker = Base.instantiate(RVisualCrossing.workerThreadId)
        self.worker.forecast_topic = self.forecast_topic
        self.worker.base_url = self.base_url
        self.worker.interval = self.update_interval
        self.worker.apiKey = self.api_key
        self.worker.location = self.location
        super().run()

    def to_dict(self):
        data = super().to_dict()
        data["_visualcrossing"] = {
            "topic": self.forecast_topic,
            "url": self.base_url,
            "api_key": self.api_key,
            "interval": self.update_interval,
        }
        return data

    def from_dict(self, data):
        super().from_dict(data)
        if "_visualcrossing" in data:
            for key, value in data["_visualcrossing"].items():
                setattr(self, key, value)

    @classmethod
    def register(cls):
        if cls._class_id is None:
            RCloud.register()
            RVisualCrossingThread.register()
            cls.initialize_class()
