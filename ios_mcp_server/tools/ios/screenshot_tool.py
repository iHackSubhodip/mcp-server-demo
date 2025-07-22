"""
Screenshot tool for iOS automation.

This tool provides functionality for taking screenshots of iOS simulators
with proper error handling and file management.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add the ios_mcp_server directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from automation.screenshot_service import ScreenshotService
from shared.utils.exceptions import ScreenshotError


class ScreenshotTool:
    """
    Tool for taking screenshots of iOS simulators.
    
    This tool provides a clean interface for screenshot capture with proper
    error handling and file management.
    """
    
    def __init__(self):
        """Initialize the screenshot tool."""
        self.screenshot_service = ScreenshotService()
    
    @property
    def name(self) -> str:
        """Return the tool name."""
        return "take_screenshot"
    
    @property
    def description(self) -> str:
        """Return the tool description."""
        return (
            "Take a screenshot of the iOS simulator. "
            "Automatically generates timestamped filenames and saves to the current directory. "
            "Useful for capturing app state during automation workflows."
        )

    async def execute_impl(
        self, 
        filename: Optional[str] = None, 
        device_id: str = "booted",
        directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the screenshot capture.
        
        Args:
            filename: Custom filename (optional)
            device_id: Simulator device identifier
            directory: Save directory (optional)
            
        Returns:
            Dictionary with screenshot information
            
        Raises:
            ScreenshotError: If screenshot capture fails
        """
        
        self.logger.info(f"📸 Taking screenshot of device: {device_id}")
        if filename:
            self.logger.debug(f"📁 Custom filename: {filename}")
        if directory:
            self.logger.debug(f"📂 Custom directory: {directory}")
        
        try:
            # Take the screenshot using the service
            result = await self.screenshot_service.take_screenshot(
                filename=filename,
                device_id=device_id,
                directory=directory
            )
            
            self.logger.info(f"✅ Screenshot captured successfully: {result['filename']}")
            
            # Return enhanced result with user-friendly information
            return {
                "success": True,
                "message": f"Screenshot saved as {result['filename']}",
                "filename": result["filename"],
                "path": result["path"],
                "size_bytes": result["size_bytes"],
                "size_mb": round(result["size_bytes"] / (1024 * 1024), 2),
                "device_id": result["device_id"],
                "timestamp": result["timestamp"],
                "details": f"Screenshot captured from iOS simulator ({result['size_bytes']:,} bytes)"
            }
            
        except ScreenshotError as e:
            self.logger.error(f"❌ Screenshot capture failed: {e}")
            
            # Provide helpful error context
            error_context = {
                "device_id": device_id,
                "filename": filename,
                "directory": directory,
                "error_details": str(e),
                "suggestions": self._get_troubleshooting_suggestions(str(e))
            }
            
            return {
                "success": False,
                "error": str(e),
                "context": error_context
            }
            
        except Exception as e:
            self.logger.error(f"❌ Unexpected error taking screenshot: {e}")
            
            return {
                "success": False,
                "error": f"Unexpected screenshot error: {str(e)}",
                "context": {
                    "device_id": device_id,
                    "filename": filename,
                    "directory": directory,
                    "error_type": type(e).__name__
                }
            }
    
    def _get_troubleshooting_suggestions(self, error_message: str) -> List[str]:
        """
        Provide context-specific troubleshooting suggestions.
        
        Args:
            error_message: The error message from screenshot failure
            
        Returns:
            List of troubleshooting suggestions
        """
        
        suggestions = []
        error_lower = error_message.lower()
        
        # Simulator-related errors
        if "simulator" in error_lower or "device" in error_lower:
            suggestions.extend([
                "Ensure iOS Simulator is running and visible",
                "Check if the device ID is correct (use 'booted' for active simulator)",
                "Try restarting the iOS Simulator",
                "Verify Xcode command line tools are installed"
            ])
        
        # File system errors
        elif "permission" in error_lower or "access" in error_lower:
            suggestions.extend([
                "Check write permissions for the target directory",
                "Ensure the directory exists or can be created",
                "Try using a different save directory"
            ])
        
        # Path-related errors
        elif "path" in error_lower or "directory" in error_lower:
            suggestions.extend([
                "Verify the directory path is valid",
                "Check if the directory exists",
                "Use absolute paths to avoid ambiguity"
            ])
        
        # Command execution errors
        elif "xcrun" in error_lower or "simctl" in error_lower:
            suggestions.extend([
                "Ensure Xcode is properly installed",
                "Verify Xcode command line tools are available",
                "Try running 'xcrun simctl list devices' to test simulator access"
            ])
        
        # Generic suggestions
        if not suggestions:
            suggestions.extend([
                "Ensure iOS Simulator is running and accessible",
                "Check if Xcode and command line tools are properly installed",
                "Verify write permissions for the save directory",
                "Try using default parameters (no custom filename or directory)"
            ])
        
        return suggestions 