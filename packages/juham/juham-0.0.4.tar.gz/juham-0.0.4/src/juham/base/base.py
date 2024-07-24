import json
from datetime import datetime, timezone
from typing import Any
from paho.mqtt.client import MQTTMessage as MqttMsg
from .object import Object


class Base(Object):
    """An automation object with MQTT networking, data storage,
    logging and factory method pattern capabilities.

    Example:
    ::

        obj = Base("foo")
        obj.mqtt_host = "myhost.com"
        obj.mqtt_port = 12345
        obj.subscribe('foo/bar')
        obj.run()


    To configure Base class to use a specific MQTT and time series implementations set
    the class attributes to refer to desired MQTT and time series database implementations.
    When instantiated the object will instantiate the given MQTT and database objects with it.

    """

    database_class_id: str = ""
    mqtt_class_id: str = ""
    write_attempts = 3
    mqtt_root_topic: str = "juham"
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    _class_id: str = ""
    _valid_topics: set = set()

    def __init__(self, name: str = "") -> None:
        """Constructs new automation object with the given name, configured
        time series recorder and MQTT network features.

        Args:
            name (str): name of the object
        """
        super().__init__(name)
        self.database_client: object = None
        self.init_database(name)
        self.init_mqtt(name)
        self.debug(name + " instantiated")

    # @override
    def to_dict(self):
        data = super().to_dict()
        data["_base"] = {}
        attributes = ["mqtt_host", "mqtt_port", "mqtt_root_topic", "write_attempts"]
        for attr in attributes:
            if getattr(self, attr) != getattr(type(self), attr):
                data["_base"][attr] = getattr(self, attr)
        if self.database_client is not None:
            data["_database"] = {"db_client": self.database_client.to_dict()}
        return data

    # @override
    def from_dict(self, data):
        super().from_dict(data)
        for key, value in data["_base"].items():
            if key == "db_client":
                self.database_client = Object.instantiate(value["_class"])
                self.database_client.from_dict(value)
            else:
                setattr(self, key, value)

    def init_database(self, name: str) -> None:
        """Instantiates the configured time series database object.

        Issues a warning if the :attr:`~database_class_id` has not
        been configured, in which case the object will not have the time series
        recording feature.

        This method is called internally and typically there is no need to call it
        from the application code.
        """

        if Base.database_class_id != 0 and Object.find_class(Base.database_class_id):
            self.database_client = Object.instantiate(Base.database_class_id)
        else:
            self.warning("Suscpicious configuration: no database_class_id set")

    def init_mqtt(self, name: str) -> None:
        """Instantiates the configured MQTT object for networking.

        This method is called internally and typically there is no need to call it
        from the application code.

        Issues a warning if the :attr:`~pubsub_class_id` has not
        been configured, even though objects without a capability to communicate
        are rather crippled.
        """
        if Base.mqtt_class_id is not None and Base.find_class(Base.mqtt_class_id):
            self.mqtt_client = Object.instantiate_with_param(Base.mqtt_class_id, name)
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_disconnect = self.on_disconnect
            if self.mqtt_client.connect_to_server(self.mqtt_host, self.mqtt_port) != 0:
                self.error(
                    f"Couldn't connect to the mqtt broker at {self.mqtt_client.host}"
                )
            else:
                self.debug(
                    f"{self.name} with mqtt broker {self.mqtt_client.name} connected to {self.mqtt_client.host}"
                )
        else:
            self.warning("Suscpicious configuration: no mqtt_class_id set")

    def subscribe(self, topic: str) -> None:
        """Subscribe to the given MQTT topic.

        This method sets up the subscription to the specified MQTT topic and registers
        the :meth:`on_message` method as the callback for incoming messages.

        Args:
            topic (str): The MQTT topic to subscribe to.

        Example:
        ::

            # configure
            obj.subscribe('foo/bar')
        """
        if self.valid_topic(topic):
            self.mqtt_client.connected_flag = True
            self.mqtt_client.subscribe(topic)
            self.info(f"{self.name}  subscribed to { topic}")
        else:
            raise ValueError(
                f"Subscription to invalid topic {topic} by object {self.name}"
            )

    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        """MQTT message notification on arrived message.

        Called whenever a new message is posted on one of the
        topics the object has subscribed to via subscribe() method.
        This method is the heart of automation: here, derived subclasses should
        automate whatever they were designed to automate. For example, they could switch a
        relay when a boiler temperature sensor signals that the temperature is too low for
        a comforting shower for say one's lovely wife.

        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            msg (object): The MQTT message
        """

        if msg.topic == self.mqtt_root_topic + "/control":
            m = json.loads(msg.payload)
            if m["command"] == "shutdown":
                self.mqtt_client.disconnect()
                self.mqtt_client.loop_stop()

    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        """Notification on connect.

        This method is called whenever the MQTT broker is connected.
        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            flags (int): Consult MQTT
            rc (int): See MQTT docs
        """
        self.mqtt_client.subscribe(self.mqtt_root_topic + "/control")
        self.debug(self.name + " connected to the mqtt broker ")

    def on_disconnect(self, client, userdata, rc=0):
        """Notification on disconnect.

        This method is called whenever the MQTT broker is disconnected.
        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            rc (int): See MQTT docs
        """
        self._log.debug(self.name + " disconnected from the mqtt broker ")
        # client.loop_stop()

    def epoc2utc(self, epoch):
        """Converts the given epoch time to UTC time string. All time
        coordinates are represented in UTC time. This allows the time
        coordinate to be mapped to any local time representation without
        ambiguity.

        Args:
            epoch (float) : timestamp in UTC time
            rc (str): time string describing date, time and time zone e.g 2024-07-08T12:10:22Z

        Returns:
            UTC time
        """
        utc_time = datetime.fromtimestamp(epoch, timezone.utc)
        utc_timestr = utc_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        return utc_timestr

    def timestampstr(self, ts):
        """Converts the given timestamp to human readable string of form 'Y-m-d
        H:M:S'.

        Args:
            ts (timestamp):  time stamp to be converted

        Returns:
            rc (string):  human readable date-time string
        """
        return str(datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))

    def timestamp(self):
        """Returns the current date-time in UTC.

        Returns:
            rc (datetime):  datetime in UTC.
        """
        return datetime.now(timezone.utc).timestamp()

    def is_time_between(self, begin_time, end_time, check_time=None):
        """Check if the given time is within the given time line. All
        timestamps must be in UTC time.

        Args:
            begin_time (timestamp):  beginning of the timeline
            end_time (timestamp):  end of the timeline
            check_time (timestamp):  time to be checked

        Returns:
            rc (bool):  True if within the timeline
        """

        check_time = check_time or datetime.utcnow().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else:  # crosses midnight
            return check_time >= begin_time or check_time <= end_time

    def write(self, point):
        """Writes the given measurement to the database. In case of an error,
        it tries again until the maximum number of attempts is reached.  If it
        is still unsuccessful, it gives up and passes the first encountered
        exception to the caller.

        Args:
            point: a measurement describing a time stamp and related attributes for one measurement.
        """
        first_exception = None
        for i in range(self.write_attempts):
            try:
                self.database_client.write(point)
                return
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                self.warning(f"Writing ts failed, attempt {str(i+1)}", str(e))

        self.log_message(
            "Error",
            f"Writing failed after {str(self.write_attempts)} attempts, giving up",
            str(first_exception),
        )
        raise first_exception

    def read(self, point):
        """Reads the given measurement from the database.

        Args:
            point: point with initialized time stamp.

        ... note: NOT IMPLEMENTED YET
        """
        self.database_client.read(point)

    # @override
    def debug(self, msg, details=""):
        """Logs the given debug message to the database after logging it using
        the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().debug(msg, details)
        self.log_message("Debug", msg, details="")

    # @override
    def info(self, msg: str, details: str = ""):
        """Logs the given information message to the database after logging it
        using the BaseClass's info() method.

        Args:
            msg : The information message to be logged.
            details : Additional detailed information for the message to be logged

        Example:
        ::

            obj = new Base('test')
            obj.info('Message arrived', str(msg))
        """
        super().info(msg, details)
        self.log_message("Info", msg, details="")

    # @override
    def warning(self, msg, details=""):
        """Logs the given warning message to the database after logging it
        using the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().warning(msg, details)
        self.log_message("Warn", msg, details)

    # @override
    def error(self, msg, details=""):
        """Logs the given error message to the database after logging it using
        the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().error(msg, details)
        self.log_message("Error", msg, details)

    def log_message(self, type, msg, details=""):
        """Publish the given log message to the MQTT 'log' topic.

        This method constructs a log message with a timestamp, class type, source name,
        message, and optional details. It then publishes this message to the 'log' topic
        using the MQTT protocol.

        Parameters:
            type : str
                The classification or type of the log message (e.g., 'Error', 'Info').
            msg : str
                The main log message to be published.
            details : str, optional
                Additional details about the log message (default is an empty string).

        Returns:
            None

        Raises:
            Exception
                If there is an issue with the MQTT client while publishing the message.

        Example:
        ::

            # publish info message to the Juham's 'log' topic
            self.log_message("Info", f"Some cool message {some_stuff}", str(dict))
        """

        try:
            msg = {
                "Timestamp": self.timestamp(),
                "Class": type,
                "Source": self.name,
                "Msg": msg,
                "Details": str(details),
            }
            self.publish(Base.mqtt_root_topic + "/log", json.dumps(msg), 1)
        except Exception as e:
            if self._log is not None:
                self._log.error(f"Publishing log event failed {str(e)}")

    def publish(self, topic: str, msg: str, qos: int = 1, retain: bool = True):
        """Publish the given message to the given MQTT topic.
        For more information consult MQTT.

        Args:
            topic (str): topic
            msg (str): message to be published
            qos (int, optional): quality of service. Defaults to 1.
            retain (bool, optional): retain. Defaults to True.
        """

        if self.valid_topic(topic):
            self.mqtt_client.publish(topic, msg, qos, retain)
            super().debug(f"Message published to valid topic: {topic}")
        else:
            raise ValueError(f"Publish to invalid topic {topic} by object {self.name}")

    def valid_topic(self, topic: str) -> bool:
        """Check if the given topic has been registered as valid topic.

        Args:
            topic (str): topic to be validated

        Returns:
            bool: true if known topic.
        """
        return topic in self._valid_topics

    @classmethod
    def register_topic(cls, topic: str):
        """Register the given topic as known valid topic. Publishing and subscriptions are allowed only to registered
        topics. Each topic must have an owner, who is responsible for registering the topic.

        Args:
            topic (str): valid topic
        """
        cls._valid_topics.add(topic)

    def shutdown(self):
        """Shut down all services, free resources, stop threads, disconnect
        from mqtt, in general, prepare for shutdown."""
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def run(self):
        """Start a new thread to runs the network loop in the background.

        Allows the main program to continue executing while the MQTT
        client handles incoming and outgoing messages in the background.
        """
        self.mqtt_client.loop_start()

    def run_forever(self):
        """Starts the network loop and blocks the main thread, continuously
        running the loop to process MQTT messages.

        The loop will run indefinitely unless the connection is lost or
        the program is terminated.
        """
        self.mqtt_client.loop_forever()

    @classmethod
    def register(cls) -> None:
        if cls._class_id == "":
            # register super class and other dependencies
            Object.register()
            cls.initialize_class()
            cls.register_topic(cls.mqtt_root_topic + "/control")
            cls.register_topic(cls.mqtt_root_topic + "/log")
