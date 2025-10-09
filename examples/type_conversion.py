#!/usr/bin/env python3
"""Type conversion demonstration.

Shows all the types that CheapSettings can automatically convert
from environment variable strings.
"""

import os
from typing import Optional

from cheap_settings import CheapSettings


class TypedSettings(CheapSettings):
    """Settings demonstrating various type conversions."""

    # Basic types
    text_value: str = "default text"
    integer_value: int = 42
    float_value: float = 3.14159
    boolean_value: bool = False

    # Complex types (parsed from JSON)
    string_list: list = ["apple", "banana", "cherry"]
    number_list: list = [1, 2, 3, 4, 5]
    config_dict: dict = {"timeout": 30, "retries": 3}

    # Optional types
    optional_string: Optional[str] = None
    optional_int: Optional[int] = None
    optional_float: Optional[float] = 2.718

    # Python 3.10+ union syntax also works
    # union_value: str | int = "hello"


def main():
    print("=== Type Conversion Examples ===\n")

    print("Default Values (with their types):")
    print(
        f"  text_value: {TypedSettings.text_value!r} ({type(TypedSettings.text_value).__name__})"
    )
    print(
        f"  integer_value: {TypedSettings.integer_value} ({type(TypedSettings.integer_value).__name__})"
    )
    print(
        f"  float_value: {TypedSettings.float_value} ({type(TypedSettings.float_value).__name__})"
    )
    print(
        f"  boolean_value: {TypedSettings.boolean_value} ({type(TypedSettings.boolean_value).__name__})"
    )
    print(
        f"  string_list: {TypedSettings.string_list} ({type(TypedSettings.string_list).__name__})"
    )
    print(
        f"  config_dict: {TypedSettings.config_dict} ({type(TypedSettings.config_dict).__name__})"
    )
    print(
        f"  optional_string: {TypedSettings.optional_string} ({type(TypedSettings.optional_string).__name__})"
    )
    print(
        f"  optional_float: {TypedSettings.optional_float} ({type(TypedSettings.optional_float).__name__})"
    )

    print("\n" + "=" * 50)
    print("Setting environment variables with string values...")
    print("=" * 50 + "\n")

    # Set environment variables (all as strings!)
    os.environ["TEXT_VALUE"] = "environment text"
    os.environ["INTEGER_VALUE"] = "999"
    os.environ["FLOAT_VALUE"] = "2.71828"
    os.environ["BOOLEAN_VALUE"] = "true"  # Also accepts: yes, on, 1

    # JSON strings for complex types
    os.environ["STRING_LIST"] = '["red", "green", "blue"]'
    os.environ["NUMBER_LIST"] = "[10, 20, 30, 40, 50]"
    os.environ["CONFIG_DICT"] = '{"timeout": 60, "retries": 5, "host": "example.com"}'

    # Optional types
    os.environ["OPTIONAL_STRING"] = "now has a value"
    os.environ["OPTIONAL_INT"] = "42"
    os.environ["OPTIONAL_FLOAT"] = "none"  # Special: "none" sets Optional to None

    print("After Setting Environment Variables:")
    print(f"  text_value: {TypedSettings.text_value!r}")
    print(
        f"  integer_value: {TypedSettings.integer_value} (converted from string '999')"
    )
    print(
        f"  float_value: {TypedSettings.float_value} (converted from string '2.71828')"
    )
    print(
        f"  boolean_value: {TypedSettings.boolean_value} (converted from string 'true')"
    )
    print(f"  string_list: {TypedSettings.string_list} (parsed from JSON)")
    print(f"  number_list: {TypedSettings.number_list} (parsed from JSON)")
    print(f"  config_dict: {TypedSettings.config_dict} (parsed from JSON)")
    print(f"  optional_string: {TypedSettings.optional_string!r} (was None)")
    print(f"  optional_int: {TypedSettings.optional_int} (was None)")
    print(f"  optional_float: {TypedSettings.optional_float} (set to None via 'none')")

    print("\n=== Boolean Conversion ===")
    print("Accepted TRUE values: 'true', 'yes', 'on', '1' (case-insensitive)")
    print("Accepted FALSE values: 'false', 'no', 'off', '0' (case-insensitive)")

    # Test boolean variations
    for bool_value in ["TRUE", "Yes", "on", "1", "FALSE", "No", "off", "0"]:
        os.environ["BOOLEAN_VALUE"] = bool_value
        print(f"  BOOLEAN_VALUE='{bool_value}' → {TypedSettings.boolean_value}")

    # Clean up
    for key in os.environ.copy():
        if key.startswith(
            (
                "TEXT_",
                "INTEGER_",
                "FLOAT_",
                "BOOLEAN_",
                "STRING_",
                "NUMBER_",
                "CONFIG_",
                "OPTIONAL_",
            )
        ):
            del os.environ[key]


if __name__ == "__main__":
    main()
