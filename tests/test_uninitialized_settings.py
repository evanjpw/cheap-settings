"""Test settings without initializers (uninitialized settings)."""

from typing import Optional

from cheap_settings import CheapSettings


class TestUninitializedSettings:
    """Test settings without initializers."""

    def test_uninitialized_setting_returns_none_by_default(self):
        """Test that uninitialized settings return None by default."""

        class MySettings(CheapSettings):
            initialized: str = "default"
            uninitialized: str

        assert MySettings.initialized == "default"
        assert MySettings.uninitialized is None

    def test_uninitialized_setting_with_env_var(self, monkeypatch):
        """Test that uninitialized settings work with environment variables."""

        class MySettings(CheapSettings):
            uninitialized: str

        monkeypatch.setenv("UNINITIALIZED", "from_env")
        assert MySettings.uninitialized == "from_env"

    def test_optional_uninitialized_setting(self):
        """Test that Optional uninitialized settings return None."""

        class MySettings(CheapSettings):
            optional_setting: Optional[str]

        assert MySettings.optional_setting is None

    def test_set_raise_on_uninitialized_method_exists(self):
        """Test that the set_raise_on_uninitialized method exists."""

        class MySettings(CheapSettings):
            setting: str

        # Should not raise
        MySettings.set_raise_on_uninitialized(True)
        MySettings.set_raise_on_uninitialized(False)

    def test_inheritance_with_uninitialized_settings(self, monkeypatch):
        """Test that inheritance works with uninitialized settings."""

        class BaseSettings(CheapSettings):
            base_initialized: str = "base_default"
            base_uninitialized: str

        class ChildSettings(BaseSettings):
            child_initialized: str = "child_default"
            child_uninitialized: str

        # Test defaults
        assert ChildSettings.base_initialized == "base_default"
        assert ChildSettings.child_initialized == "child_default"
        assert ChildSettings.base_uninitialized is None
        assert ChildSettings.child_uninitialized is None

        # Test with environment variables
        monkeypatch.setenv("BASE_UNINITIALIZED", "base_from_env")
        monkeypatch.setenv("CHILD_UNINITIALIZED", "child_from_env")

        assert ChildSettings.base_uninitialized == "base_from_env"
        assert ChildSettings.child_uninitialized == "child_from_env"

    def test_mixed_initialized_and_uninitialized(self, monkeypatch):
        """Test class with both initialized and uninitialized settings."""

        class MixedSettings(CheapSettings):
            host: str = "localhost"
            port: int = 8080
            api_key: str  # No default
            timeout: Optional[int]  # No default, Optional

        # Defaults
        assert MixedSettings.host == "localhost"
        assert MixedSettings.port == 8080
        assert MixedSettings.api_key is None
        assert MixedSettings.timeout is None

        # With env vars
        monkeypatch.setenv("HOST", "example.com")
        monkeypatch.setenv("API_KEY", "secret123")
        monkeypatch.setenv("TIMEOUT", "30")

        assert MixedSettings.host == "example.com"
        assert MixedSettings.port == 8080  # Not overridden
        assert MixedSettings.api_key == "secret123"
        assert MixedSettings.timeout == 30

    def test_uninitialized_with_type_conversion(self, monkeypatch):
        """Test that uninitialized settings handle type conversion."""

        class TypedSettings(CheapSettings):
            count: int
            rate: float
            enabled: bool
            items: list
            config: dict

        # All should be None by default
        assert TypedSettings.count is None
        assert TypedSettings.rate is None
        assert TypedSettings.enabled is None
        assert TypedSettings.items is None
        assert TypedSettings.config is None

        # With environment variables
        monkeypatch.setenv("COUNT", "42")
        monkeypatch.setenv("RATE", "3.14")
        monkeypatch.setenv("ENABLED", "true")
        monkeypatch.setenv("ITEMS", '["a", "b"]')
        monkeypatch.setenv("CONFIG", '{"key": "value"}')

        assert TypedSettings.count == 42
        assert TypedSettings.rate == 3.14
        assert TypedSettings.enabled is True
        assert TypedSettings.items == ["a", "b"]
        assert TypedSettings.config == {"key": "value"}

    def test_uninitialized_in_from_env(self, monkeypatch):
        """Test that uninitialized settings work with from_env()."""

        class MySettings(CheapSettings):
            initialized: str = "default"
            uninitialized: str

        # No env vars set
        EnvOnly = MySettings.from_env()
        assert not hasattr(EnvOnly, "initialized")
        assert not hasattr(EnvOnly, "uninitialized")

        # Set env var for uninitialized setting
        monkeypatch.setenv("UNINITIALIZED", "from_env")
        EnvOnly = MySettings.from_env()
        assert not hasattr(EnvOnly, "initialized")
        assert EnvOnly.uninitialized == "from_env"

    def test_uninitialized_in_to_static(self, monkeypatch):
        """Test that uninitialized settings work with to_static()."""

        class MySettings(CheapSettings):
            initialized: str = "default"
            uninitialized: str

        # Create static snapshot
        StaticSettings = MySettings.to_static()
        assert StaticSettings.initialized == "default"
        assert StaticSettings.uninitialized is None

        # With environment variable
        monkeypatch.setenv("UNINITIALIZED", "from_env")
        StaticSettings = MySettings.to_static()
        assert StaticSettings.initialized == "default"
        assert StaticSettings.uninitialized == "from_env"
