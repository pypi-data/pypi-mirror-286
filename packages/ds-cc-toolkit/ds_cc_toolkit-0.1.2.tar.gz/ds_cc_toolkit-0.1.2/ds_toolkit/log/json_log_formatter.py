"""
This module provides a custom JSON formatter for logging purposes.

It defines a JSONLogFormatter class that extends the logging.Formatter class to support
serializing log records into JSON format. This is particularly useful for applications
that require log data to be in a structured and easily parsable format, such as JSON,
for better integration with log management and analysis tools.
"""

import json
import logging

from ds_toolkit.log.allowed_context import AllowedContext


class JSONLogFormatter(logging.Formatter):
    """
    A formatter for converting log records to JSON format.

    This formatter is designed to serialize log records into JSON strings, facilitating
    easier parsing and processing of log data in systems that consume JSON. It is capable
    of including both standard and custom attributes within the log record, such as 'imei',
    'packet_created_time', and 'packet_processed_time'.

    Attributes:
        Inherits all attributes from the logging.Formatter class.

    Methods:
        format(record): Serializes the log record to a JSON string.
    """

    def format(self, record: logging.LogRecord):
        """
        Serializes the log record to a JSON string.

        Overrides the base class's format method to create a JSON representation of the log
        record. This includes both the standard attributes of a log record and any additional
        custom attributes that have been added to the record.

        Args:
            record (logging.LogRecord): The log record to serialize.

        Returns:
            str: The JSON string representation of the log record.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(
            record
        )  # not sure if this is needed as the message gets evauluated  in record.getMessage()
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)

        log_record = {
            "message": s,
        }
        for attr in AllowedContext.__annotations__.keys():
            log_record[attr] = getattr(record, attr)

        return json.dumps(log_record)
