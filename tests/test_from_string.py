"""Test from_string() method support for custom types."""

import pytest

from cheap_settings import CheapSettings


class CustomType:
    """A custom type with from_string support."""

    def __init__(self, value: int):
        self.value = value

    @classmethod
    def from_string(cls, s: str) -> "CustomType":
        """Convert string to CustomType."""
        return cls(int(s) * 2)  # Double the input for testing

    def __eq__(self, other):
        return isinstance(other, CustomType) and self.value == other.value


class CustomTypeNoFromString:
    """A custom type without from_string support."""

    def __init__(self, value: str):
        self.value = value


def test_custom_type_with_from_string(monkeypatch):
    """Test that custom types with from_string work."""

    class Settings(CheapSettings):
        custom: CustomType = CustomType(10)

    monkeypatch.setenv("CUSTOM", "21")

    # Should use from_string, which doubles the value
    assert Settings.custom.value == 42


def test_custom_type_without_from_string(monkeypatch):
    """Test that custom types without from_string return the string."""

    class Settings(CheapSettings):
        custom: CustomTypeNoFromString = CustomTypeNoFromString("default")

    monkeypatch.setenv("CUSTOM", "from_env")

    # Without from_string, should just return the string
    assert Settings.custom == "from_env"


def test_from_string_with_error(monkeypatch):
    """Test that from_string errors propagate correctly."""

    class FailingType:
        @classmethod
        def from_string(cls, s: str):
            raise ValueError(f"Cannot parse: {s}")

    class Settings(CheapSettings):
        failing: FailingType = None

    monkeypatch.setenv("FAILING", "bad_value")

    with pytest.raises(ValueError, match="Cannot parse: bad_value"):
        _ = Settings.failing


def test_from_string_not_classmethod():
    """Test that instance methods named from_string are ignored."""

    class WeirdType:
        def from_string(self, s: str):  # Instance method, not classmethod
            return "shouldn't be called"

    class Settings(CheapSettings):
        weird: WeirdType = WeirdType()

    # Should not crash, just return the string
    import os

    os.environ["WEIRD"] = "test"
    result = Settings.weird
    assert (
        result == "test"
    )  # Returns string since from_string isn't callable as classmethod
    del os.environ["WEIRD"]


def test_optional_custom_type_with_from_string(monkeypatch):
    """Test Optional custom types with from_string."""
    from typing import Optional

    class Settings(CheapSettings):
        custom: Optional[CustomType] = None

    # Test with "none"
    monkeypatch.setenv("CUSTOM", "none")
    assert Settings.custom is None

    # Test with actual value
    monkeypatch.setenv("CUSTOM", "21")
    assert Settings.custom.value == 42


def test_command_line_custom_type():
    """Test custom types work with command line arguments."""

    class Settings(CheapSettings):
        custom: CustomType = CustomType(10)

    Settings.set_config_from_command_line(args=["--custom", "25"])

    # Should use from_string, which doubles the value
    assert Settings.custom.value == 50
