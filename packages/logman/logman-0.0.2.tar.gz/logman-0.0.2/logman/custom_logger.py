# mypy: ignore-errors

import logging


class CustomLogger(logging.Logger):
    """
    A custom logger class that automatically includes exception information when logging with error, critical, or fatal levels.

    Methods:
        error(msg, *args, **kwargs): Logs a message with level ERROR on this logger. Automatically includes exception information if not provided.
        critical(msg, *args, **kwargs): Logs a message with level CRITICAL on this logger. Automatically includes exception information if not provided.
        fatal(msg, *args, **kwargs): Logs a message with level FATAL on this logger. Automatically includes exception information if not provided.
    """

    def error(self, msg, *args, **kwargs) -> None:
        """
        Log a message with level ERROR on this logger. Automatically includes exception information if not provided.

        Args:
            msg: The message to log.
            *args: Additional arguments to pass to the logging method.
            **kwargs: Additional keyword arguments to pass to the logging method.

        Returns:
            None
        """
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = True
        super().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        """
        Log a message with level CRITICAL on this logger. Automatically includes exception information if not provided.

        Args:
            msg: The message to log.
            *args: Additional arguments to pass to the logging method.
            **kwargs: Additional keyword arguments to pass to the logging method.

        Returns:
            None
        """
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = True
        super().critical(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs) -> None:
        """
        Log a message with level FATAL on this logger. Automatically includes exception information if not provided.

        Args:
            msg: The message to log.
            *args: Additional arguments to pass to the logging method.
            **kwargs: Additional keyword arguments to pass to the logging method.

        Returns:
            None
        """
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = True
        super().fatal(msg, *args, **kwargs)
