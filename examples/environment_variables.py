#!/usr/bin/env python3
"""Environment variable override demonstration.

Shows how environment variables automatically override default values
with proper type conversion.
"""

import os

from cheap_settings import CheapSettings


class Settings(CheapSettings):
    """Settings that can be overridden by environment variables."""

    database_host: str = "localhost"
    database_port: int = 5432
    connection_timeout: float = 30.0
    use_ssl: bool = False
    max_connections: int = 10


def main():
    print("=== Default Settings ===")
    print(f"Database Host: {Settings.database_host}")
    print(f"Database Port: {Settings.database_port}")
    print(f"Connection Timeout: {Settings.connection_timeout}s")
    print(f"Use SSL: {Settings.use_ssl}")
    print(f"Max Connections: {Settings.max_connections}")

    # Now let's set some environment variables
    print("\n=== Setting Environment Variables ===")
    os.environ["DATABASE_HOST"] = "prod.example.com"
    os.environ["DATABASE_PORT"] = "3306"  # Will be converted to int
    os.environ["CONNECTION_TIMEOUT"] = "45.5"  # Will be converted to float
    os.environ["USE_SSL"] = "true"  # Will be converted to bool
    os.environ["MAX_CONNECTIONS"] = "50"  # Will be converted to int

    print("Environment variables set!")

    print("\n=== Settings After Environment Variables ===")
    print(f"Database Host: {Settings.database_host}")
    print(
        f"Database Port: {Settings.database_port} (type: {type(Settings.database_port).__name__})"
    )
    print(
        f"Connection Timeout: {Settings.connection_timeout}s (type: {type(Settings.connection_timeout).__name__})"
    )
    print(f"Use SSL: {Settings.use_ssl} (type: {type(Settings.use_ssl).__name__})")
    print(
        f"Max Connections: {Settings.max_connections} (type: {type(Settings.max_connections).__name__})"
    )

    # Clean up
    print("\n=== Cleaning Up Environment Variables ===")
    for key in [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "CONNECTION_TIMEOUT",
        "USE_SSL",
        "MAX_CONNECTIONS",
    ]:
        if key in os.environ:
            del os.environ[key]

    print("Environment variables removed")
    print(f"Database Host is back to: {Settings.database_host}")


if __name__ == "__main__":
    main()
