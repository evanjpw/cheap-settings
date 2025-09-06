import json
import os
import sys
from typing import Union, get_args, get_origin

# Python 3.10+ has types.UnionType for the | syntax
if sys.version_info >= (3, 10):
    from types import UnionType
else:
    UnionType = None


def _convert_value_to_type(value, to_type):
    """Convert a string value from environment to the specified type.

    Handles basic types (int, float, bool, str, list, dict) as well as
    Union/Optional types. For Optional types, the string "none" (case-insensitive)
    is converted to None. Lists and dicts are parsed from JSON strings.

    Args:
        value: The value to convert (usually a string from os.environ)
        to_type: The type annotation to convert to

    Returns:
        The converted value in the appropriate type

    Raises:
        ValueError: If the value cannot be converted to the specified type
        json.JSONDecodeError: If JSON parsing fails for list/dict types
    """
    if value is None:
        return None

    # Handle the case where value is already the correct type
    if not isinstance(value, str):
        return value

    # Handle Union/Optional types (including Python 3.10+ union syntax)
    origin = get_origin(to_type)
    if origin is Union or (UnionType and isinstance(to_type, UnionType)):
        args = get_args(to_type)

        # Special handling for "none" string in Optional types
        if type(None) in args and value.lower() == "none":
            return None

        # Try each type in the union until one works
        for arg in args:
            if arg is type(None):  # Skip None type
                continue
            try:
                return _convert_value_to_type(value, arg)
            except (ValueError, TypeError, json.JSONDecodeError):
                # TODO: JSON error handling issue also affects Union types - when JSON parsing
                # fails in a Union, we silently try the next type instead of providing helpful errors
                continue
        # If none worked, raise error
        raise ValueError(f"Could not convert '{value}' to any of {args}")

    # Handle generic types like list[str], dict[str, int]
    if origin is not None:
        if origin is list:
            # TODO: Same JSON error handling issue as above - need better error messages
            parsed_value = json.loads(value)
            if not isinstance(parsed_value, list):
                raise ValueError(f"{value} is not a list")
            return parsed_value
        elif origin is dict:
            # TODO: Same JSON error handling issue as above - need better error messages
            parsed_value = json.loads(value)
            if not isinstance(parsed_value, dict):
                raise ValueError(f"{value} is not a dict")
            return parsed_value

    # Handle basic types
    # Check bool before int since bool is a subclass of int
    if to_type is bool:
        normalized_value = value.lower()
        if normalized_value in ("true", "1", "yes", "on"):
            return True
        elif normalized_value in ("false", "0", "no", "off"):
            return False
        else:
            raise ValueError(f"{value} is not a valid boolean value")
    elif to_type is int:
        return int(value)
    elif to_type is float:
        return float(value)
    elif to_type is str:
        return value
    elif to_type is list:
        # TODO: Improve JSON error handling - Currently JSON parsing errors bubble up
        # as raw json.JSONDecodeError with technical messages like "Expecting ',' delimiter".
        # Users would benefit from more helpful error messages that include:
        # 1. Which environment variable caused the error
        # 2. What type was expected (list/dict)
        # 3. A hint about JSON format requirements
        # Example: "Invalid JSON in environment variable ITEMS (expected list):
        # Expecting ',' delimiter: line 1 column 5 (char 4). Ensure the value is valid JSON like [\"item1\", \"item2\"]"
        parsed_value = json.loads(value)
        if not isinstance(parsed_value, list):
            raise ValueError(f"{value} is not a list")
        return parsed_value
    elif to_type is dict:
        parsed_value = json.loads(value)
        if not isinstance(parsed_value, dict):
            raise ValueError(f"{value} is not a dict")
        return parsed_value

    # If we get here, we don't know how to handle this type
    return value


