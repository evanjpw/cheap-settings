#!/usr/bin/env python3
"""Extended type support in CheapSettings.

Demonstrates usage of datetime, date, time, Decimal, and UUID types.
These types are automatically converted from environment variable strings.
"""

import os
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional
from uuid import UUID

from cheap_settings import CheapSettings


class ApplicationConfig(CheapSettings):
    """Application configuration with various extended types."""

    # Date and time types
    launch_date: date = date(2024, 1, 1)
    daily_backup_time: time = time(3, 0, 0)  # 3:00 AM
    last_updated: datetime = datetime(2024, 1, 1, 0, 0, 0)

    # Financial types with Decimal for precision
    product_price: Decimal = Decimal("99.99")
    tax_rate: Decimal = Decimal("0.0825")  # 8.25%
    minimum_balance: Decimal = Decimal("0.01")

    # Unique identifiers
    instance_id: UUID = UUID("00000000-0000-0000-0000-000000000000")
    api_key: UUID = UUID("12345678-1234-5678-1234-567812345678")

    # Optional types
    expires_at: Optional[datetime] = None
    promo_discount: Optional[Decimal] = None


def main():
    print("=== Extended Types Configuration ===\n")

    # Show defaults
    print("Default configuration:")
    print(f"  Launch date: {ApplicationConfig.launch_date}")
    print(f"  Backup time: {ApplicationConfig.daily_backup_time}")
    print(f"  Product price: ${ApplicationConfig.product_price}")
    print(f"  Tax rate: {ApplicationConfig.tax_rate * 100}%")
    print(f"  Instance ID: {ApplicationConfig.instance_id}")
    print(f"  Expires at: {ApplicationConfig.expires_at}")
    print()

    # Set some environment variables
    print("Setting environment variables...")
    os.environ["LAUNCH_DATE"] = "2025-01-01"
    os.environ["DAILY_BACKUP_TIME"] = "02:30:00"
    os.environ["LAST_UPDATED"] = "2024-12-25T15:30:45.123456"
    os.environ["PRODUCT_PRICE"] = "149.99"
    os.environ["TAX_RATE"] = "0.0925"  # 9.25%
    os.environ["INSTANCE_ID"] = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    os.environ["API_KEY"] = "{550e8400-e29b-41d4-a716-446655440000}"  # UUID with braces
    os.environ["EXPIRES_AT"] = "2025-12-31T23:59:59"
    os.environ["PROMO_DISCOUNT"] = "0.15"  # 15% off
    print()

    # Show updated configuration
    print("Configuration after environment variables:")
    print(f"  Launch date: {ApplicationConfig.launch_date}")
    print(f"  Backup time: {ApplicationConfig.daily_backup_time}")
    print(f"  Last updated: {ApplicationConfig.last_updated}")
    print(f"  Product price: ${ApplicationConfig.product_price}")
    print(f"  Tax rate: {ApplicationConfig.tax_rate * 100}%")
    print(f"  Instance ID: {ApplicationConfig.instance_id}")
    print(f"  API key: {ApplicationConfig.api_key}")
    print(f"  Expires at: {ApplicationConfig.expires_at}")
    print(
        f"  Promo discount: {ApplicationConfig.promo_discount * 100}%"
        if ApplicationConfig.promo_discount
        else "  Promo discount: None"
    )
    print()

    # Demonstrate Decimal precision
    print("=== Decimal Precision Example ===")
    print(f"Product price: ${ApplicationConfig.product_price}")
    print(f"Tax rate: {ApplicationConfig.tax_rate}")
    tax_amount = ApplicationConfig.product_price * ApplicationConfig.tax_rate
    print(f"Tax amount: ${tax_amount}")
    print(f"Total: ${ApplicationConfig.product_price + tax_amount}")

    if ApplicationConfig.promo_discount:
        discount = ApplicationConfig.product_price * ApplicationConfig.promo_discount
        print(f"Promo discount: ${discount}")
        final_price = ApplicationConfig.product_price - discount + tax_amount
        print(f"Final price: ${final_price}")
    print()

    # Demonstrate datetime calculations
    print("=== Date/Time Calculations ===")
    if ApplicationConfig.expires_at:
        now = datetime.now()
        time_remaining = ApplicationConfig.expires_at - now
        print(f"Time until expiration: {time_remaining.days} days")

    days_since_launch = (date.today() - ApplicationConfig.launch_date).days
    print(f"Days since launch: {days_since_launch}")
    print()

    # Parse command line arguments for these types
    print("=== Command Line Support ===")
    print("These types also work with command line arguments:")
    print("python app.py --launch-date 2025-06-01 --product-price 199.99")
    print("python app.py --instance-id deadbeef-cafe-babe-0000-000000000000")
    print("python app.py --expires-at 2025-12-31T23:59:59")

    # Clean up
    for key in [
        "LAUNCH_DATE",
        "DAILY_BACKUP_TIME",
        "LAST_UPDATED",
        "PRODUCT_PRICE",
        "TAX_RATE",
        "INSTANCE_ID",
        "API_KEY",
        "EXPIRES_AT",
        "PROMO_DISCOUNT",
    ]:
        if key in os.environ:
            del os.environ[key]


if __name__ == "__main__":
    main()
