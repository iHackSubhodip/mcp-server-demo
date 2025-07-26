"""
Main configuration module for Mobile automation iOS MCP server.

This module provides the unified configuration interface that combines
shared and platform-specific configurations.
"""

from .settings import settings, Settings

__version__ = "2.0.0"
__all__ = ["settings", "Settings"]
