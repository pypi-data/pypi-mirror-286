import logging
import os
from typing import Union


class FileRotateLoggingHandler(logging.handlers.RotatingFileHandler):
    """
    A custom logging handler that writes logs to a file with rotation.

    Args:
        formatter (logging.Formatter): The formatter to use for formatting log messages.
        filePath (Union[str, os.PathLike[str]]): The path to the log file.
        maxBytes (int): The maximum size of the log file before rotation occurs.
        level (int, optional): The logging level. Defaults to logging.DEBUG.

    Methods:
        __init__(formatter, filePath, maxBytes, level=logging.DEBUG): Initializes the handler with the specified parameters.
    """

    def __init__(
        self,
        formatter: logging.Formatter,
        filePath: Union[str, os.PathLike[str]],
        maxBytes: int,
        level: int = logging.DEBUG,
    ):
        """
        Initialize the handler with the specified parameters.

        Args:
            formatter (logging.Formatter): The formatter to use for formatting log messages.
            filePath (Union[str, os.PathLike[str]]): The path to the log file.
            maxBytes (int): The maximum size of the log file before rotation occurs.
            level (int, optional): The logging level. Defaults to logging.DEBUG.
        """
        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))

        super().__init__(
            filePath,
            maxBytes=maxBytes,
            backupCount=10,
            encoding="utf-8",
        )
        self.setLevel(level)
        self.setFormatter(formatter)
