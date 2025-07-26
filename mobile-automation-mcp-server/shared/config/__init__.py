"""
Shared configuration module for cross-platform MCP automation.

This package contains configuration classes and utilities that can be
shared across iOS, Android, and other automation platforms.
"""

from .base_settings import (
    AppiumConfig,
    ServerConfig,
    create_appium_config,
    create_server_config
)

__version__ = "2.0.0"
__all__ = [
    "AppiumConfig",
    "ServerConfig", 
    "create_appium_config",
    "create_server_config"
]
