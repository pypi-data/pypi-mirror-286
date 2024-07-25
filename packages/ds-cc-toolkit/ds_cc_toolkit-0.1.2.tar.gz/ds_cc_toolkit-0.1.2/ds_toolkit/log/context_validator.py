"""
ContextValidator is class used for validating a context dictionary against a predefined set of allowed keys.
It ensures that the context contains all required keys, only contains allowed keys, and does not have duplicate values.
"""

from typing import Any, Dict

from ds_toolkit.log.allowed_context import AllowedContext


class ContextValidator:
    """
    A class for validating context dictionaries against a set of allowed keys.

    Attributes:
        allowed_keys (set): A set of keys that are allowed in the context.

    Methods:
        validate(context: Dict[str, Any]) -> None: Validates the context dictionary.
    """

    def __init__(self, allowed_context: AllowedContext) -> None:
        """
        Initializes the ContextValidator with a set of allowed keys extracted from the allowed_context type annotations.

        Parameters:
            allowed_context (Type[Any]): A type with annotations defining the allowed keys for the context.
        """
        self.allowed_keys: set = set(allowed_context.__annotations__.keys())

    def validate(self, context: Dict[str, Any]) -> None:
        """
        Validates the given context dictionary against the allowed keys, checking for required keys, disallowed keys, and duplicate values.

        Parameters:
            context (Dict[str, Any]): The context dictionary to validate.

        Raises:
            ValueError: If the context dictionary contains missing required keys, disallowed keys, or duplicate values.
        """
        self._validate_required_keys(context)
        self._validate_allowed_keys(context)

    def _validate_required_keys(self, context: Dict[str, Any]) -> None:
        """
        Validates that the context contains all required keys.

        Parameters:
            context (Dict[str, Any]): The context dictionary to validate.

        Raises:
            ValueError: If there are missing required keys in the context.
        """
        missing_keys = self.allowed_keys - set(context.keys())
        if missing_keys:
            raise ValueError(
                f"Missing required context keys: {', '.join(sorted(missing_keys))}"
            )

    def _validate_allowed_keys(self, context: Dict[str, Any]) -> None:
        """
        Validates that the context does not contain any keys that are not allowed.

        Parameters:
            context (Dict[str, Any]): The context dictionary to validate.

        Raises:
            ValueError: If there are extra keys in the context that are not allowed.
        """
        extra_keys = set(context.keys()) - self.allowed_keys
        if extra_keys:
            raise ValueError(
                f"Context contains extra keys not allowed: {', '.join(sorted(extra_keys))}"
            )
