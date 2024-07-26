import logging
import time

from typing import Optional, Any


class PlainFormatter(logging.Formatter):
    """
    A custom plain text formatter for Python logging.

    This formatter outputs log records as plain text strings with specific fields.

    Methods:
        formatTime(record, datefmt=None): Formats the log record's timestamp.
        format(record): Formats the log record as a plain text string.
    """

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """
        Format the log record's timestamp.

        Args:
            record (logging.LogRecord): The log record.
            datefmt (Optional[str]): The date format string.

        Returns:
            str: The formatted timestamp.
        """
        if datefmt:
            return super().formatTime(record, datefmt)
        ct = self.converter(record.created)
        t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        s = "%s.%03d" % (t, record.msecs)
        return s

    def format(self, record: Any) -> str:
        """
        Format the log record as a plain text string.

        Args:
            record (Any): The log record.

        Returns:
            str: The formatted log record as a plain text string.
        """
        formatted_message = f"{self.formatTime(record)} - {record.levelname} - {record.name} - {record.getMessage()}"

        if record.exc_info:
            formatted_message += f"\n{self.formatException(record.exc_info)}"

        if record.stack_info:
            formatted_message += f"\n{record.stack_info}"

        return formatted_message
