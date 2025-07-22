"""
iOS automation services.

This package contains the core automation services for iOS platform:
- AppiumClient: Handles Appium automation connections and script execution
- ScreenshotService: Manages iOS simulator screenshot capture
- SimulatorManager: Manages iOS simulator and application lifecycle
"""

from .appium_client import AppiumClient
from .screenshot_service import ScreenshotService
from .simulator_manager import SimulatorManager

__version__ = "2.0.0"
__all__ = [
    "AppiumClient",
    "ScreenshotService", 
    "SimulatorManager"
]
