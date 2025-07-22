"""
Launch app tool for iOS automation.

This tool provides functionality for launching iOS applications on simulators
with proper error handling and process management.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add the ios_mcp_server directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from automation.simulator_manager import SimulatorManager
from config.settings import settings
from utils.exceptions import AppLaunchError


class LaunchAppTool:
    """
    Tool for launching iOS applications on simulators.
    
    This tool provides a clean interface for launching apps with proper
    error handling and process information.
    """
    
    def __init__(self):
        """Initialize the launch app tool."""
        self.simulator_manager = SimulatorManager()
    
    @property
    def name(self) -> str:
        """Return the tool name."""
        return "launch_app"
    
    @property
    def description(self) -> str:
        """Return the tool description."""
        return (
            "Launch an iOS application on the simulator using its bundle ID. "
            "This ensures the app is running and ready for automation. "
            "Provides process information and launch status."
        )
    
    @property
    def arguments(self) -> List[ToolArgument]:
        """Define the tool arguments."""
        return [
            ToolArgument(
                name="bundle_id",
                type="string",
                description="iOS app bundle identifier (e.g., com.apple.mobilesafari)",
                required=True
            ),
            ToolArgument(
                name="device_id",
                type="string",
                description="Simulator device ID (defaults to 'booted' for current active simulator)",
                required=False,
                default="booted"
            )
        ]
    
    async def execute_impl(self, bundle_id: str, device_id: str = "booted") -> Dict[str, Any]:
        """
        Execute the app launch.
        
        Args:
            bundle_id: iOS app bundle identifier
            device_id: Simulator device identifier
            
        Returns:
            Dictionary with launch information
            
        Raises:
            AppLaunchError: If app launch fails
        """
        
        self.logger.info(f"🚀 Launching app: {bundle_id}")
        self.logger.debug(f"📱 Target device: {device_id}")
        
        try:
            # Launch the app using the simulator manager
            result = await self.simulator_manager.launch_app(
                bundle_id=bundle_id,
                device_id=device_id
            )
            
            self.logger.info(f"✅ App launched successfully: {bundle_id}")
            
            # Return enhanced result with user-friendly information
            return {
                "success": True,
                "message": f"Successfully launched {bundle_id}",
                "bundle_id": result["bundle_id"],
                "device_id": result["device_id"],
                "process_info": result.get("process_info", "Process started"),
                "launch_output": result.get("output", ""),
                "details": f"App {bundle_id} is now running on simulator {device_id}"
            }
            
        except AppLaunchError as e:
            self.logger.error(f"❌ App launch failed: {e}")
            
            # Provide helpful error context
            error_context = {
                "bundle_id": bundle_id,
                "device_id": device_id,
                "error_details": str(e),
                "suggestions": self._get_troubleshooting_suggestions(str(e), bundle_id)
            }
            
            return {
                "success": False,
                "error": str(e),
                "context": error_context
            }
            
        except Exception as e:
            self.logger.error(f"❌ Unexpected error launching app: {e}")
            
            return {
                "success": False,
                "error": f"Unexpected launch error: {str(e)}",
                "context": {
                    "bundle_id": bundle_id,
                    "device_id": device_id,
                    "error_type": type(e).__name__
                }
            }
    
    def _get_troubleshooting_suggestions(self, error_message: str, bundle_id: str) -> List[str]:
        """
        Provide context-specific troubleshooting suggestions.
        
        Args:
            error_message: The error message from launch failure
            bundle_id: The app bundle ID that failed to launch
            
        Returns:
            List of troubleshooting suggestions
        """
        
        suggestions = []
        error_lower = error_message.lower()
        
        # App not found errors
        if "not found" in error_lower or "invalid" in error_lower:
            suggestions.extend([
                f"Verify that {bundle_id} is installed on the simulator",
                "Check if the bundle ID is spelled correctly",
                "Install the app on the simulator before launching",
                "Use 'xcrun simctl listapps booted' to see installed apps"
            ])
        
        # Simulator-related errors
        elif "simulator" in error_lower or "device" in error_lower:
            suggestions.extend([
                "Ensure the iOS Simulator is running and booted",
                "Check if the device ID is correct",
                "Try restarting the iOS Simulator",
                "Use 'xcrun simctl list devices' to see available simulators"
            ])
        
        # Permission or access errors
        elif "permission" in error_lower or "access" in error_lower:
            suggestions.extend([
                "Check if the app has proper permissions",
                "Ensure Xcode and simulators have necessary access rights",
                "Try running with elevated permissions if needed"
            ])
        
        # Process-related errors
        elif "process" in error_lower or "running" in error_lower:
            suggestions.extend([
                "Check if the app is already running",
                "Try terminating the app first if it's stuck",
                "Restart the simulator if processes are in bad state"
            ])
        
        # Generic suggestions based on common bundle IDs
        if "safari" in bundle_id.lower():
            suggestions.extend([
                "Safari should be pre-installed on iOS simulators",
                "Try using bundle ID: com.apple.mobilesafari"
            ])
        elif "settings" in bundle_id.lower():
            suggestions.extend([
                "Settings app should be available as: com.apple.Preferences"
            ])
        elif "com.apple" not in bundle_id.lower():
            suggestions.extend([
                "For third-party apps, ensure they are installed via Xcode or App Store",
                "Check if the app is compatible with the simulator iOS version"
            ])
        
        # Generic suggestions if no specific pattern matched
        if not suggestions:
            suggestions.extend([
                "Verify the app is installed on the target simulator",
                "Ensure the iOS Simulator is running and accessible",
                "Check if the bundle ID is correct and properly formatted",
                "Try launching a system app first to test simulator functionality"
            ])
        
        return suggestions 