import json
from juham.shelly import JShelly
from juham.base import Base


class RBoiler(JShelly):
    """Automation class for controlling Shelly Wifi relay. Subscribes to
    'power' topic and controls the Shelly relay accordingly.

    Args:
        JShelly (class): Super class
    """

    _class_id = ""
    power_topic = "power"  # topic to listen
    relay_url = "shellyplus1-alakerta/command/switch:0"  # relay to control

    def __init__(self, name="rboiler"):
        super().__init__(name)
        self.current_relay_state = 0

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(Base.mqtt_root_topic + "/" + self.power_topic)

    def on_message(self, client, userdata, msg):
        """
        Handle incoming MQTT message
        Args:
            client (object): mqtt client
            userdata (any): user context
            msg (object) : mqtt message
        """
        if msg.topic == self.power_topic:
            self.on_power(json.loads(msg.payload.decode()))
        else:
            super().on_message(client, userdata, msg)

    def on_power(self, m: dict):
        """Process power_topic message.

        Args:
            m (dict): holding data from the power sensor
        """
        if m["Unit"] == "main_boiler":
            new_state = m["State"]

            if new_state != self.current_relay_state:
                self.current_relay_state = new_state
                if new_state == 0:
                    relay = "off"
                else:
                    relay = "on"
                self.publish(self.relay_url, relay, 1)
                self.info(m["Unit"] + " state: " + relay, self.relay_url)
            else:
                self.info(
                    m["Unit"] + " Relay state " + str(new_state) + " not changed", ""
                )

    @classmethod
    def register(cls):
        if cls._class_id == "":
            JShelly.register()
            cls.initialize_class()
            cls.register_topic(Base.mqtt_root_topic + "/" + cls.power_topic)


def main():
    RBoiler().run_forever()


if __name__ == "__main__":
    main()
