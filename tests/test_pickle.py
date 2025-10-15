"""Test pickling support for CheapSettings."""

import os
import pickle
from typing import Optional

import pytest

from cheap_settings import CheapSettings


class SimpleSettings(CheapSettings):
    """Simple settings for testing."""

    host: str = "localhost"
    port: int = 8080
    debug: bool = False


class ComplexSettings(CheapSettings):
    """Settings with more complex types."""

    name: str = "test"
    count: int = 42
    ratio: float = 3.14
    enabled: bool = True
    tags: list = ["a", "b", "c"]
    config: dict = {"key": "value"}
    optional: Optional[str] = None


class SettingsWithUninitialized(CheapSettings):
    """Settings with uninitialized values for testing."""

    initialized: str = "default"
    uninitialized: str


class BaseSettings(CheapSettings):
    """Base settings for inheritance testing."""

    base_value: str = "base"
    shared: int = 100


class DerivedSettings(BaseSettings):
    """Derived settings for inheritance testing."""

    derived_value: str = "derived"
    shared: int = 200  # Override parent value


class TestPickleSupport:
    """Test pickle compatibility for CheapSettings classes."""

    def test_pickle_simple_class(self):
        """Test that a simple settings class can be pickled and unpickled."""
        # Get original values
        original_host = SimpleSettings.host
        original_port = SimpleSettings.port
        original_debug = SimpleSettings.debug

        # Pickle and unpickle the class
        pickled = pickle.dumps(SimpleSettings)
        unpickled_class = pickle.loads(pickled)

        # Verify the class works after unpickling
        assert unpickled_class.host == original_host
        assert unpickled_class.port == original_port
        assert unpickled_class.debug == original_debug

    def test_pickle_complex_class(self):
        """Test that a settings class with complex types can be pickled."""
        # Get original values
        original_name = ComplexSettings.name
        original_tags = ComplexSettings.tags
        original_config = ComplexSettings.config

        # Pickle and unpickle
        pickled = pickle.dumps(ComplexSettings)
        unpickled_class = pickle.loads(pickled)

        # Verify values
        assert unpickled_class.name == original_name
        assert unpickled_class.tags == original_tags
        assert unpickled_class.config == original_config

    def test_pickle_instance(self):
        """Test that instances of CheapSettings can be pickled."""
        # Create an instance
        instance = SimpleSettings()

        # Pickle and unpickle the instance
        pickled = pickle.dumps(instance)
        unpickled_instance = pickle.loads(pickled)

        # Verify the instance has access to settings
        assert hasattr(unpickled_instance, "host")
        assert hasattr(unpickled_instance, "port")

    def test_pickle_with_env_override(self):
        """Test pickling when environment variables override defaults."""
        # Set environment variable
        os.environ["HOST"] = "env-host.com"

        try:
            # Get the value (should come from env)
            env_host = SimpleSettings.host
            assert env_host == "env-host.com"

            # Pickle the class
            pickled = pickle.dumps(SimpleSettings)

            # Clear the environment variable
            del os.environ["HOST"]

            # Unpickle - should get default value now
            unpickled_class = pickle.loads(pickled)
            assert unpickled_class.host == "localhost"  # Back to default

        finally:
            # Clean up
            if "HOST" in os.environ:
                del os.environ["HOST"]

    def test_pickle_preserves_type_annotations(self):
        """Test that type annotations are preserved through pickling."""
        # Pickle and unpickle
        pickled = pickle.dumps(ComplexSettings)
        unpickled_class = pickle.loads(pickled)

        # Check that we can still access typed attributes correctly
        assert isinstance(unpickled_class.name, str)
        assert isinstance(unpickled_class.count, int)
        assert isinstance(unpickled_class.ratio, float)
        assert isinstance(unpickled_class.enabled, bool)

    def test_pickle_with_inheritance(self):
        """Test pickling with inherited settings."""
        # Test with module-level classes that support inheritance
        pickled = pickle.dumps(DerivedSettings)
        unpickled_class = pickle.loads(pickled)

        # Verify both base and derived values are accessible
        assert unpickled_class.base_value == "base"
        assert unpickled_class.derived_value == "derived"
        assert unpickled_class.shared == 200  # Should have the overridden value

    def test_local_class_pickle_limitation(self):
        """Document that local classes cannot be pickled."""

        # This is a Python limitation, not specific to CheapSettings
        class LocalSettings(CheapSettings):
            value: str = "local"

        with pytest.raises(AttributeError, match="Can't pickle local object"):
            pickle.dumps(LocalSettings)

    @pytest.mark.parametrize(
        "value,expected_type",
        [
            ("localhost", str),
            (8080, int),
            (3.14, float),
            (True, bool),
            (["a", "b"], list),
            ({"key": "value"}, dict),
        ],
    )
    def test_pickle_individual_values(self, value, expected_type):
        """Test that individual setting values can be pickled."""
        pickled = pickle.dumps(value)
        unpickled = pickle.loads(pickled)
        assert unpickled == value
        assert isinstance(unpickled, expected_type)

    def test_pickle_with_uninitialized_settings(self, monkeypatch):
        """Test pickling classes with uninitialized settings."""

        # Test class pickling
        pickled_class = pickle.dumps(SettingsWithUninitialized)
        UnpickledClass = pickle.loads(pickled_class)

        assert UnpickledClass.initialized == "default"
        assert UnpickledClass.uninitialized is None

        # Test with environment variable
        monkeypatch.setenv("UNINITIALIZED", "from_env")
        assert UnpickledClass.uninitialized == "from_env"

        # Test instance pickling
        instance = SettingsWithUninitialized()
        pickled_instance = pickle.dumps(instance)
        unpickled_instance = pickle.loads(pickled_instance)

        assert unpickled_instance.initialized == "default"
        assert unpickled_instance.uninitialized == "from_env"
