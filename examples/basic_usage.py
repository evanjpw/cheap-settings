#!/usr/bin/env python3
"""Basic usage of CheapSettings.

This example shows the simplest way to use cheap-settings:
define a settings class with typed attributes and default values.
"""

from cheap_settings import CheapSettings


class AppSettings(CheapSettings):
    """Application configuration."""

    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    app_name: str = "MyApp"


def main():
    # Access settings directly as class attributes
    print("=== Basic Settings Access ===")
    print(f"Host: {AppSettings.host}")
    print(f"Port: {AppSettings.port}")
    print(f"Debug: {AppSettings.debug}")
    print(f"App Name: {AppSettings.app_name}")

    print(f"\nServer would run at: http://{AppSettings.host}:{AppSettings.port}")

    # Settings can be used anywhere in your code
    if AppSettings.debug:
        print("Debug mode is enabled")
    else:
        print("Debug mode is disabled")


if __name__ == "__main__":
    main()
    print("\nTip: Try setting environment variables before running:")
    print("  HOST=example.com PORT=3000 DEBUG=true python basic_usage.py")
