from juham.base.jdatabase import JDatabase


class JConsole(JDatabase):
    """Database interface that simply dumps the written records to stdout
    solely for testing and debugging purposes."""

    _class_id = ""

    def __init__(self, name="jconsole"):
        super().__init__(name)

    def write(self, point):
        print(f"Table:{self.database}:  {str(point)}")

    @classmethod
    def register(cls):
        if cls._class_id == "":
            JDatabase.register()
            cls.initialize_class()
