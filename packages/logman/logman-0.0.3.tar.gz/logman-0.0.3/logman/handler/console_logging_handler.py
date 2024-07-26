import logging


class ConsoleLoggingHandler(logging.StreamHandler):
    """
    A custom logging handler that outputs logs to the console.

    Args:
        formatter (logging.Formatter): The formatter to use for formatting log messages.
        level (int, optional): The logging level. Defaults to logging.DEBUG.

    Methods:
        __init__(formatter, level=logging.DEBUG): Initializes the handler with the specified formatter and logging level.
    """

    def __init__(self, formatter: logging.Formatter, level: int = logging.DEBUG):
        """
        Initialize the handler with the specified formatter and logging level.

        Args:
            formatter (logging.Formatter): The formatter to use for formatting log messages.
            level (int, optional): The logging level. Defaults to logging.DEBUG.
        """
        super().__init__()
        self.setLevel(level)
        self.setFormatter(formatter)
