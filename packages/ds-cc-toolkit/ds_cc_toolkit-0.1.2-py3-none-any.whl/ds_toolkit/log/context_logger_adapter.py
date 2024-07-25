"""
Enhances logging with additional context by defining the ContextLoggerAdapter class.

This module is designed to enrich logging output with contextual information, aiding in the distinction and understanding
of logs from various parts of an application or different instances. It includes the ContextLoggerAdapter class for this purpose"""

import logging
from typing import Dict, Optional

from ds_toolkit.log.allowed_context import AllowedContext
from ds_toolkit.log.context_validator import ContextValidator
from ds_toolkit.log.json_log_formatter import JSONLogFormatter

SupportedFormatters = JSONLogFormatter
context_validator = ContextValidator(AllowedContext)


class ContextLoggerAdapter(logging.LoggerAdapter):
    """
    A logging adapter that provides a unique instance based on the logger's name, allowing for context-specific logging.

    This adapter enhances the standard logging capabilities by allowing the inclusion of contextual information in log messages,
    making it easier to trace and understand logs from different parts of an application. It supports singleton-like behavior
    for instances with the same name, ensuring that only one instance exists for each unique logger name, unless different
    context or formatter arguments are provided.

    Attributes:
        _instances (Dict[str, "ContextLoggerAdapter"]): A class-level dictionary that stores instances of ContextLoggerAdapter
            by their names to ensure unique instances for each name.

    Methods:
        __new__(cls, name, level, context=None, formatter=None): Attempts to return an existing instance if one exists with the
            same name and no context or formatter is provided. Otherwise, it creates a new instance.
    """

    _instances: Dict[str, "ContextLoggerAdapter"] = {}  # Registry of instances by name

    def __new__(
        cls,
        name: str,
        level: Optional[str | int] = None,
        context: Optional[AllowedContext] = None,
        formatter: Optional[SupportedFormatters] = None,
    ) -> "ContextLoggerAdapter":
        """
        Create a new ContextLoggerAdapter instance or return an existing one.

        This method ensures that only one instance of ContextLoggerAdapter per name exists.
        If an instance with the given name already exists, it will return that instance.
        If `context` or `formatter` is provided and not None, it will update the existing instance with these values.
        Similarly, if `level` is provided, it will update the logging level of the existing instance.

        Parameters:
        - cls: The class.
        - name: The name of the logger adapter. Used to identify unique instances.
        - level: The logging level. Required on first initialisation.
        - context: Optional context information to be included in log messages.
        - formatter: Optional formatter for log messages.

        Returns:
        - An instance of ContextLoggerAdapter.
        """
        existing_instance = cls._instances.get(name)
        if existing_instance:
            if context is not None or formatter is not None:
                if context is not None:
                    existing_instance.replace_context(context)
                if formatter is not None:
                    existing_instance.formatter = formatter
                    # Reconfigure logger to use the new formatter
                    for handler in existing_instance.logger.handlers:
                        handler.setFormatter(formatter)
            if level is not None:
                existing_instance.logger.setLevel(level)
                for handler in existing_instance.logger.handlers:
                    handler.setLevel(level)
            return existing_instance

        instance = super(ContextLoggerAdapter, cls).__new__(cls)
        cls._instances[name] = instance
        return instance

    def __init__(
        self,
        name: str,
        level: Optional[str | int] = None,
        context: Optional[AllowedContext] = None,
        formatter: Optional[SupportedFormatters] = None,
    ):
        """
        Initializes a ContextLoggerAdapter with a logger name, level, and optional context and formatter.

        This method configures the underlying logger and its formatter, ensuring that the logger is ready for use
        with the specified context and formatting.

        Parameters:
            name (str): The name of the logger.
            level (Union[str, int]): The logging level, either as a string (e.g., 'DEBUG') or an integer (logging.DEBUG).
            context (Optional[AllowedContext]): The context to include in log messages, if any.
            formatter (Optional[SupportedFormatters]): The formatter to use for log messages, if any.

        Raises:
            ValueError: If the context contains keys not allowed in AllowedContext.
        """
        if not hasattr(self, "_initialized"):
            if level is None:
                raise ValueError(
                    "Level is required when the instance is not initialized."
                )
            self.formatter = formatter if formatter is not None else JSONLogFormatter()
            context = context if context is not None else {}
            self.replace_context(context)
            self._configure_logger(name, level)
            self._initialized = True

    def _configure_logger(self, name: str, level: str | int):
        """
        Configures the logger with the specified name and level.

        This method sets the logging level and ensures the logger has at least one handler. If no handlers are present,
        a new StreamHandler is added. If handlers exist, their level is updated.

        Parameters:
            name (str): The logger's name, typically a dot-separated hierarchical name.
            level (Union[str, int]): The logging level, either as a string (e.g., 'INFO') or an integer (logging.INFO).
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.hasHandlers():
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)
        else:
            for handler in self.logger.handlers:
                handler.setLevel(level)

    def replace_context(self, new_context: AllowedContext):
        """
        Replaces the current context with a new one, after validating it.

        Parameters:
            new_context (AllowedContext): The new context to set.
        """
        context_validator.validate(new_context)
        self.extra = new_context
