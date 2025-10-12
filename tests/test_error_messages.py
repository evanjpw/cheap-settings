"""Test improved error messages for better user experience."""

import pytest

from cheap_settings import CheapSettings


class ErrorTestSettings(CheapSettings):
    """Settings for testing error messages."""

    tags: list = []
    config: dict = {}


class TestErrorMessages:
    """Test that error messages are helpful."""

    def test_json_single_quote_error(self, monkeypatch):
        """Test helpful error for single quotes in JSON."""
        monkeypatch.setenv("TAGS", "['item1', 'item2']")  # Wrong: single quotes

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.tags

        error_message = str(exc_info.value)
        assert "Invalid JSON in TAGS environment variable" in error_message
        assert "Your value: \"['item1', 'item2']\"" in error_message
        assert "Use double quotes" in error_message
        assert 'Example: ["item1", "item2"]' in error_message

    def test_json_empty_value_error(self, monkeypatch):
        """Test helpful error for empty/invalid JSON."""
        monkeypatch.setenv("TAGS", "")

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.tags

        error_message = str(exc_info.value)
        assert "Invalid JSON in TAGS environment variable" in error_message
        assert "Empty values are not valid" in error_message
        assert "Use '[]' for empty list" in error_message

    def test_json_type_mismatch_list_got_dict(self, monkeypatch):
        """Test helpful error when expecting list but got dict."""
        monkeypatch.setenv("TAGS", '{"key": "value"}')  # Dict instead of list

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.tags

        error_message = str(exc_info.value)
        assert "JSON type mismatch in TAGS" in error_message
        assert "Expected: list" in error_message
        assert "Got: dict" in error_message
        assert "change the type annotation to 'dict'" in error_message

    def test_json_type_mismatch_dict_got_list(self, monkeypatch):
        """Test helpful error when expecting dict but got list."""
        monkeypatch.setenv("CONFIG", '["item1", "item2"]')  # List instead of dict

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.config

        error_message = str(exc_info.value)
        assert "JSON type mismatch in CONFIG" in error_message
        assert "Expected: dict" in error_message
        assert "Got: list" in error_message
        assert "change the type annotation to 'list'" in error_message

    def test_json_missing_quotes(self, monkeypatch):
        """Test helpful error for missing quotes in JSON."""
        monkeypatch.setenv("TAGS", "[item1, item2]")  # Missing quotes around strings

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.tags

        error_message = str(exc_info.value)
        assert "Invalid JSON in TAGS" in error_message
        assert "Your value: '[item1, item2]'" in error_message
        # The specific JSON error will be shown

    def test_json_python_syntax_error(self, monkeypatch):
        """Test error for using Python syntax instead of JSON."""
        monkeypatch.setenv("CONFIG", "{'key': 'value'}")  # Python dict, not JSON

        with pytest.raises(ValueError) as exc_info:
            _ = ErrorTestSettings.config

        error_message = str(exc_info.value)
        assert "Invalid JSON in CONFIG" in error_message
        assert "Use double quotes" in error_message

    def test_type_conversion_error(self, monkeypatch):
        """Test error messages for basic type conversion failures."""

        class TypeSettings(CheapSettings):
            port: int = 8080

        monkeypatch.setenv("PORT", "not_a_number")

        with pytest.raises(ValueError) as exc_info:
            _ = TypeSettings.port

        # Should get the standard int conversion error
        assert "invalid literal for int()" in str(exc_info.value)
