from .object import Object


class JMqtt(Object):
    """Abstract base class for MQTT brokers."""

    _class_id = ""

    def __init__(self, name):
        super().__init__(name)

    def disconnect_from_server(self):
        """Disconnect from the MQTT broker.

        It is up to the sub classes to implement the method.
        """

    def connect_to_server(
        self, host: str = "localhost", port: int = 1883, keepalive: int = 60
    ):
        """Connect to MQTT server

        Args:
            host (str, optional): host. Defaults to "localhost".
            port (int, optional): port. Defaults to 1883.
            keepalive (int, optional): keep alive, in seconds. Defaults to 60.
        """

    def loop_stop(self):
        """Stop the network loop.

        No further messages shall be dispatched.
        """

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Object.register()
            cls.initialize_class()
