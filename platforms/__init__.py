"""
Platform-specific automation modules.

This package contains platform-specific implementations for different
mobile automation platforms (iOS, Android, etc.).

Each platform follows the same structure:
- automation/: Core automation services (screenshot, app management, etc.)
- tools/: MCP tools specific to that platform
- config/: Platform-specific configuration and exceptions
"""

__version__ = "2.0.0"
__all__ = ["ios"]  # Will expand to include "android" in the future 