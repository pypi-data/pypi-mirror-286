import logging
import logging.handlers
import threading
import os
from typing import Dict, List, Union
from logman.handler import FileRotateLoggingHandler, ConsoleLoggingHandler
from logman.formatter import JsonFormatter
from logman.custom_logger import CustomLogger

# Set the custom logger class
logging.setLoggerClass(CustomLogger)


class LoggerFactory:
    """
    A factory class for creating and managing loggers with file rotation and console output.

    Attributes:
        _filePath (Union[str, os.PathLike[str]]): The default log file path.
        _maxBytes (int): The maximum size of the log file before rotation occurs.
        _loggers (Dict[str, logging.Logger]): A dictionary to store created loggers.
        _lock (threading.Lock): A lock to ensure thread safety.
        _initialized (bool): A flag to check if logging has been initialized.
    """

    _filePath: Union[str, os.PathLike[str]] = "logs/app.log"
    _maxBytes: int = 30 * 1024 * 1024
    _loggers: Dict[str, logging.Logger] = {}
    _lock = threading.Lock()
    _initialized = False

    @classmethod
    def _initialize_logging(cls) -> None:
        """
        Initialize the logging configuration with a file handler and a console handler.

        This method sets up the logging configuration if it hasn't been initialized yet.
        It creates a file handler with rotation and a console handler, both using a JSON formatter.

        Returns:
            None
        """
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    json_formatter = JsonFormatter()
                    log_level = logging.INFO
                    file_handler = FileRotateLoggingHandler(
                        level=log_level,
                        formatter=json_formatter,
                        maxBytes=cls._maxBytes,
                        filePath=cls._filePath,
                    )
                    console_handler = ConsoleLoggingHandler(
                        level=log_level, formatter=json_formatter
                    )

                    cls._add_handler([file_handler, console_handler])
                    cls._initialized = True

    @classmethod
    def _add_handler(cls, handler: Union[logging.Handler, List[logging.Handler]]) -> None:
        """
        Add handlers to the root logger.

        This method clears existing handlers from the root logger and adds the provided handlers.

        Args:
            handler (Union[logging.Handler, List[logging.Handler]]): The handler or list of handlers to add to the root logger.

        Returns:
            None
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.NOTSET)

        if root_logger.hasHandlers():
            for h in root_logger.handlers:
                if isinstance(h, logging.FileHandler):
                    h.close()
            root_logger.handlers.clear()

        if isinstance(handler, list):
            for h in handler:
                root_logger.addHandler(h)
        else:
            root_logger.addHandler(handler)

    @classmethod
    def getLogger(cls, name: str) -> logging.Logger:
        """
        Get a logger by name.

        This method initializes the logging configuration if necessary and returns a logger with the specified name.

        Args:
            name (str): The name of the logger to retrieve.

        Returns:
            logging.Logger: The logger instance with the specified name.
        """
        cls._initialize_logging()
        if name not in cls._loggers:
            with cls._lock:
                if name not in cls._loggers:
                    cls._loggers[name] = logging.getLogger(name)
        return cls._loggers[name]
