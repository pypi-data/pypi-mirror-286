import logging


class JLog(logging.Logger):
    """Default logger for logging events to application log and/or to
    console."""

    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)
        """Creates and initializes default logger with the given name and
        logging level. Typically the name is the name of the application.

        Args:
            name: name of the logger
            level: logging level, the default is logging.DEBUG
        """

        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # log file
        fileFormatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-0.140s"
        )
        fileHandler = logging.FileHandler(name)
        fileHandler.setFormatter(fileFormatter)
        self.addHandler(fileHandler)

        # console
        consoleFormatter = logging.Formatter(
            "[%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-0.140s"
        )
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)
        self.addHandler(consoleHandler)
