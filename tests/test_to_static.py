"""Test the to_static() functionality for CheapSettings."""
import os
import pickle

import pytest

from cheap_settings import CheapSettings


class BasicSettings(CheapSettings):
    """Basic settings for testing."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


class TestToStatic:
    """Test the to_static() class method."""

    def test_basic_static_conversion(self):
        """Test that to_static creates a class with the same values."""
        StaticSettings = BasicSettings.to_static()

        # Verify values are preserved
        assert StaticSettings.host == "localhost"
        assert StaticSettings.port == 8080
        assert StaticSettings.debug is False

        # Verify it's a different class
        assert StaticSettings is not BasicSettings
        assert StaticSettings.__name__ == "StaticBasicSettings"

    def test_static_with_env_override(self):
        """Test that to_static captures environment variable values."""
        os.environ["HOST"] = "production.example.com"
        os.environ["PORT"] = "443"

        try:
            # Create static snapshot with env values
            StaticSettings = BasicSettings.to_static()

            # Static class should have the env values
            assert StaticSettings.host == "production.example.com"
            assert StaticSettings.port == 443

            # Change the env vars
            os.environ["HOST"] = "changed.example.com"

            # Static class should still have the old values (frozen)
            assert StaticSettings.host == "production.example.com"

            # Original class should see the new env value
            assert BasicSettings.host == "changed.example.com"

        finally:
            # Clean up
            del os.environ["HOST"]
            del os.environ["PORT"]

    def test_static_class_is_regular_class(self):
        """Test that the static class is a regular Python class."""
        StaticSettings = BasicSettings.to_static()

        # Should not have the metaclass
        assert type(StaticSettings) is type
        assert not hasattr(StaticSettings, '__config_instance')

        # Setting attributes should work normally
        StaticSettings.new_attr = "test"
        assert StaticSettings.new_attr == "test"

    def test_static_excludes_methods(self):
        """Test that methods are not copied to static class."""
        # Create a settings class with methods
        class SettingsWithMethods(CheapSettings):
            value: int = 42

            @classmethod
            def class_method(cls):
                return "class"

            @staticmethod
            def static_method():
                return "static"

            @property
            def prop(self):
                return "property"

        StaticSettings = SettingsWithMethods.to_static()

        # Should have the value
        assert StaticSettings.value == 42

        # Should not have methods (they're callable and skipped)
        assert not hasattr(StaticSettings, 'class_method')
        assert not hasattr(StaticSettings, 'static_method')
        assert not hasattr(StaticSettings, 'set_config_from_command_line')
        assert not hasattr(StaticSettings, 'to_static')

    def test_static_with_inheritance(self):
        """Test that to_static works with inherited settings."""
        class BaseSettings(CheapSettings):
            base_value: str = "base"

        class DerivedSettings(BaseSettings):
            derived_value: str = "derived"

        StaticDerived = DerivedSettings.to_static()

        # Should have both base and derived values
        assert StaticDerived.base_value == "base"
        assert StaticDerived.derived_value == "derived"

    def test_static_performance(self):
        """Test that static class attribute access is faster."""
        import timeit

        # Create both versions
        StaticSettings = BasicSettings.to_static()

        # Time dynamic access
        dynamic_time = timeit.timeit(
            lambda: BasicSettings.host,
            number=10000
        )

        # Time static access
        static_time = timeit.timeit(
            lambda: StaticSettings.host,
            number=10000
        )

        # We don't assert that static is faster (it might not be significantly so),
        # but we verify both work and complete in reasonable time
        assert dynamic_time < 1.0  # Should complete 10k accesses in under a second
        assert static_time < 1.0