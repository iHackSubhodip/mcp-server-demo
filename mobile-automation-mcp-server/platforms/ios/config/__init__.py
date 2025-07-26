"""
iOS-specific configuration module.

This package contains configuration classes specific to iOS automation
using XCUITest and iOS Simulator/Device interactions.
"""

from .ios_settings import (
    iOSConfig,
    create_ios_config
)

__version__ = "2.0.0"
__all__ = [
    "iOSConfig",
    "create_ios_config"
]
