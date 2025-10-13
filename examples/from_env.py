#!/usr/bin/env python3
"""Example demonstrating the from_env() method."""

import os

from cheap_settings import CheapSettings


class AppSettings(CheapSettings):
    """Application settings with defaults."""

    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "myapp"
    db_user: str = "appuser"

    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8080

    # Feature flags
    debug_mode: bool = False
    enable_cache: bool = True


def main():
    """Demonstrate from_env() usage."""
    # Set some environment variables (in production these would come from your deployment)
    os.environ["DB_HOST"] = "prod-db.example.com"
    os.environ["DB_PORT"] = "5433"
    os.environ["SERVER_PORT"] = "443"
    os.environ["DEBUG_MODE"] = "false"

    print("=== Regular Settings (includes defaults) ===")
    print(f"DB Host: {AppSettings.db_host}")
    print(f"DB Port: {AppSettings.db_port}")
    print(f"DB Name: {AppSettings.db_name}")  # Default, not in env
    print(f"DB User: {AppSettings.db_user}")  # Default, not in env
    print(f"Server Host: {AppSettings.server_host}")  # Default, not in env
    print(f"Server Port: {AppSettings.server_port}")
    print(f"Debug Mode: {AppSettings.debug_mode}")
    print(f"Enable Cache: {AppSettings.enable_cache}")  # Default, not in env

    print("\n=== Environment-Only Settings (from_env) ===")
    EnvOnlySettings = AppSettings.from_env()

    # Show what's actually in the environment
    print(f"DB Host: {EnvOnlySettings.db_host}")
    print(f"DB Port: {EnvOnlySettings.db_port}")
    print(f"Server Port: {EnvOnlySettings.server_port}")
    print(f"Debug Mode: {EnvOnlySettings.debug_mode}")

    # These attributes don't exist because they weren't in env
    print(f"DB Name in env: {hasattr(EnvOnlySettings, 'db_name')}")
    print(f"DB User in env: {hasattr(EnvOnlySettings, 'db_user')}")
    print(f"Server Host in env: {hasattr(EnvOnlySettings, 'server_host')}")
    print(f"Enable Cache in env: {hasattr(EnvOnlySettings, 'enable_cache')}")

    print("\n=== Use Case: Debugging Deployment ===")
    print("Settings from environment only:")
    for attr_name in dir(EnvOnlySettings):
        if not attr_name.startswith("_"):
            print(f"  {attr_name} = {getattr(EnvOnlySettings, attr_name)}")

    print("\n=== Use Case: Validation ===")
    # Check that critical settings are in environment
    critical = ["db_host", "db_port", "server_port"]
    missing = [s for s in critical if not hasattr(EnvOnlySettings, s)]
    if missing:
        print(f"WARNING: Missing critical environment variables: {missing}")
    else:
        print("✓ All critical settings are configured via environment")


if __name__ == "__main__":
    main()
