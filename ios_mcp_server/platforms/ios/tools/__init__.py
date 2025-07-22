"""
iOS-specific MCP tools.

This package contains MCP tools specific to iOS automation using
XCUITest and iOS Simulator interactions:
- AppiumTapTypeTool: Advanced text input using Appium automation
- FindAndTapTool: Intelligent element finding and tapping
- LaunchAppTool: iOS application launching functionality  
- ScreenshotTool: iOS simulator screenshot capture
"""

from .appium_tap_type_tool import AppiumTapTypeTool
from .find_and_tap_tool import FindAndTapTool
from .launch_app_tool import LaunchAppTool
from .screenshot_tool import ScreenshotTool

__version__ = "2.0.0"
__all__ = [
    "AppiumTapTypeTool",
    "FindAndTapTool",
    "LaunchAppTool", 
    "ScreenshotTool"
]
