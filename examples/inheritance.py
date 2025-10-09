#!/usr/bin/env python3
"""Settings inheritance demonstration.

Shows how settings classes can inherit from each other,
allowing you to build hierarchies of configuration.
"""

from cheap_settings import CheapSettings


class BaseConfig(CheapSettings):
    """Base configuration with common settings."""

    app_name: str = "MyApplication"
    version: str = "1.0.0"
    timeout: int = 30


class DatabaseConfig(BaseConfig):
    """Database configuration, inheriting base settings."""

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "myapp"


class DevelopmentConfig(DatabaseConfig):
    """Development environment configuration."""

    debug: bool = True
    db_name: str = "myapp_dev"  # Override parent setting
    hot_reload: bool = True


class ProductionConfig(DatabaseConfig):
    """Production environment configuration."""

    debug: bool = False
    db_host: str = "prod.db.example.com"  # Override parent setting
    db_name: str = "myapp_prod"  # Override parent setting
    ssl_required: bool = True


def show_config(config_class, env_name):
    """Display configuration for a given environment."""
    print(f"\n=== {env_name} Configuration ===")
    print(f"App Name: {config_class.app_name} (from BaseConfig)")
    print(f"Version: {config_class.version} (from BaseConfig)")
    print(f"Timeout: {config_class.timeout}s (from BaseConfig)")
    print(f"Database Host: {config_class.db_host}")
    print(f"Database Port: {config_class.db_port}")
    print(f"Database Name: {config_class.db_name}")

    # Check for environment-specific settings
    if hasattr(config_class, "debug"):
        print(f"Debug Mode: {config_class.debug}")
    if hasattr(config_class, "hot_reload"):
        print(f"Hot Reload: {config_class.hot_reload}")
    if hasattr(config_class, "ssl_required"):
        print(f"SSL Required: {config_class.ssl_required}")


def main():
    print("=== Settings Inheritance Example ===")
    print("\nThis example shows how settings can be inherited and overridden")
    print("in a hierarchy of configuration classes.")

    # Show the base configuration
    show_config(BaseConfig, "Base")

    # Show database configuration (inherits from Base)
    show_config(DatabaseConfig, "Database")

    # Show development configuration (inherits from Database -> Base)
    show_config(DevelopmentConfig, "Development")

    # Show production configuration (inherits from Database -> Base)
    show_config(ProductionConfig, "Production")

    print("\n=== Key Points ===")
    print("• Child classes inherit all settings from parents")
    print("• Child classes can override parent settings")
    print("• Child classes can add new settings")
    print("• Environment variables work with all inherited settings")


if __name__ == "__main__":
    main()
