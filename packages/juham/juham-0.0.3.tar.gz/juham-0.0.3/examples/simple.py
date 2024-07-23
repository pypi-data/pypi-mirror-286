from juham.base import Base
from juham.app import JApp
from juham.mqtt import JPaho2
from juham.database import JConsole


def main():

    # Use 'JConsole' as replacement for time series database, for minimal dependencies
    Base.database_class_id = JConsole.get_class_id()
    # You want to create Influx account (v3) and replace JConsole with JInflux
    # Base.database_class_id = JInflux.get_class_id()
    # JInflux.token = 'your token'
    # JInflux.org = 'your organization'
    # JInflux.host = 'Url to your influx site'
    # JInflux.database='database name'
    # Base.database_class_id = JInflux.get_class_id()

    # Configure mqtt network
    JPaho2.host = "localhost"
    JPaho2.port = 1883
    Base.mqtt_class_id = JPaho2.get_class_id()

    simple = JApp("simple")

    # start
    simple.run()


if __name__ == "__main__":
    main()
