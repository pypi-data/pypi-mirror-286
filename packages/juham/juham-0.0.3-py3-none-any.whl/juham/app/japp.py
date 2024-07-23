from typing import List
from juham.base.group import Group
from juham.base.object import Object
import importlib.metadata  # for plugin architecture


class JApp(Group):
    """Default application class.

    Configures Base class with JPaho2 MQTT and JInflux time series
    database. It is up to the sub classes to initialize appropriate
    JInflux toke, org, host and database attributes to match the Influx
    account in question.
    """

    _class_id = ""
    plugins: List = []

    def __init__(self, name: str) -> None:
        """Instantiates and initializes the Juham application with the given
        name using the default JPaho2 MQTT and JInflux time series database. It
        is up to the subclasses to initialize the appropriate MQTT and JInflux
        attributes, such as token, org, and host. The host and port class
        attributes for MQTT client is set to 'localhost' and 1883. The default
        logger instantiated with the application is configured to write log
        messages to both a log file and stdout. By default, the application log
        filename is set to the same as the application name.

        Args:
            name (str): The name of the application, determining the default log filename.
        """
        super().__init__(name)
        self.children = []
        self.configure()

    @classmethod
    def load_plugins(cls) -> None:
        """Loads all plugins."""
        cls.plugins = []
        for entry_point in importlib.metadata.entry_points(group="juham.plugins"):
            plugin_class = entry_point.load()  # Load the plugin class
            cls.plugins.append(plugin_class)

    @classmethod
    def instantiate_plugins(cls, plugin_classes: list) -> list:
        """Instantiates  all installed plugin classes with their default names.
        This method is provided for testing purposes only, or for small home
        automation applications that needs only one instance per class.

        Args:
            plugins (list) : list of plugin classes

        Returns:
            list of plugin objects
        """
        plugins = []
        for plugin_class in plugin_classes:
            plugin_instance = plugin_class()  # Instantiate the plugin class
            plugins.append(plugin_instance)  # Append the instance to the plugins list
        return plugins

    def add_all(self, plugins) -> None:
        """Add the plugin instances into the application."""
        for plugin in plugins:
            # check if the plugin is already in the list
            if isinstance(plugin, Object):
                if self.find_plugin(plugin.name, type(plugin)) is None:
                    self.add(plugin)
                    self.info(f"Plugin {plugin.name}:{str(type(plugin))} installed")
                else:
                    self.error(
                        f"Plugin {plugin.name}:{str(type(plugin))} already installed"
                    )
            else:
                self.error(f"{type(plugin)} is not a Juham object")

    def configure(self) -> None:
        """Application instance specific configuration tasks.

        Up to the sub classes to implement.
        """

    def find_plugin(self, name, cls):
        """Check if the application contains the given plugin, as defined by
        its name and class, and return the plugin.

        Returns:
            plugin object if found, None if the application does not contain a plugin of that name and type
        """
        for p in self.children:
            if p.name == name and type(p) == cls:
                return p
        return None

    @classmethod
    def register(cls):
        if cls.get_class_id() is None:
            Group.register()
            cls.initialize_class()
