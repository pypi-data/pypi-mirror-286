import argparse
import logging


class JLog(logging.Logger):
    """Default logger for logging events to application log and/or to
    console."""

    log_name = ""

    def __init__(self, name, level=logging.INFO):
        """Creates and initializes default logger with the given name and
        logging level. Typically the name is the name of the application.

        Args:
            name: name of the logger
            level: logging level, the default is logging.DEBUG
        """
        super().__init__(name, level)

        if self.log_name == "":
            self.log_name = name

        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # log file
        fileFormatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-0.140s"
        )
        fileHandler = logging.FileHandler(self.log_name)
        fileHandler.setFormatter(fileFormatter)
        self.addHandler(fileHandler)

        # console
        consoleFormatter = logging.Formatter(
            "[%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-0.140s"
        )
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)
        self.addHandler(consoleHandler)

    @classmethod
    def register(cls):
        pass
