"""Test type inference from default values."""

from pathlib import Path

from cheap_settings import CheapSettings


class InferredSettings(CheapSettings):
    """Settings without explicit type annotations."""

    # These should infer types from their default values
    host = "localhost"  # Should infer str
    port = 8080  # Should infer int
    timeout = 30.5  # Should infer float
    debug = False  # Should infer bool
    config_path = Path("/etc/config")  # Should infer Path


class TestInferredTypes:
    """Test that types can be inferred from default values."""

    def test_inferred_str_type(self, monkeypatch):
        """Test str type inference."""
        assert InferredSettings.host == "localhost"

        # Set environment variable
        monkeypatch.setenv("HOST", "production.com")
        assert InferredSettings.host == "production.com"
        assert isinstance(InferredSettings.host, str)

    def test_inferred_int_type(self, monkeypatch):
        """Test int type inference."""
        assert InferredSettings.port == 8080

        # Set environment variable
        monkeypatch.setenv("PORT", "9000")
        assert InferredSettings.port == 9000
        assert isinstance(InferredSettings.port, int)

    def test_inferred_float_type(self, monkeypatch):
        """Test float type inference."""
        assert InferredSettings.timeout == 30.5

        # Set environment variable
        monkeypatch.setenv("TIMEOUT", "45.75")
        assert InferredSettings.timeout == 45.75
        assert isinstance(InferredSettings.timeout, float)

    def test_inferred_bool_type(self, monkeypatch):
        """Test bool type inference."""
        assert InferredSettings.debug is False

        # Set environment variable
        monkeypatch.setenv("DEBUG", "true")
        assert InferredSettings.debug is True
        assert isinstance(InferredSettings.debug, bool)

    def test_inferred_path_type(self, monkeypatch):
        """Test Path type inference."""
        assert InferredSettings.config_path == Path("/etc/config")

        # Set environment variable
        monkeypatch.setenv("CONFIG_PATH", "/custom/path")
        assert InferredSettings.config_path == Path("/custom/path")
        assert isinstance(InferredSettings.config_path, Path)

    def test_mixed_explicit_and_inferred(self, monkeypatch):
        """Test class with both explicit annotations and inferred types."""

        class MixedSettings(CheapSettings):
            # Explicit annotation
            database_url: str = "postgresql://localhost/db"
            # Inferred from default
            max_connections = 100

        assert MixedSettings.database_url == "postgresql://localhost/db"
        assert MixedSettings.max_connections == 100

        # Test environment overrides
        monkeypatch.setenv("DATABASE_URL", "mysql://example.com/prod")
        monkeypatch.setenv("MAX_CONNECTIONS", "200")

        assert MixedSettings.database_url == "mysql://example.com/prod"
        assert isinstance(MixedSettings.database_url, str)

        assert MixedSettings.max_connections == 200
        assert isinstance(MixedSettings.max_connections, int)

    def test_command_line_with_inferred_types(self):
        """Test that inferred types work with command line parsing."""

        class CLISettings(CheapSettings):
            host = "localhost"
            port = 8080
            debug = False

        # Test command line arguments
        args = ["--host", "example.com", "--port", "3000", "--debug"]
        CLISettings.set_config_from_command_line(args=args)

        assert CLISettings.host == "example.com"
        assert CLISettings.port == 3000
        assert CLISettings.debug is True

        # Verify types
        assert isinstance(CLISettings.host, str)
        assert isinstance(CLISettings.port, int)
        assert isinstance(CLISettings.debug, bool)
