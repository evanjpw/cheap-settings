"""Tests for extended type support: datetime, date, time, Decimal, UUID."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional
from uuid import UUID

import pytest

from cheap_settings import CheapSettings


class TestDateTimeTypes:
    """Test datetime, date, and time type support."""

    def test_datetime_from_env(self, monkeypatch):
        """Test datetime parsing from environment variable."""

        class Settings(CheapSettings):
            created_at: datetime = datetime(2024, 1, 1, 12, 0, 0)
            updated_at: datetime = datetime(2024, 1, 1)

        monkeypatch.setenv("CREATED_AT", "2024-12-25T15:30:45")
        monkeypatch.setenv("UPDATED_AT", "2024-12-31T23:59:59.999999")

        assert Settings.created_at == datetime(2024, 12, 25, 15, 30, 45)
        assert Settings.updated_at == datetime(2024, 12, 31, 23, 59, 59, 999999)

    def test_date_from_env(self, monkeypatch):
        """Test date parsing from environment variable."""

        class Settings(CheapSettings):
            start_date: date = date(2024, 1, 1)
            end_date: date = date(2024, 12, 31)

        monkeypatch.setenv("START_DATE", "2024-06-15")
        monkeypatch.setenv("END_DATE", "2025-01-01")

        assert Settings.start_date == date(2024, 6, 15)
        assert Settings.end_date == date(2025, 1, 1)

    def test_time_from_env(self, monkeypatch):
        """Test time parsing from environment variable."""

        class Settings(CheapSettings):
            backup_time: time = time(3, 0, 0)
            meeting_time: time = time(14, 30)

        monkeypatch.setenv("BACKUP_TIME", "02:30:00")
        monkeypatch.setenv("MEETING_TIME", "09:15:30.500000")

        assert Settings.backup_time == time(2, 30, 0)
        assert Settings.meeting_time == time(9, 15, 30, 500000)

    def test_datetime_with_timezone(self, monkeypatch):
        """Test datetime with timezone information."""

        class Settings(CheapSettings):
            scheduled_at: datetime = datetime(2024, 1, 1)

        # ISO format with timezone
        monkeypatch.setenv("SCHEDULED_AT", "2024-06-15T10:30:00+05:30")

        # This will parse the timezone-aware datetime
        dt = Settings.scheduled_at
        assert dt.year == 2024
        assert dt.month == 6
        assert dt.day == 15
        assert dt.hour == 10
        assert dt.minute == 30

    def test_invalid_datetime_format(self, monkeypatch):
        """Test that invalid datetime format raises error."""

        class Settings(CheapSettings):
            created_at: datetime = datetime(2024, 1, 1)

        monkeypatch.setenv("CREATED_AT", "not-a-datetime")

        with pytest.raises(ValueError):
            _ = Settings.created_at

    def test_invalid_date_format(self, monkeypatch):
        """Test that invalid date format raises error."""

        class Settings(CheapSettings):
            start_date: date = date(2024, 1, 1)

        monkeypatch.setenv("START_DATE", "2024/06/15")  # Wrong separator

        with pytest.raises(ValueError):
            _ = Settings.start_date

    def test_invalid_time_format(self, monkeypatch):
        """Test that invalid time format raises error."""

        class Settings(CheapSettings):
            backup_time: time = time(3, 0, 0)

        monkeypatch.setenv("BACKUP_TIME", "3:00 AM")  # Not ISO format

        with pytest.raises(ValueError):
            _ = Settings.backup_time


class TestDecimalType:
    """Test Decimal type support."""

    def test_decimal_from_env(self, monkeypatch):
        """Test Decimal parsing from environment variable."""

        class Settings(CheapSettings):
            price: Decimal = Decimal("19.99")
            tax_rate: Decimal = Decimal("0.0825")

        monkeypatch.setenv("PRICE", "29.95")
        monkeypatch.setenv("TAX_RATE", "0.0625")

        assert Settings.price == Decimal("29.95")
        assert Settings.tax_rate == Decimal("0.0625")

    def test_decimal_precision(self, monkeypatch):
        """Test that Decimal preserves precision."""

        class Settings(CheapSettings):
            bitcoin_amount: Decimal = Decimal("0.00000001")

        monkeypatch.setenv("BITCOIN_AMOUNT", "0.00012345678901234567890")

        # Decimal preserves all the precision
        assert str(Settings.bitcoin_amount) == "0.00012345678901234567890"

    def test_decimal_scientific_notation(self, monkeypatch):
        """Test Decimal with scientific notation."""

        class Settings(CheapSettings):
            small_value: Decimal = Decimal("1E-10")
            large_value: Decimal = Decimal("1E10")

        monkeypatch.setenv("SMALL_VALUE", "2.5E-8")
        monkeypatch.setenv("LARGE_VALUE", "3.14159E6")

        assert Settings.small_value == Decimal("2.5E-8")
        assert Settings.large_value == Decimal("3.14159E6")

    def test_decimal_invalid_format(self, monkeypatch):
        """Test that invalid decimal format raises error."""

        class Settings(CheapSettings):
            amount: Decimal = Decimal("0")

        monkeypatch.setenv("AMOUNT", "not-a-number")

        with pytest.raises(Exception):  # decimal.InvalidOperation
            _ = Settings.amount


class TestUUIDType:
    """Test UUID type support."""

    def test_uuid_from_env(self, monkeypatch):
        """Test UUID parsing from environment variable."""

        class Settings(CheapSettings):
            session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
            api_key: UUID = UUID("00000000-0000-0000-0000-000000000000")

        monkeypatch.setenv("SESSION_ID", "a8098c1a-f86e-11da-bd1a-00112444be1e")
        monkeypatch.setenv("API_KEY", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")

        assert Settings.session_id == UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
        assert Settings.api_key == UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

    def test_uuid_different_formats(self, monkeypatch):
        """Test UUID with different valid formats."""

        class Settings(CheapSettings):
            uuid1: UUID = UUID("00000000-0000-0000-0000-000000000000")
            uuid2: UUID = UUID("00000000-0000-0000-0000-000000000000")
            uuid3: UUID = UUID("00000000-0000-0000-0000-000000000000")

        # With hyphens (standard)
        monkeypatch.setenv("UUID1", "550e8400-e29b-41d4-a716-446655440000")
        # Without hyphens
        monkeypatch.setenv("UUID2", "550e8400e29b41d4a716446655440000")
        # With braces
        monkeypatch.setenv("UUID3", "{550e8400-e29b-41d4-a716-446655440000}")

        # pragma: allowlist nextline secret
        expected = UUID("550e8400-e29b-41d4-a716-446655440000")

        assert Settings.uuid1 == expected
        assert Settings.uuid2 == expected
        assert Settings.uuid3 == expected

    def test_uuid_invalid_format(self, monkeypatch):
        """Test that invalid UUID format raises error."""

        class Settings(CheapSettings):
            session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")

        monkeypatch.setenv("SESSION_ID", "not-a-uuid")

        with pytest.raises(ValueError):
            _ = Settings.session_id

    def test_uuid_case_insensitive(self, monkeypatch):
        """Test that UUID parsing is case-insensitive."""

        class Settings(CheapSettings):
            key: UUID = UUID("00000000-0000-0000-0000-000000000000")

        monkeypatch.setenv("KEY", "A8098C1A-F86E-11DA-BD1A-00112444BE1E")

        assert Settings.key == UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


class TestOptionalExtendedTypes:
    """Test Optional variants of extended types."""

    def test_optional_datetime(self, monkeypatch):
        """Test Optional[datetime] type support."""

        class Settings(CheapSettings):
            expires_at: Optional[datetime] = None

        # Test with None
        assert Settings.expires_at is None

        # Test with "none" string
        monkeypatch.setenv("EXPIRES_AT", "none")
        assert Settings.expires_at is None

        # Test with actual datetime
        monkeypatch.setenv("EXPIRES_AT", "2025-12-31T23:59:59")
        assert Settings.expires_at == datetime(2025, 12, 31, 23, 59, 59)

    def test_optional_date(self, monkeypatch):
        """Test Optional[date] type support."""

        class Settings(CheapSettings):
            deadline: Optional[date] = None

        monkeypatch.setenv("DEADLINE", "2025-06-30")
        assert Settings.deadline == date(2025, 6, 30)

        monkeypatch.setenv("DEADLINE", "none")
        assert Settings.deadline is None

    def test_optional_decimal(self, monkeypatch):
        """Test Optional[Decimal] type support."""

        class Settings(CheapSettings):
            discount: Optional[Decimal] = None

        monkeypatch.setenv("DISCOUNT", "15.50")
        assert Settings.discount == Decimal("15.50")

        monkeypatch.setenv("DISCOUNT", "none")
        assert Settings.discount is None

    def test_optional_uuid(self, monkeypatch):
        """Test Optional[UUID] type support."""

        class Settings(CheapSettings):
            tracking_id: Optional[UUID] = None

        monkeypatch.setenv("TRACKING_ID", "550e8400-e29b-41d4-a716-446655440000")
        assert Settings.tracking_id == UUID("550e8400-e29b-41d4-a716-446655440000")

        monkeypatch.setenv("TRACKING_ID", "none")
        assert Settings.tracking_id is None


class TestInferredExtendedTypes:
    """Test type inference for extended types without annotations."""

    def test_inferred_datetime(self, monkeypatch):
        """Test datetime type inference from default value."""

        class Settings(CheapSettings):
            # No type annotation, should infer from default
            created = datetime(2024, 1, 1, 12, 0, 0)

        monkeypatch.setenv("CREATED", "2024-07-04T16:30:00")
        assert Settings.created == datetime(2024, 7, 4, 16, 30, 0)

    def test_inferred_date(self, monkeypatch):
        """Test date type inference from default value."""

        class Settings(CheapSettings):
            start = date(2024, 1, 1)

        monkeypatch.setenv("START", "2024-03-15")
        assert Settings.start == date(2024, 3, 15)

    def test_inferred_decimal(self, monkeypatch):
        """Test Decimal type inference from default value."""

        class Settings(CheapSettings):
            rate = Decimal("3.14159")

        monkeypatch.setenv("RATE", "2.71828")
        assert Settings.rate == Decimal("2.71828")

    def test_inferred_uuid(self, monkeypatch):
        """Test UUID type inference from default value."""

        class Settings(CheapSettings):
            node_id = UUID("12345678-1234-5678-1234-567812345678")

        monkeypatch.setenv("NODE_ID", "abcdef12-3456-7890-abcd-ef1234567890")
        assert Settings.node_id == UUID("abcdef12-3456-7890-abcd-ef1234567890")


class TestCommandLineExtendedTypes:
    """Test extended types with command line arguments."""

    def test_datetime_from_cli(self):
        """Test datetime from command line arguments."""

        class Settings(CheapSettings):
            scheduled: datetime = datetime(2024, 1, 1)

        Settings.set_config_from_command_line(
            args=["--scheduled", "2024-08-15T14:30:00"]
        )

        assert Settings.scheduled == datetime(2024, 8, 15, 14, 30, 0)

    def test_decimal_from_cli(self):
        """Test Decimal from command line arguments."""

        class Settings(CheapSettings):
            amount: Decimal = Decimal("0.00")

        Settings.set_config_from_command_line(args=["--amount", "123.456789"])

        assert Settings.amount == Decimal("123.456789")

    def test_uuid_from_cli(self):
        """Test UUID from command line arguments."""

        class Settings(CheapSettings):
            request_id: UUID = UUID("00000000-0000-0000-0000-000000000000")

        Settings.set_config_from_command_line(
            args=["--request-id", "deadbeef-cafe-babe-0000-000000000000"]
        )

        assert Settings.request_id == UUID("deadbeef-cafe-babe-0000-000000000000")


class TestIntegration:
    """Integration tests with multiple extended types."""

    def test_financial_settings(self, monkeypatch):
        """Test a realistic financial settings configuration."""

        class FinancialSettings(CheapSettings):
            transaction_date: date = date.today()
            transaction_time: time = time(9, 0, 0)
            amount: Decimal = Decimal("0.00")
            tax_rate: Decimal = Decimal("0.08")
            transaction_id: UUID = UUID("00000000-0000-0000-0000-000000000000")
            processed_at: Optional[datetime] = None

        monkeypatch.setenv("TRANSACTION_DATE", "2024-12-25")
        monkeypatch.setenv("TRANSACTION_TIME", "14:35:22")
        monkeypatch.setenv("AMOUNT", "1999.99")
        monkeypatch.setenv("TAX_RATE", "0.0875")
        monkeypatch.setenv("TRANSACTION_ID", "a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        monkeypatch.setenv("PROCESSED_AT", "2024-12-25T14:35:22.123456")

        assert FinancialSettings.transaction_date == date(2024, 12, 25)
        assert FinancialSettings.transaction_time == time(14, 35, 22)
        assert FinancialSettings.amount == Decimal("1999.99")
        assert FinancialSettings.tax_rate == Decimal("0.0875")
        assert FinancialSettings.transaction_id == UUID(
            "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        )
        assert FinancialSettings.processed_at == datetime(
            2024, 12, 25, 14, 35, 22, 123456
        )

        # Calculate tax (using Decimal for precision)
        total_tax = FinancialSettings.amount * FinancialSettings.tax_rate
        assert total_tax == Decimal("174.999125")
