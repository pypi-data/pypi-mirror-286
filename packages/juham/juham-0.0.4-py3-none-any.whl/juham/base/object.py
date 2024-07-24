import os
import json
import logging
from typing import Any, Callable, Optional
import atexit
import argparse


class Object:
    """Base class of everything. Serves as the foundational class offering  key
    features needed by any robust object-oriented software.

    Logging:

    All objects have logging methods e.g. info() and error() at their fingertips, for
    centralized logging.
    ::

        if not self.do_good():
            self.error(f"Damn, did bad")

    Factory Method Support:

    Instantiation via class identifiers, adhering to the factory method pattern. This allows for the dynamic creation of
    instances based on identifier strings, promoting decoupled and extensible design required by plugin architecture.
    ::

        # instead of fixed implementation car = Ferrari()
        car = Object.instantiate(car_class_id)


    Serialization:

    Serialization of both class and instance attributes, serving as by means of configuration.
    ::

        # serialize to json file
        with open("ferrari.json", "w") as f:
            ferrari.serialize(f)

        # deserialize
        ferrari = Ferrari()
        with open("ferrari.json", "r") as f:
            ferrari.deserialize(f)


    Cloning:

    Any object can be copied.
    ::

        sphere = Sphere("mycar")
        sphere.radius = 1.8
        sphere.center = [0.1, 0.2, 0.3]

        sphere2 = sphere.copy()


    Class attributes should follow consistent naming convention where underscore prefix
    implies non-serializable attribute.
    """

    # public serializable class attributes
    app_name = "juham"
    config_folder = "config"

    # non-serializable private class attributes
    _log: Optional[logging.Logger] = None
    _factory: dict = {}
    _class_id: str = ""

    @classmethod
    def initialize_class(cls, load_class_attrs: bool = True) -> bool:
        """Initialize the class for instantiation, if not initialized already.
        This method initializes the class identifier and deserializes the
        public attributes from the specified configuration folder.

        Args:
            load_class_attrs (bool, optional): If true then attempts to initialize class attributes
            from the class specific configuration files. Defaults to True.

        Returns:
            bool: returns true if the class was initialized, false implies the class is already initialized
            in which case the method call has no effect.
        """

        if cls._class_id == "":
            cls._class_id = cls.__name__
            Object.register_class(cls._class_id, cls)
            if load_class_attrs:
                cls.load_from_json()
                atexit.register(cls.save_to_json)
            return False
        else:
            return True

    @classmethod
    def is_abstract(cls) -> bool:
        """Check whether the class is abstract or real. Override in the derived
        sub-classes. The default is False.

        Returns:
            True (bool) if abstract
        """
        return False

    @classmethod
    def set_log(cls, l: logging.Logger) -> None:
        """Set logger.

        Args:
            l (logger): logger object
        """

        cls._log = l

    @classmethod
    def get_class_id(cls) -> str:
        """Return the class id of the class. Each class has an unique
        identifier that can be used for instantiating the class via
        :meth:`Object.instantiate` method.

        Args:
            cls (class): class

        Returns:
            id (int) unique class identifier through which the class can be instantiated by factory method pattern.
        """
        return cls.__name__

    def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:
        """Called when new sub-class is created.

        Automatically registers the sub class by calling its register()
        method. For more information on this method consult Python
        documentation.
        """
        super().__init_subclass__(**kwargs)
        cls.register()

    def __init__(self, name: str = "noname") -> None:
        """Creates object with the given name. Initializes logger for the newly
        created object.

        Example:
            ```python
            obj = Object('foo')
            obj.info('Yippee, object created')
            ```
        """
        self.name = name

    def debug(self, msg: str, details: str = "") -> None:
        """Logs the given debug message to the application log.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        if self._log is not None:
            self._log.debug(f"{self.name} : {msg} - {details}")

    def info(self, msg: str, details: str = "") -> None:
        """Logs the given information message to the application log.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        if self._log is not None:
            self._log.info(f"{self.name} : {msg} - {details}")

    def warning(self, msg: str, details: str = "") -> None:
        """Logs the given warning message to the application log.

        Args:
            msg (str): The message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        if self._log is not None:
            self._log.warn(f"{self.name} : {msg} - {details}")

    def error(self, msg: str, details: str = "") -> None:
        """Logs the given error message to the application log.

        Args:
            msg (str): The message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        if self._log is not None:
            self._log.error(f"{self.name} : {msg} - {details}")

    @classmethod
    def get_json_file(cls):
        """Generate the JSON file name based on the class name.

        The file is created into users home folder.
        """
        return os.path.join(
            os.path.expanduser("~"),
            "." + cls.app_name,
            cls.config_folder,
            cls.__name__ + ".json",
        )

    def to_dict(self):
        """Convert instance attributes to a dictionary."""

        return {
            "_class": self.get_class_id(),  # the real class
            "_version:": 0,
            "_object": {
                "name": self.name,
                # Add more attributes here as needed
            },
        }

    def from_dict(self, data):
        """Update instance attributes from a dictionary."""

        if self.get_class_id() != data["_class"]:
            raise ValueError(
                f"Class mismatch, expected:{self.get_class_id()}, actual:{data['_class']}"
            )
        for key, value in data["_object"].items():
            setattr(self, key, value)

    def serialize_to_json(self, f):
        """Serialize."""
        json.dump(self.to_dict(), f, indent=4)

    def deserialize_from_json(self, f):
        """Load  attributes from a JSON file."""
        attributes = json.load(f)
        self.from_dict(attributes)

    def copy(self):
        """Create and return a copy of the current object.

        This method serializes the current object to a dictionary using the `to_dict` method,
        creates a new instance of the object's class, and populates it with the serialized data
        using the `from_dict` method.

        This method uses class identifier based instantiation (see factory method pattern) to create a new instance
        of the object, and 'to_dict' and 'from_dict'  methods to initialize object's state.

        Returns:
            A new instance of the object's class with the same state as the original object.

        Example:
        ::

            john = Human("john")
            john.height = 1.8
            john.age = 62
            clone_of_john = john.copy()
        """

        data = self.to_dict()
        copy_of_self = Object.instantiate(self.get_class_id())
        copy_of_self.from_dict(data)
        return copy_of_self

    @classmethod
    def classattrs_to_dict(cls):
        """Convert class attributes to a dictionary."""
        return {
            attr: getattr(cls, attr)
            for attr in cls.__dict__
            if not callable(getattr(cls, attr))
            and not attr.startswith("__")
            and not attr.startswith(("_"))
        }

    @classmethod
    def classattrs_from_dict(cls, attributes):
        """Set class attributes from a dictionary."""
        for key, value in attributes.items():
            setattr(cls, key, value)

    @classmethod
    def save_to_json(cls):
        """Create class configuration file, if the file does not exist yet."""
        filename = cls.get_json_file()
        if not os.path.exists(filename):
            with open(cls.get_json_file(), "w") as f:
                json.dump(cls.classattrs_to_dict(), f)
                if cls._log is not None:
                    cls._log.info(f"Configuration file {filename} created")

    @classmethod
    def load_from_json(cls):
        """Load class attributes from a JSON file."""
        try:
            filename = cls.get_json_file()
            with open(filename, "r") as f:
                attributes = json.load(f)
                cls.classattrs_from_dict(attributes)
        except FileNotFoundError:
            if cls._log is not None:
                cls._log.info(f"No configuration file {filename} found")

    @classmethod
    def register_class(cls, class_id: str, ctor: Callable):
        """Register the given class identifier for identifier based
        instantiation . This, factory method pattern, as it is called,
        decouples the actual implementation from the interface.  For more
        information see :meth:`instantiate` method.

        Args:
            class_id (str): class identifier
            ctor  (function): constructor
        """
        cls._factory[class_id] = ctor

    @classmethod
    def instantiate(cls, class_id: str) -> object:
        """Create an instance of the class corresponding to the given class identifier.
        This method implements the factory method pattern, which is essential for a plugin architecture.

        Args:
            class_id (int): Identifier of the class to instantiate.

        Returns:
            obj: An instance of the class corresponding to the given class identifier.
        """
        if class_id in cls._factory:
            return cls._factory[class_id]()
        else:
            raise ValueError(f"Attempting to instantiate unregistered class {class_id}")

    @classmethod
    def find_class(cls, class_id: str) -> object:
        """Given class identifier find the registered class. If no class with
        the give identifier exists return None.

        Args:
            class_id (int): class identifier

        Returns:
            obj (obj): class or null if not registered
        """
        if class_id in cls._factory:
            return cls._factory[class_id]
        else:
            return None

    @classmethod
    def instantiate_with_param(cls, class_id: str, param: Any):
        """Given class identifier and one constructor argument create the
        corresponding object.

        Args:
            class_id : class identifier
            param : class specific constructor parameter

        Returns:
            obj : instance of the given class.
        """
        return cls._factory[class_id](param)

    @classmethod
    def parse_args(cls) -> None:
        """Parse the startup arguments defined by this class."""
        parser = argparse.ArgumentParser(description=cls.get_class_id())
        parser.add_argument(
            "--config-folder",
            type=str,
            help="The folder from which to load configuration files",
        )
        args = parser.parse_args()

        if args is not None and args.config_folder:
            cls.config_folder = args.config_folder

    @classmethod
    def register(cls) -> None:
        """Register the class to the class database.

        Once registered the class can be instantiated by its class
        identifier. Note that this method is called automatically by the
        system when the python loads the class. In this method sub
        classes should prepare themselves for instantiation by
        initializing their class attributes, for example.
        """
        if cls._class_id == "":
            cls._class_id = cls.__name__
            cls.parse_args()
            if not cls.is_abstract():
                cls.register_class(cls.get_class_id(), cls)

            # load class attributes from the configuration file
            cls.load_from_json()
            # automatically create configuration file, if not created already
            atexit.register(cls.save_to_json)
