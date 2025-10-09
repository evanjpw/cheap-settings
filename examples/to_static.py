#!/usr/bin/env python3
"""Static snapshot demonstration with to_static().

Shows how to create a frozen, regular Python class from your settings
for performance-critical code or special use cases.
"""

import os
import time
from cheap_settings import CheapSettings


class DynamicSettings(CheapSettings):
    """Settings that respond to environment changes."""
    api_url: str = "https://api.example.com"
    timeout: int = 30
    retry_count: int = 3
    debug: bool = False


def measure_access_time(settings_class, name, iterations=100000):
    """Measure time to access a setting many times."""
    start = time.perf_counter()
    for _ in range(iterations):
        _ = settings_class.api_url
    elapsed = time.perf_counter() - start
    return elapsed


def main():
    print("=== Static Snapshot with to_static() ===\n")

    # Show initial values
    print("Initial Dynamic Settings:")
    print(f"  API URL: {DynamicSettings.api_url}")
    print(f"  Timeout: {DynamicSettings.timeout}")
    print(f"  Retry Count: {DynamicSettings.retry_count}")
    print(f"  Debug: {DynamicSettings.debug}")

    # Set environment variables
    print("\nSetting environment variables...")
    os.environ["API_URL"] = "https://prod.api.example.com"
    os.environ["TIMEOUT"] = "60"
    os.environ["DEBUG"] = "true"

    print("\nDynamic Settings (with environment):")
    print(f"  API URL: {DynamicSettings.api_url}")
    print(f"  Timeout: {DynamicSettings.timeout}")
    print(f"  Debug: {DynamicSettings.debug}")

    # Create a static snapshot
    print("\n" + "="*50)
    print("Creating static snapshot with to_static()...")
    print("="*50 + "\n")

    StaticSettings = DynamicSettings.to_static()

    print(f"Static Settings Class: {StaticSettings}")
    print(f"  Type: {type(StaticSettings)}")
    print(f"  Name: {StaticSettings.__name__}")

    print("\nStatic Settings Values (frozen at snapshot time):")
    print(f"  API URL: {StaticSettings.api_url}")
    print(f"  Timeout: {StaticSettings.timeout}")
    print(f"  Debug: {StaticSettings.debug}")

    # Change environment to show static doesn't change
    print("\nChanging environment variables again...")
    os.environ["API_URL"] = "https://changed.example.com"
    os.environ["TIMEOUT"] = "90"

    print("\nAfter environment change:")
    print("  Dynamic Settings (responds to change):")
    print(f"    API URL: {DynamicSettings.api_url}")
    print(f"    Timeout: {DynamicSettings.timeout}")

    print("  Static Settings (frozen, unchanged):")
    print(f"    API URL: {StaticSettings.api_url}")
    print(f"    Timeout: {StaticSettings.timeout}")

    # Performance comparison
    print("\n" + "="*50)
    print("Performance Comparison (100,000 accesses)")
    print("="*50 + "\n")

    dynamic_time = measure_access_time(DynamicSettings, "DynamicSettings")
    static_time = measure_access_time(StaticSettings, "StaticSettings")

    print(f"Dynamic Settings: {dynamic_time:.4f} seconds")
    print(f"Static Settings:  {static_time:.4f} seconds")

    if static_time < dynamic_time:
        speedup = (dynamic_time / static_time - 1) * 100
        print(f"Static is {speedup:.1f}% faster")
    else:
        print("Times are similar (both are very fast!)")

    print("\n=== Use Cases for to_static() ===")
    print("• Performance-critical tight loops")
    print("• Freezing configuration at startup")
    print("• Working around edge cases with dynamic behavior")
    print("• Creating serializable configuration objects")

    # Clean up
    for key in ["API_URL", "TIMEOUT", "DEBUG"]:
        if key in os.environ:
            del os.environ[key]


if __name__ == "__main__":
    main()