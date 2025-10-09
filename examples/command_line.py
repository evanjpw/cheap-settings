#!/usr/bin/env python3
"""Command line argument parsing with CheapSettings.

Shows how to automatically create command line arguments from your settings.
Command line arguments take precedence over environment variables.
"""

import os
import sys

from cheap_settings import CheapSettings


class ServerConfig(CheapSettings):
    """Server configuration with CLI support."""

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    log_level: str = "INFO"


def main():
    print("=== Command Line Configuration ===\n")

    # Show what happens without command line parsing
    print("Before parsing command line arguments:")
    print(f"  Host: {ServerConfig.host}")
    print(f"  Port: {ServerConfig.port}")
    print(f"  Workers: {ServerConfig.workers}")

    # Set an environment variable to show precedence
    os.environ["PORT"] = "9000"
    print("\nAfter setting PORT=9000 in environment:")
    print(f"  Port: {ServerConfig.port}")

    # Parse command line arguments
    # This automatically creates flags like --host, --port, --workers, etc.
    _args = ServerConfig.set_config_from_command_line()

    print("\nAfter parsing command line arguments:")
    print(f"  Host: {ServerConfig.host}")
    print(f"  Port: {ServerConfig.port}")
    print(f"  Workers: {ServerConfig.workers}")
    print(f"  Reload: {ServerConfig.reload}")
    print(f"  Log Level: {ServerConfig.log_level}")

    print("\n" + "=" * 50)
    print("Server Configuration Summary:")
    print(f"  Starting server at http://{ServerConfig.host}:{ServerConfig.port}")
    print(f"  Workers: {ServerConfig.workers}")
    print(f"  Auto-reload: {'enabled' if ServerConfig.reload else 'disabled'}")
    print(f"  Log level: {ServerConfig.log_level}")

    # Clean up
    if "PORT" in os.environ:
        del os.environ["PORT"]


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Try running with arguments:")
        print(
            f"  python {sys.argv[0]} --host localhost --port 3000 --workers 8 --reload"
        )
        print(f"  python {sys.argv[0]} --help")
        print("\nRunning with defaults...\n")

    main()
