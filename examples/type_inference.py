#!/usr/bin/env python3
"""Type inference demonstration.

Shows how cheap-settings can infer types from default values,
making type annotations optional for simple cases.
"""

import os
from pathlib import Path

from cheap_settings import CheapSettings


class InferredSettings(CheapSettings):
    """Settings without explicit type annotations - types are inferred!"""

    # String inference
    host = "localhost"
    database_name = "myapp"

    # Integer inference
    port = 8080
    max_connections = 100
    retry_count = 3

    # Float inference
    timeout = 30.5
    rate_limit = 0.95

    # Boolean inference
    debug = False
    use_cache = True

    # Path inference
    config_dir = Path("/etc/myapp")
    log_file = Path("/var/log/app.log")


class MixedSettings(CheapSettings):
    """Mix explicit annotations with inferred types as needed."""

    # Inferred types for simple cases
    app_name = "MyApplication"
    worker_count = 4
    enable_metrics = True

    # Explicit annotations when you need them
    # (like for Optional types or to document intent)
    from typing import Optional

    api_key: Optional[str] = None
    custom_headers: dict = {}
    allowed_hosts: list = ["localhost", "127.0.0.1"]


def main():
    print("=== Type Inference Example ===\n")

    print("Settings with inferred types:")
    print(
        f"  Host: {InferredSettings.host} (type: {type(InferredSettings.host).__name__})"
    )
    print(
        f"  Port: {InferredSettings.port} (type: {type(InferredSettings.port).__name__})"
    )
    print(
        f"  Timeout: {InferredSettings.timeout} (type: {type(InferredSettings.timeout).__name__})"
    )
    print(
        f"  Debug: {InferredSettings.debug} (type: {type(InferredSettings.debug).__name__})"
    )
    print(
        f"  Config Dir: {InferredSettings.config_dir} (type: {type(InferredSettings.config_dir).__name__})"
    )

    # Set some environment variables
    print("\n=== Testing Environment Variable Override ===")
    os.environ["HOST"] = "production.example.com"
    os.environ["PORT"] = "443"  # Will be converted to int
    os.environ["TIMEOUT"] = "60.0"  # Will be converted to float
    os.environ["DEBUG"] = "true"  # Will be converted to bool
    os.environ["CONFIG_DIR"] = "/opt/myapp/config"  # Will be converted to Path

    print("\nAfter setting environment variables:")
    print(f"  Host: {InferredSettings.host}")
    print(
        f"  Port: {InferredSettings.port} (still an {type(InferredSettings.port).__name__}!)"
    )
    print(
        f"  Timeout: {InferredSettings.timeout} (still a {type(InferredSettings.timeout).__name__}!)"
    )
    print(
        f"  Debug: {InferredSettings.debug} (still a {type(InferredSettings.debug).__name__}!)"
    )
    print(
        f"  Config Dir: {InferredSettings.config_dir} (still a {type(InferredSettings.config_dir).__name__}!)"
    )

    print("\n=== Benefits of Type Inference ===")
    print("✓ Less typing - no redundant type annotations")
    print("✓ Still get automatic type conversion from environment variables")
    print("✓ Works with command line arguments")
    print("✓ Mix and match with explicit annotations as needed")
    print("✓ The type is obvious from the default value")

    # Clean up
    for key in ["HOST", "PORT", "TIMEOUT", "DEBUG", "CONFIG_DIR"]:
        if key in os.environ:
            del os.environ[key]


if __name__ == "__main__":
    main()
