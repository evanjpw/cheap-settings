"""Test pathlib.Path support in CheapSettings."""

from pathlib import Path

from cheap_settings import CheapSettings


class PathSettings(CheapSettings):
    """Settings with Path types."""

    config_dir: Path = Path("/etc/myapp")
    log_file: Path = Path("/var/log/myapp.log")
    data_path: Path = Path("./data")


class TestPathSupport:
    """Test Path type conversion."""

    def test_default_path_values(self):
        """Test that default Path values work."""
        assert PathSettings.config_dir == Path("/etc/myapp")
        assert PathSettings.log_file == Path("/var/log/myapp.log")
        assert PathSettings.data_path == Path("./data")
        assert isinstance(PathSettings.config_dir, Path)

    def test_path_from_env(self, monkeypatch):
        """Test Path conversion from environment variables."""
        monkeypatch.setenv("CONFIG_DIR", "/custom/config")
        monkeypatch.setenv("LOG_FILE", "/tmp/test.log")
        monkeypatch.setenv("DATA_PATH", "../other/data")

        assert PathSettings.config_dir == Path("/custom/config")
        assert PathSettings.log_file == Path("/tmp/test.log")
        assert PathSettings.data_path == Path("../other/data")

        # Verify they're Path objects
        assert isinstance(PathSettings.config_dir, Path)
        assert isinstance(PathSettings.log_file, Path)

    def test_path_with_home_expansion(self, monkeypatch):
        """Test that Path handles home directory expansion."""
        monkeypatch.setenv("CONFIG_DIR", "~/myconfig")

        # Path constructor preserves the ~ (doesn't auto-expand)
        assert str(PathSettings.config_dir) == "~/myconfig"

        # But you can use expanduser() if needed
        expanded = PathSettings.config_dir.expanduser()
        assert str(expanded).startswith(str(Path.home()))

    def test_path_with_spaces(self, monkeypatch):
        """Test Path with spaces in the path."""
        monkeypatch.setenv("CONFIG_DIR", "/path with spaces/config")

        assert PathSettings.config_dir == Path("/path with spaces/config")
        assert str(PathSettings.config_dir) == "/path with spaces/config"

    def test_windows_style_paths(self, monkeypatch):
        """Test Windows-style paths (they work on all platforms as Path objects)."""
        monkeypatch.setenv("CONFIG_DIR", "C:\\Users\\test\\config")

        # Path handles this correctly on all platforms
        path = PathSettings.config_dir
        assert isinstance(path, Path)
        # The string representation will vary by platform
        assert "config" in str(path)

    def test_path_with_command_line(self, monkeypatch):
        """Test that Path types work with command line arguments."""

        # Mock command line arguments
        test_args = ["--config-dir", "/cli/config", "--log-file", "/cli/app.log"]

        # Set config from command line
        PathSettings.set_config_from_command_line(args=test_args)

        # Verify the values were set and are Path objects
        assert PathSettings.config_dir == Path("/cli/config")
        assert PathSettings.log_file == Path("/cli/app.log")
        assert isinstance(PathSettings.config_dir, Path)
        assert isinstance(PathSettings.log_file, Path)
