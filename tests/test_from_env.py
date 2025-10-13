"""Test the from_env() class method."""

from cheap_settings import CheapSettings


class TestFromEnv:
    """Test the from_env() class method that only reads environment variables."""

    def test_from_env_basic(self, monkeypatch):
        """Test basic from_env functionality."""

        class MySettings(CheapSettings):
            host: str = "localhost"
            port: int = 8080
            debug: bool = False

        # Set only some env vars
        monkeypatch.setenv("HOST", "example.com")
        monkeypatch.setenv("DEBUG", "true")
        # PORT is not set in env

        EnvSettings = MySettings.from_env()

        # Should have the env values
        assert EnvSettings.host == "example.com"
        assert EnvSettings.debug is True

        # Should NOT have port since it wasn't in env
        assert not hasattr(EnvSettings, "port")

    def test_from_env_empty(self):
        """Test from_env when no env vars are set."""

        class MySettings(CheapSettings):
            host: str = "localhost"
            port: int = 8080

        # No env vars set
        EnvSettings = MySettings.from_env()

        # Should have no attributes
        assert not hasattr(EnvSettings, "host")
        assert not hasattr(EnvSettings, "port")

    def test_from_env_type_conversion(self, monkeypatch):
        """Test that from_env properly converts types."""

        class MySettings(CheapSettings):
            count: int = 0
            rate: float = 0.0
            enabled: bool = False
            items: list = []
            config: dict = {}

        monkeypatch.setenv("COUNT", "42")
        monkeypatch.setenv("RATE", "3.14")
        monkeypatch.setenv("ENABLED", "yes")
        monkeypatch.setenv("ITEMS", '["a", "b", "c"]')
        monkeypatch.setenv("CONFIG", '{"key": "value"}')

        EnvSettings = MySettings.from_env()

        assert EnvSettings.count == 42
        assert isinstance(EnvSettings.count, int)

        assert EnvSettings.rate == 3.14
        assert isinstance(EnvSettings.rate, float)

        assert EnvSettings.enabled is True
        assert isinstance(EnvSettings.enabled, bool)

        assert EnvSettings.items == ["a", "b", "c"]
        assert isinstance(EnvSettings.items, list)

        assert EnvSettings.config == {"key": "value"}
        assert isinstance(EnvSettings.config, dict)

    def test_from_env_with_inheritance(self, monkeypatch):
        """Test from_env with inherited settings."""

        class BaseSettings(CheapSettings):
            base_host: str = "localhost"
            base_port: int = 8080

        class AppSettings(BaseSettings):
            app_debug: bool = False

        monkeypatch.setenv("BASE_HOST", "base.example.com")
        monkeypatch.setenv("APP_DEBUG", "true")
        # base_port not in env

        EnvSettings = AppSettings.from_env()

        assert EnvSettings.base_host == "base.example.com"
        assert EnvSettings.app_debug is True
        assert not hasattr(EnvSettings, "base_port")

    def test_from_env_class_name(self, monkeypatch):
        """Test that from_env creates a properly named class."""

        class MyCustomSettings(CheapSettings):
            value: str = "default"

        monkeypatch.setenv("VALUE", "from_env")

        EnvSettings = MyCustomSettings.from_env()

        # Check the class name
        assert EnvSettings.__name__ == "MyCustomSettingsFromEnv"

    def test_from_env_invalid_conversion_skipped(self, monkeypatch):
        """Test that invalid conversions are skipped in from_env."""

        class MySettings(CheapSettings):
            port: int = 8080
            debug: bool = False

        monkeypatch.setenv("PORT", "not_a_number")  # Invalid int
        monkeypatch.setenv("DEBUG", "true")  # Valid bool

        EnvSettings = MySettings.from_env()

        # PORT should be skipped due to conversion error
        assert not hasattr(EnvSettings, "port")
        # DEBUG should still work
        assert EnvSettings.debug is True

    def test_from_env_is_static(self, monkeypatch):
        """Test that from_env returns a static class without dynamic behavior."""

        class MySettings(CheapSettings):
            host: str = "localhost"

        monkeypatch.setenv("HOST", "example.com")

        EnvSettings = MySettings.from_env()
        assert EnvSettings.host == "example.com"

        # Changing env should not affect the static class
        monkeypatch.setenv("HOST", "changed.com")
        assert EnvSettings.host == "example.com"  # Still the old value

    def test_from_env_comparison_with_regular_settings(self, monkeypatch):
        """Compare from_env with regular settings access."""

        class MySettings(CheapSettings):
            host: str = "localhost"
            port: int = 8080
            debug: bool = False

        monkeypatch.setenv("HOST", "prod.example.com")
        monkeypatch.setenv("PORT", "443")

        # Regular settings (includes defaults)
        assert MySettings.host == "prod.example.com"
        assert MySettings.port == 443
        assert MySettings.debug is False

        # from_env (only env vars)
        EnvSettings = MySettings.from_env()
        assert EnvSettings.host == "prod.example.com"
        assert EnvSettings.port == 443
        assert not hasattr(EnvSettings, "debug")  # Not in env

    def test_from_env_optional_types(self, monkeypatch):
        """Test from_env with Optional types."""
        from typing import Optional

        class MySettings(CheapSettings):
            api_key: Optional[str] = None
            timeout: Optional[int] = None

        monkeypatch.setenv("API_KEY", "secret123")
        monkeypatch.setenv("TIMEOUT", "30")

        EnvSettings = MySettings.from_env()

        assert EnvSettings.api_key == "secret123"
        assert EnvSettings.timeout == 30
