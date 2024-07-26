import logging
import time
import json
from typing import Optional, Any


class JsonFormatter(logging.Formatter):
    """
    A custom JSON formatter for Python logging.

    This formatter outputs log records as JSON strings with specific fields.

    Methods:
        formatTime(record, datefmt=None): Formats the log record's timestamp.
        format(record): Formats the log record as a JSON string.
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

    def format(self, record: Any) -> Any:
        """
        Format the log record as a JSON string.

        Args:
            record (Any): The log record.

        Returns:
            Any: The formatted log record as a JSON string.
        """
        if hasattr(record, "formatted_message"):
            return record.formatted_message

        log_record = {
            "context": record.name,
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
            "thread": record.threadName,
        }

        if record.exc_info:
            log_record["stack_trace"] = self.formatException(record.exc_info)

        if record.stack_info:
            log_record["stack_info"] = record.stack_info

        record.formatted_message = json.dumps(log_record, ensure_ascii=False)
        return record.formatted_message
