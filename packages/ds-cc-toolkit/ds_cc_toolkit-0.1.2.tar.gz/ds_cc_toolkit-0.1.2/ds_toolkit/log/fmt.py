"""Provides a utility class for deferred string formatting in logging.

This module contains the Fmt class, which supports `.format` style string formatting in logging contexts.
The class defers the formatting operation until the `__str__` method is called, allowing for more efficient logging.
"""


class Fmt:
    """
    A utility class for deferred string formatting in logging.

    This class is designed to support `.format` style string formatting in logging contexts where the logger
    might not directly support this style. It defers the formatting operation until the `__str__` method is
    called, typically by the logging framework when it actually needs to render the log message as a string.
    This approach allows for more efficient logging, as the formatting operation is only performed if the
    log message is going to be emitted based on the current log level.

    Attributes:
        fmt (str): The format string, containing placeholders for the arguments.
        args (tuple): Positional arguments to be substituted into the format string.
        kwargs (dict): Keyword arguments to be substituted into the format string.

    Methods:
        __str__: Returns the formatted string by substituting the arguments into the format string.
    """

    def __init__(self, fmt, /, *args, **kwargs):
        """
        Initializes a new instance of the Fmt class.

        Args:
            fmt (str): The format string.
            *args: Positional arguments for the format string.
            **kwargs: Keyword arguments for the format string.
        """
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """
        Returns the formatted string by substituting the provided arguments into the format string.

        Returns:
            str: The formatted string.
        """
        return self.fmt.format(*self.args, **self.kwargs)
