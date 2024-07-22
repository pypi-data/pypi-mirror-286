from juham.base import JDatabase
from influxdb_client_3 import InfluxDBClient3, Point


class JInflux(JDatabase):
    """Influx time series database version 3."""

    _class_id = None

    def __init__(self, name: str = "influx"):
        """Construct InfluxDB v3 client for writing and reading time series.

        Args:
            name (str, optional): Name of the object to be created. Defaults to "influx".
        """
        super().__init__(name)
        self.influx_client = InfluxDBClient3(
            host=JDatabase.host,
            token=JDatabase.token,
            org=JDatabase.org,
            database=JDatabase.database,
        )

    def write(self, point: Point) -> None:
        self.influx_client.write(record=point)

    @classmethod
    def register(cls) -> None:
        if cls.initialize_class():
            JDatabase.register()
