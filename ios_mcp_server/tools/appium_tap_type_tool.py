"""
Appium tap and type tool for iOS automation.

This tool provides the main functionality for finding text fields,
tapping them, and typing text using real Appium automation.
"""

from typing import Dict, Any, List, Optional

try:
    from .base_tool import BaseTool, ToolArgument
    from ..automation.appium_client import AppiumClient
    from ..config.settings import settings
    from ..utils.exceptions import AutomationError
except ImportError:
    # Fallback for Claude Desktop context
    import sys
    import os
    
    # Add the ios_mcp_server to path if not already there
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    from tools.base_tool import BaseTool, ToolArgument
    from automation.appium_client import AppiumClient
    from config.settings import settings
    from utils.exceptions import AutomationError


class AppiumTapTypeTool(BaseTool):
    """
    Tool for tapping text fields and typing text using Appium automation.
    
    This is the main tool that replaces the old coordinate-based and
    AppleScript approaches with real iOS automation using Appium.
    """
    
    def __init__(self):
        """Initialize the Appium tap and type tool."""
        super().__init__()
        self.appium_client = AppiumClient()
    
    @property
    def name(self) -> str:
        """Return the tool name."""
        return "appium_tap_and_type"
    
    @property
    def description(self) -> str:
        """Return the tool description."""
        return (
            "Find a text field in the iOS app, tap it to focus, and type the specified text. "
            "This uses real Appium automation with multiple element finding strategies for reliability. "
            "Works with any iOS app that has text input fields."
        )
    
    @property
    def arguments(self) -> List[ToolArgument]:
        """Define the tool arguments."""
        return [
            ToolArgument(
                name="text",
                type="string",
                description="The text to type into the text field",
                required=True
            ),
            ToolArgument(
                name="app_bundle_id",
                type="string",
                description=f"iOS app bundle ID (defaults to {settings.ios.default_bundle_id})",
                required=False,
                default=settings.ios.default_bundle_id
            ),
            ToolArgument(
                name="timeout",
                type="number",
                description="Timeout in seconds for finding the text field (default: 10)",
                required=False,
                default=10
            )
        ]
    
    async def execute_impl(self, text: str, app_bundle_id: str = None, timeout: int = 10) -> Dict[str, Any]:
        """
        Execute the tap and type automation.
        
        Args:
            text: Text to type
            app_bundle_id: iOS app bundle identifier
            timeout: Element finding timeout in seconds
            
        Returns:
            Dictionary with automation results
            
        Raises:
            AutomationError: If automation fails
        """
        
        # Use default bundle ID if none provided
        if app_bundle_id is None:
            app_bundle_id = settings.ios.default_bundle_id
            
        self.logger.info(f"🎯 Starting Appium tap and type automation")
        self.logger.debug(f"📱 Target app: {app_bundle_id}")
        self.logger.debug(f"⌨️ Text to type: '{text}'")
        self.logger.debug(f"⏱️ Timeout: {timeout}s")
        
        try:
            # Start Appium session to verify connectivity
            await self.appium_client.start_session()
            
            # Execute the tap and type automation
            result = await self.appium_client.tap_and_type(
                text=text,
                app_bundle_id=app_bundle_id,
                timeout=timeout
            )
            
            self.logger.info(f"✅ Appium automation completed successfully")
            
            # Enhanced result with additional context
            return {
                "success": True,
                "message": result["message"],
                "text_typed": text,
                "app_bundle_id": result["app_bundle_id"],
                "screenshot_saved": result.get("screenshot_saved", False),
                "automation_method": "appium",
                "timeout_used": timeout,
                "details": "Text field found and typed successfully using Appium XCUITest automation"
            }
            
        except AutomationError as e:
            self.logger.error(f"❌ Appium automation failed: {e}")
            
            # Provide helpful error context
            error_context = {
                "text": text,
                "app_bundle_id": app_bundle_id,
                "timeout": timeout,
                "error_details": str(e),
                "suggestions": self._get_troubleshooting_suggestions(str(e))
            }
            
            return {
                "success": False,
                "error": str(e),
                "context": error_context,
                "automation_method": "appium"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in Appium automation: {e}")
            
            return {
                "success": False,
                "error": f"Unexpected automation error: {str(e)}",
                "context": {
                    "text": text,
                    "app_bundle_id": app_bundle_id,
                    "timeout": timeout,
                    "error_type": type(e).__name__
                },
                "automation_method": "appium"
            }
        
        finally:
            # Always clean up the session
            try:
                await self.appium_client.close_session()
            except:
                pass  # Don't let cleanup errors mask the main result
    
    def _get_troubleshooting_suggestions(self, error_message: str) -> List[str]:
        """
        Provide context-specific troubleshooting suggestions based on the error.
        
        Args:
            error_message: The error message from automation failure
            
        Returns:
            List of troubleshooting suggestions
        """
        
        suggestions = []
        error_lower = error_message.lower()
        
        # Connection-related errors
        if "connection" in error_lower or "refused" in error_lower:
            suggestions.extend([
                "Ensure Appium server is running: appium server --port 4723",
                "Check if localhost:4723 is accessible",
                "Restart Appium server if it's unresponsive"
            ])
        
        # Element finding errors
        elif "no text field" in error_lower or "element" in error_lower:
            suggestions.extend([
                "Make sure the target app is open and visible",
                "Verify the app has text input fields on the current screen",
                "Try increasing the timeout value",
                "Check if the app requires navigation to reach text fields"
            ])
        
        # App launch errors
        elif "bundle" in error_lower or "launch" in error_lower:
            suggestions.extend([
                "Verify the bundle ID is correct",
                "Ensure the app is installed on the simulator",
                "Check if the simulator is booted and accessible"
            ])
        
        # Import/dependency errors
        elif "import" in error_lower or "module" in error_lower:
            suggestions.extend([
                "Verify Appium Python client is installed in virtual environment",
                "Check virtual environment path in configuration",
                "Reinstall dependencies: pip install -r requirements.txt"
            ])
        
        # Simulator/device errors
        elif "simulator" in error_lower or "device" in error_lower:
            suggestions.extend([
                "Ensure iOS Simulator is running",
                "Check simulator device settings match configuration",
                "Try restarting the iOS Simulator"
            ])
        
        # Generic suggestions if no specific pattern matched
        if not suggestions:
            suggestions.extend([
                "Check Appium server logs for detailed error information",
                "Verify iOS Simulator is running and accessible",
                "Ensure the target app is open and has text input fields",
                "Try restarting both Appium server and iOS Simulator"
            ])
        
        return suggestions 