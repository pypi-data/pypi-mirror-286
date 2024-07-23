import json
from typing import List
from .base import Base, Object


class Group(Base):
    """Group base class that can consist of `Base` and `Group` objects as
    children.

    This class can be used for grouping home automation objects into larger logical entities.

    Example:
    ::

        motion_sensors = Group("motionsensors")
        motion_sensors.add(ShellyMotionSensor("downstairs"))
        motion_sensors.add(ShellyMotionSensor("upstairs"))
    """

    _class_id = ""

    def __init__(self, name: str = "group") -> None:
        super().__init__(name)
        self.children: List = []
        self.role: str = "union"

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.mqtt_client.connected_flag = True

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)
        m = json.loads(msg.payload.decode())
        self.warning(f"Message {str(m)} not handled")

    def run(self) -> None:
        """Start up all automation objects in the group and enter the network
        event loop to process MQTT messages.

        The method returns only when the process is terminated by some
        means e.g. Ctrl+C or kill, or by sending 'quit' event to MQTT
        message broker.
        """
        self.debug("Starting up mqtt clients...")
        for h in self.children:
            h.run()
        self.debug("Starting up control client, press CTRL+C to exit...")
        try:
            self.mqtt_client.loop_forever()
            self.info(f"Networking loop terminated, terminating children...")
        except:
            self.info(f"Networking loop terminated, terminating children...")
        for h in self.children:
            self.info(f"Terminating {h.name}")
            h.shutdown()

    def add(self, h: Object) -> None:
        """Add new automation object as children. The object to be inserted
        must be derived from Object base class.

        Args:
            h (Object): object to be inserted.
        """
        self.children.append(h)

    def to_dict(self):
        data = super().to_dict()
        data["_group"] = {
            "role": self.role,
            "children": [child.to_dict() for child in self.children],
        }
        return data

    def from_dict(self, data):
        """Recursively deserialize the group from a dictionary, including it
        children.

        Args:
            data (dict): data to deserialize from.

        Example:
        ::

            from juham.base import Group, Base

            # create a group with a child
            group = Group("foo")
            base = Base("bar")
            group.add(base)

            # group to dictionary
            data = group.to_dict()

            copy_of_group = Group()
            copy_of_group.from_dict(data)
        """
        super().from_dict(data)
        for key, value in data.get("_group", {}).items():
            if key == "children":
                for child_dict in value:
                    child = Object.instantiate(child_dict["_class"])
                    self.add(child)
                    child.from_dict(child_dict)
            else:
                setattr(self, key, value)

    @classmethod
    def register(cls):
        if cls._class_id == "":
            Base.register()
            cls.initialize_class()
