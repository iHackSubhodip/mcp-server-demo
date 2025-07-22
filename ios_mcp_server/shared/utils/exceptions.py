"""
Shared exception classes for cross-platform MCP automation.

This module defines a hierarchy of exceptions that provide clear,
actionable error information for iOS, Android, and other platforms.
"""

from typing import Optional, Dict, Any


class AutomationMCPError(Exception):
    """
    Base exception class for all MCP automation errors.
    
    This provides a common interface for all custom exceptions
    and includes helpful context information across platforms.
    """
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize the exception with message and optional context.
        
        Args:
            message: Human-readable error description
            context: Additional context information for debugging
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        """Return formatted error message with context."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (Context: {context_str})"
        return self.message


class AppiumConnectionError(AutomationMCPError):
    """
    Raised when unable to connect to or communicate with Appium server.
    
    This typically indicates:
    - Appium server is not running
    - Network connectivity issues
    - Incorrect server configuration
    """
    pass


class SimulatorError(AutomationMCPError):
    """
    Raised when iOS Simulator operations fail.
    
    This can indicate:
    - Simulator not found or not booted
    - Simulator in invalid state
    - Xcode/simulator tools not available
    """
    pass


class AppLaunchError(AutomationMCPError):
    """
    Raised when app launch operations fail.
    
    Common causes:
    - App not installed on simulator
    - Invalid bundle ID
    - App crashed during launch
    """
    pass


class AutomationError(AutomationMCPError):
    """
    Raised when UI automation operations fail.
    
    This covers:
    - Element not found
    - Interaction failures (tap, type, etc.)
    - Timeout waiting for elements
    """
    pass


class ScreenshotError(AutomationMCPError):
    """
    Raised when screenshot operations fail.
    
    Possible causes:
    - Simulator not accessible
    - File system permission issues
    - Invalid save path
    """
    pass


class ToolExecutionError(AutomationMCPError):
    """
    Raised when MCP tool execution fails.
    
    This is a wrapper for tool-specific errors that provides
    consistent error handling across all tools.
    """
    
    def __init__(self, tool_name: str, message: str, original_error: Optional[Exception] = None):
        """
        Initialize tool execution error.
        
        Args:
            tool_name: Name of the tool that failed
            message: Error description
            original_error: The original exception that caused this error
        """
        context = {"tool_name": tool_name}
        if original_error:
            context["original_error"] = str(original_error)
            context["error_type"] = type(original_error).__name__
        
        super().__init__(message, context)
        self.tool_name = tool_name
        self.original_error = original_error


class ConfigurationError(AutomationMCPError):
    """
    Raised when configuration is invalid or missing.
    
    This helps identify setup and configuration issues early.
    """
    pass


class ValidationError(AutomationMCPError):
    """
    Raised when input validation fails.
    
    This covers:
    - Invalid tool arguments
    - Missing required parameters
    - Parameter type mismatches
    """
    pass 