# TODO: Implement __delattr__ & __dir__
class MetaCheapSettings(type):
    """Metaclass that implements the settings behavior for CheapSettings.

    This metaclass intercepts attribute access to check environment variables
    and performs automatic type conversion based on type hints. Each settings
    class gets its own ConfigInstance to store the default values and annotations.
    """

    class ConfigInstance:
        """Internal storage for settings values and type annotations."""

    # TODO: See https://docs.python.org/3/howto/annotations.html#annotations-howto
    def __new__(mcs, name, bases, dct):
        """Create a new settings class with its own config instance.

        Moves class attributes (settings definitions) from the class dict
        to a ConfigInstance, preserving inheritance of settings from parent classes.
        Type annotations are collected from the class and its parents.
        """
        config_instance = mcs.ConfigInstance()

        # Collect annotations from parent classes
        annotations = {}
        for base in reversed(bases):  # Start from the most base class
            try:
                # Use object.__getattribute__ to avoid calling our custom __getattribute__
                parent_config = object.__getattribute__(base, "__config_instance")
                if hasattr(parent_config, "__annotations__"):
                    annotations.update(parent_config.__annotations__)
                # Also copy parent attributes
                for attr in dir(parent_config):
                    if not attr.startswith("__"):
                        setattr(config_instance, attr, getattr(parent_config, attr))
            except AttributeError:
                # Base class doesn't have __config_instance, skip it
                continue

        # Add current class annotations (override parent ones)
        annotations.update(dct.pop("__annotations__", {}))
        config_instance.__annotations__ = annotations

        # Create a list of keys to avoid modifying dict during iteration
        # TODO: Fix non-dunder attribute handling - Currently we remove ALL non-dunder
        # attributes from the class dict, which breaks if users add methods, properties,
        # static methods, or other descriptors to their settings classes. We should only
        # move attributes that represent actual settings (those with type annotations or
        # simple values), but preserve methods, properties, etc. This requires:
        # 1. Distinguishing between settings attributes and other class members
        # 2. Updating __getattribute__ to handle both settings and regular class attributes
        # 3. Testing with classes that have methods, properties, class methods, static methods
        keys_to_move = list(dct.keys())
        for key in keys_to_move:
            if not key.startswith("__") and not key.endswith("__"):
                setattr(config_instance, key, dct.pop(key))
        dct["__config_instance"] = config_instance
        return super().__new__(mcs, name, bases, dct)

    def __getattribute__(cls, attribute):
        """Get attribute value, checking environment variables first.

        For settings attributes, this checks if an environment variable with the
        uppercase attribute name exists. If found, converts the value using
        the type annotation and returns it. Otherwise, returns the default value.
        Supports inheritance by checking parent classes in the MRO.
        """
        # Special attributes that should use default behavior
        if attribute in ("__config_instance", "__mro__", "__class__", "__dict__"):
            return type.__getattribute__(cls, attribute)

        # Check each class in the MRO for the attribute
        mro = type.__getattribute__(cls, "__mro__")
        for klass in mro:
            if not hasattr(klass, "__config_instance"):
                continue

            try:
                config_instance = object.__getattribute__(klass, "__config_instance")
            except AttributeError:
                continue

            if hasattr(config_instance, attribute):
                env_attr = os.environ.get(attribute.upper())
                if env_attr is not None:
                    # Check if we have annotations for this attribute
                    if (
                        hasattr(config_instance, "__annotations__")
                        and attribute in config_instance.__annotations__
                    ):
                        return _convert_value_to_type(
                            env_attr, config_instance.__annotations__[attribute]
                        )
                    else:
                        # No type annotation, return as string
                        return env_attr
                return getattr(config_instance, attribute)

        # If not found in any config instance, use default behavior
        return type.__getattribute__(cls, attribute)

    def __setattr__(cls, attribute, value):
        if attribute == "__config_instance":
            object.__setattr__(cls, attribute, value)
        else:
            config_instance = object.__getattribute__(cls, "__config_instance")
            setattr(config_instance, attribute, value)


class CheapSettings(metaclass=MetaCheapSettings):
    """Base class for simple, environment-variable-driven configuration.

    Subclass this and define your settings as typed class attributes:

        class MySettings(CheapSettings):
            host: str = "localhost"
            port: int = 8080
            debug: bool = False

    Environment variables will override the defaults:
        HOST=example.com PORT=3000 DEBUG=true python myapp.py

    Supports all basic Python types plus Optional and Union types.
    Complex types (list, dict) are parsed from JSON strings.
    """
