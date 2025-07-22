"""
Shared utilities for cross-platform MCP automation.

This package provides platform-agnostic utilities that can be used
by iOS, Android, and other automation platforms.

Modules:
- logger: Colored logging with emojis for better terminal output
- exceptions: Exception hierarchy for consistent error handling
- command_runner: Safe shell command execution with timeout support
"""

from .logger import get_logger, ColoredFormatter
from .exceptions import (
    AutomationMCPError,
    AppiumConnectionError, 
    SimulatorError,
    AppLaunchError,
    AutomationError,
    ScreenshotError,
    ToolExecutionError,
    ConfigurationError,
    ValidationError
)
from .command_runner import CommandRunner, CommandResult, run_command

__version__ = "2.0.0"
__all__ = [
    # Logger
    "get_logger",
    "ColoredFormatter",
    
    # Exceptions
    "AutomationMCPError",
    "AppiumConnectionError",
    "SimulatorError", 
    "AppLaunchError",
    "AutomationError",
    "ScreenshotError",
    "ToolExecutionError",
    "ConfigurationError",
    "ValidationError",
    
    # Command Runner
    "CommandRunner",
    "CommandResult", 
    "run_command"
]
