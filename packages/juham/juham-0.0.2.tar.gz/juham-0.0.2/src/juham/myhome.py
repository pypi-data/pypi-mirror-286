import logging
from juham.app import JApp
from juham.base import Object
from juham.base import JLog
from juham.database import JInflux
from juham.mqtt import JPaho2


class MyHomeApp(JApp):
    """Juham home automation application."""

    _class_id = None
    application_name = "myhome"

    def __init__(self, name: str = "myhome"):
        """Creates home automation application with the given name.

        Args:
            name (str): name for the application
        """
        super().__init__(name)

    @classmethod
    def register(cls):
        if cls._class_id is None:
            app_name = "myhome"
            JApp.register()
            JApp.application_name = app_name
            Object.set_log(JLog(app_name, logging.DEBUG))
            JInflux.register()
            JPaho2.register()

            # register plugins
            cls.load_plugins()
            cls.initialize_class()


def main():

    # instantiate the application
    app = MyHomeApp()

    # load configuration to instantiate home automation objects
    try:
        with open("myhome.json", "r") as f:
            app.deserialize_from_json(f)
    except FileNotFoundError:
        app.warning(f'No "myhome.json" found, falling back to default configuration')
        plugins = app.instantiate_plugins(app.plugins)
        app.add_all(plugins)
    except Exception as e:
        app.error(f'Exception {e} occurred while reading "myhome.json"')
        exit(1)

    # start the network loops
    app.run()

    # save the current state of the application
    with open("myhome.json", "w") as f:
        app.serialize_to_json(f)


if __name__ == "__main__":
    main()
