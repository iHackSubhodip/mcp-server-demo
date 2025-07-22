"""
iOS Simulator manager for automation.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.utils.command_runner import run_command
from shared.utils.logger import get_logger
from shared.utils.exceptions import SimulatorError, AppLaunchError

logger = get_logger(__name__)


class SimulatorManager:
    """
    Service for managing iOS simulators and applications.
    
    This class follows the Single Responsibility Principle by focusing
    solely on simulator-related operations.
    """
    
    def __init__(self):
        """Initialize the simulator manager."""
        self.logger = get_logger(__name__)
    
    async def list_simulators(self) -> Dict[str, Any]:
        """
        List all available iOS simulators with their status.
        
        Returns:
            Dictionary containing simulator information in JSON format
            
        Raises:
            SimulatorError: If unable to list simulators
        """
        self.logger.info("📱 Listing available iOS simulators")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "list", "devices", "--json"])
            
            if success:
                # Parse JSON output to validate it
                simulator_data = json.loads(output)
                self.logger.info("✅ Successfully retrieved simulator list")
                self.logger.debug(f"🔍 Found {len(simulator_data.get('devices', {}))} device categories")
                return simulator_data
            else:
                raise SimulatorError(
                    "Failed to list iOS simulators",
                    context={"command_output": output}
                )
                
        except json.JSONDecodeError as e:
            raise SimulatorError(
                "Invalid JSON response from simctl list command",
                context={"parse_error": str(e), "output": output[:500]}
            )
        except Exception as e:
            raise SimulatorError(
                f"Unexpected error listing simulators: {str(e)}",
                context={"error_type": type(e).__name__}
            )
    
    async def boot_simulator(self, device_id: str) -> bool:
        """
        Boot a specific iOS simulator.
        
        Args:
            device_id: The UDID of the simulator to boot
            
        Returns:
            True if simulator was booted successfully
            
        Raises:
            SimulatorError: If unable to boot the simulator
        """
        if not device_id:
            raise SimulatorError("Device ID cannot be empty")
        
        self.logger.info(f"🚀 Booting iOS simulator: {device_id}")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "boot", device_id])
            
            if success:
                self.logger.info(f"✅ Successfully booted simulator: {device_id}")
                return True
            else:
                # Check if simulator is already booted (this is not an error)
                if "Unable to boot device in current state: Booted" in output:
                    self.logger.info(f"📱 Simulator already booted: {device_id}")
                    return True
                
                raise SimulatorError(
                    f"Failed to boot simulator {device_id}",
                    context={
                        "device_id": device_id,
                        "command_output": output,
                        "suggestion": "Check if device ID is valid and Xcode is properly installed"
                    }
                )
                
        except Exception as e:
            if isinstance(e, SimulatorError):
                raise
            
            raise SimulatorError(
                f"Unexpected error booting simulator {device_id}: {str(e)}",
                context={"device_id": device_id, "error_type": type(e).__name__}
            )
    
    async def shutdown_simulator(self, device_id: str) -> bool:
        """
        Shutdown a specific iOS simulator.
        
        Args:
            device_id: The UDID of the simulator to shutdown
            
        Returns:
            True if simulator was shutdown successfully
            
        Raises:
            SimulatorError: If unable to shutdown the simulator
        """
        if not device_id:
            raise SimulatorError("Device ID cannot be empty")
        
        self.logger.info(f"🛑 Shutting down iOS simulator: {device_id}")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "shutdown", device_id])
            
            if success:
                self.logger.info(f"✅ Successfully shutdown simulator: {device_id}")
                return True
            else:
                # Check if simulator is already shutdown (this is not an error)
                if "Unable to shutdown device in current state: Shutdown" in output:
                    self.logger.info(f"📱 Simulator already shutdown: {device_id}")
                    return True
                
                raise SimulatorError(
                    f"Failed to shutdown simulator {device_id}",
                    context={
                        "device_id": device_id,
                        "command_output": output
                    }
                )
                
        except Exception as e:
            if isinstance(e, SimulatorError):
                raise
            
            raise SimulatorError(
                f"Unexpected error shutting down simulator {device_id}: {str(e)}",
                context={"device_id": device_id, "error_type": type(e).__name__}
            )
    
    async def launch_app(self, bundle_id: str, device_id: str = "booted") -> Dict[str, Any]:
        """
        Launch an application on the specified simulator.
        
        Args:
            bundle_id: The bundle identifier of the app to launch
            device_id: The simulator UDID (defaults to "booted")
            
        Returns:
            Dictionary with launch result and process information
            
        Raises:
            AppLaunchError: If unable to launch the application
        """
        if not bundle_id:
            raise AppLaunchError("Bundle ID cannot be empty")
        
        self.logger.info(f"🚀 Launching app '{bundle_id}' on device: {device_id}")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "launch", device_id, bundle_id])
            
            if success:
                self.logger.info(f"✅ Successfully launched app: {bundle_id}")
                
                # Parse process information from output if available
                result = {
                    "success": True,
                    "bundle_id": bundle_id,
                    "device_id": device_id,
                    "output": output.strip()
                }
                
                # Extract process ID if present in output
                lines = output.strip().split('\n')
                for line in lines:
                    if ':' in line and 'process' in line.lower():
                        result["process_info"] = line.strip()
                        break
                
                return result
            else:
                raise AppLaunchError(
                    f"Failed to launch app {bundle_id}",
                    context={
                        "bundle_id": bundle_id,
                        "device_id": device_id,
                        "command_output": output,
                        "suggestions": [
                            "Check if app is installed on simulator",
                            "Verify bundle ID is correct",
                            "Ensure simulator is booted"
                        ]
                    }
                )
                
        except Exception as e:
            if isinstance(e, AppLaunchError):
                raise
            
            raise AppLaunchError(
                f"Unexpected error launching app {bundle_id}: {str(e)}",
                context={
                    "bundle_id": bundle_id,
                    "device_id": device_id,
                    "error_type": type(e).__name__
                }
            )
    
    async def terminate_app(self, bundle_id: str, device_id: str = "booted") -> bool:
        """
        Terminate a running application on the specified simulator.
        
        Args:
            bundle_id: The bundle identifier of the app to terminate
            device_id: The simulator UDID (defaults to "booted")
            
        Returns:
            True if app was terminated successfully
            
        Raises:
            AppLaunchError: If unable to terminate the application
        """
        if not bundle_id:
            raise AppLaunchError("Bundle ID cannot be empty")
        
        self.logger.info(f"🛑 Terminating app '{bundle_id}' on device: {device_id}")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "terminate", device_id, bundle_id])
            
            if success:
                self.logger.info(f"✅ Successfully terminated app: {bundle_id}")
                return True
            else:
                # Check if app was not running (this might not be an error)
                if "not running" in output.lower() or "no such process" in output.lower():
                    self.logger.info(f"📱 App was not running: {bundle_id}")
                    return True
                
                raise AppLaunchError(
                    f"Failed to terminate app {bundle_id}",
                    context={
                        "bundle_id": bundle_id,
                        "device_id": device_id,
                        "command_output": output
                    }
                )
                
        except Exception as e:
            if isinstance(e, AppLaunchError):
                raise
            
            raise AppLaunchError(
                f"Unexpected error terminating app {bundle_id}: {str(e)}",
                context={
                    "bundle_id": bundle_id,
                    "device_id": device_id,
                    "error_type": type(e).__name__
                }
            )
    
    async def list_installed_apps(self, device_id: str = "booted") -> List[Dict[str, Any]]:
        """
        List all installed applications on the specified simulator.
        
        Args:
            device_id: The simulator UDID (defaults to "booted")
            
        Returns:
            List of dictionaries containing app information
            
        Raises:
            SimulatorError: If unable to list installed apps
        """
        self.logger.info(f"📱 Listing installed apps on device: {device_id}")
        
        try:
            output, success = await run_command(["xcrun", "simctl", "listapps", device_id])
            
            if success:
                self.logger.info("✅ Successfully retrieved installed apps list")
                
                # Parse the output to extract app information
                apps = []
                lines = output.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('=') and ':' in line:
                        # Basic parsing - this could be enhanced based on actual output format
                        apps.append({
                            "raw_info": line,
                            "device_id": device_id
                        })
                
                self.logger.debug(f"🔍 Found {len(apps)} installed apps")
                return apps
            else:
                raise SimulatorError(
                    f"Failed to list installed apps on device {device_id}",
                    context={
                        "device_id": device_id,
                        "command_output": output
                    }
                )
                
        except Exception as e:
            if isinstance(e, SimulatorError):
                raise
            
            raise SimulatorError(
                f"Unexpected error listing apps on device {device_id}: {str(e)}",
                context={"device_id": device_id, "error_type": type(e).__name__}
            ) 