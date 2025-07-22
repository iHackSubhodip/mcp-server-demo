"""
iOS-specific automation platform.

This package contains all iOS-specific automation functionality including
Appium integration, iOS Simulator management, and iOS-specific MCP tools.

Structure:
- automation/: iOS automation services (screenshot, appium client, simulator manager)
- tools/: iOS-specific MCP tools (tap, type, launch app, etc.)
- config/: iOS-specific configuration and exceptions
"""

__version__ = "2.0.0"
__all__ = ["automation", "tools", "config"]
