"""
Screenshot service for iOS automation.

This module handles taking and managing screenshots from iOS simulators
with proper error handling and file management.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add the parent directory to sys.path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.utils.command_runner import run_command
from shared.utils.logger import get_logger
from shared.utils.exceptions import ScreenshotError

logger = get_logger(__name__)


class ScreenshotService:
    """
    Service for taking and managing screenshots from iOS simulators.
    
    This class follows the Single Responsibility Principle by focusing
    solely on screenshot-related operations.
    """
    
    def __init__(self, default_directory: Optional[str] = None):
        """
        Initialize the screenshot service.
        
        Args:
            default_directory: Default directory for saving screenshots
        """
        if default_directory:
            self.default_directory = Path(default_directory)
        else:
            # Use project root directory instead of current working directory
            # to avoid issues when MCP server is started by Claude Desktop
            project_root = Path(__file__).parent.parent
            self.default_directory = project_root / "screenshots"
        
        self.logger = get_logger(__name__)
        
        # Ensure default directory exists
        self.default_directory.mkdir(parents=True, exist_ok=True)
    
    async def take_screenshot(
        self, 
        filename: Optional[str] = None,
        device_id: str = "booted",
        directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Take a screenshot of the specified iOS simulator.
        
        Args:
            filename: Name for the screenshot file (auto-generated if None)
            device_id: The simulator UDID (defaults to "booted")
            directory: Directory to save the screenshot (uses default if None)
            
        Returns:
            Dictionary with screenshot information and file path
            
        Raises:
            ScreenshotError: If unable to take or save the screenshot
        """
        
        # Determine save directory
        save_dir = Path(directory) if directory else self.default_directory
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ios_screenshot_{timestamp}.png"
        
        # Ensure filename has .png extension
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Full path for the screenshot
        screenshot_path = save_dir / filename
        
        self.logger.info(f"📸 Taking screenshot of device: {device_id}")
        self.logger.debug(f"💾 Save path: {screenshot_path}")
        
        try:
            # Take screenshot using simctl
            output, success = await run_command([
                "xcrun", "simctl", "io", device_id, "screenshot", str(screenshot_path)
            ])
            
            if success and screenshot_path.exists():
                # Get file size for verification
                file_size = screenshot_path.stat().st_size
                
                self.logger.info(f"✅ Screenshot saved successfully: {screenshot_path}")
                self.logger.debug(f"📊 File size: {file_size:,} bytes")
                
                return {
                    "success": True,
                    "filename": filename,
                    "path": str(screenshot_path),
                    "size_bytes": file_size,
                    "device_id": device_id,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Check if file was created but command reported failure
                if screenshot_path.exists():
                    file_size = screenshot_path.stat().st_size
                    if file_size > 0:
                        self.logger.warning(f"⚠️ Screenshot saved but command reported failure: {output}")
                        return {
                            "success": True,
                            "filename": filename,
                            "path": str(screenshot_path),
                            "size_bytes": file_size,
                            "device_id": device_id,
                            "timestamp": datetime.now().isoformat(),
                            "warning": "Command reported failure but file was created"
                        }
                
                raise ScreenshotError(
                    f"Failed to take screenshot of device {device_id}",
                    context={
                        "device_id": device_id,
                        "save_path": str(screenshot_path),
                        "command_output": output,
                        "file_exists": screenshot_path.exists(),
                        "suggestions": [
                            "Check if simulator is booted and accessible",
                            "Verify device ID is correct",
                            "Ensure write permissions to save directory"
                        ]
                    }
                )
                
        except Exception as e:
            if isinstance(e, ScreenshotError):
                raise
            
            # Clean up partial file if it exists
            if screenshot_path.exists():
                try:
                    screenshot_path.unlink()
                    self.logger.debug(f"🗑️ Cleaned up partial screenshot file: {screenshot_path}")
                except:
                    pass
            
            raise ScreenshotError(
                f"Unexpected error taking screenshot: {str(e)}",
                context={
                    "device_id": device_id,
                    "save_path": str(screenshot_path),
                    "error_type": type(e).__name__
                }
            )
    
    async def take_multiple_screenshots(
        self,
        count: int,
        interval_seconds: float = 1.0,
        device_id: str = "booted",
        directory: Optional[str] = None,
        prefix: str = "sequence"
    ) -> List[Dict[str, Any]]:
        """
        Take multiple screenshots at specified intervals.
        
        This is useful for capturing sequences of automation actions
        or monitoring app state changes.
        
        Args:
            count: Number of screenshots to take
            interval_seconds: Time between screenshots
            device_id: The simulator UDID (defaults to "booted")
            directory: Directory to save screenshots (uses default if None)
            prefix: Prefix for screenshot filenames
            
        Returns:
            List of dictionaries with screenshot information
            
        Raises:
            ScreenshotError: If unable to take screenshots
        """
        
        if count <= 0:
            raise ScreenshotError("Screenshot count must be positive")
        
        if interval_seconds < 0:
            raise ScreenshotError("Interval must be non-negative")
        
        self.logger.info(f"📸 Taking {count} screenshots with {interval_seconds}s interval")
        
        screenshots = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            for i in range(count):
                # Generate sequential filename
                filename = f"{prefix}_{timestamp}_{i+1:03d}.png"
                
                # Take screenshot
                result = await self.take_screenshot(
                    filename=filename,
                    device_id=device_id,
                    directory=directory
                )
                
                result["sequence_number"] = i + 1
                result["total_count"] = count
                screenshots.append(result)
                
                self.logger.debug(f"📸 Screenshot {i+1}/{count} completed")
                
                # Wait before next screenshot (except for the last one)
                if i < count - 1 and interval_seconds > 0:
                    await asyncio.sleep(interval_seconds)
            
            self.logger.info(f"✅ Successfully captured {len(screenshots)} screenshots")
            return screenshots
            
        except Exception as e:
            if isinstance(e, ScreenshotError):
                raise
            
            raise ScreenshotError(
                f"Failed to capture screenshot sequence: {str(e)}",
                context={
                    "count": count,
                    "completed": len(screenshots),
                    "interval": interval_seconds,
                    "device_id": device_id,
                    "error_type": type(e).__name__
                }
            )
    
    def list_screenshots(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all screenshot files in the specified directory.
        
        Args:
            directory: Directory to search (uses default if None)
            
        Returns:
            List of dictionaries with file information
        """
        
        search_dir = Path(directory) if directory else self.default_directory
        
        if not search_dir.exists():
            self.logger.warning(f"⚠️ Screenshot directory does not exist: {search_dir}")
            return []
        
        self.logger.info(f"📂 Listing screenshots in: {search_dir}")
        
        screenshots = []
        
        # Find all PNG files in the directory
        for png_file in search_dir.glob("*.png"):
            try:
                stat = png_file.stat()
                screenshots.append({
                    "filename": png_file.name,
                    "path": str(png_file),
                    "size_bytes": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception as e:
                self.logger.warning(f"⚠️ Error reading file info for {png_file}: {e}")
        
        # Sort by creation time (newest first)
        screenshots.sort(key=lambda x: x["created"], reverse=True)
        
        self.logger.info(f"📊 Found {len(screenshots)} screenshot files")
        return screenshots
    
    async def cleanup_old_screenshots(
        self,
        keep_count: int = 10,
        directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Clean up old screenshot files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of recent screenshots to keep
            directory: Directory to clean (uses default if None)
            
        Returns:
            Dictionary with cleanup statistics
        """
        
        if keep_count < 0:
            raise ScreenshotError("Keep count must be non-negative")
        
        search_dir = Path(directory) if directory else self.default_directory
        
        if not search_dir.exists():
            self.logger.info(f"📂 Screenshot directory does not exist: {search_dir}")
            return {"deleted": 0, "kept": 0, "directory": str(search_dir)}
        
        self.logger.info(f"🧹 Cleaning up old screenshots, keeping {keep_count} recent files")
        
        # Get all PNG files sorted by modification time (newest first)
        png_files = list(search_dir.glob("*.png"))
        png_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        # Determine which files to delete
        files_to_keep = png_files[:keep_count]
        files_to_delete = png_files[keep_count:]
        
        deleted_count = 0
        deleted_size = 0
        
        # Delete old files
        for file_path in files_to_delete:
            try:
                file_size = file_path.stat().st_size
                file_path.unlink()
                deleted_count += 1
                deleted_size += file_size
                self.logger.debug(f"🗑️ Deleted: {file_path.name}")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to delete {file_path}: {e}")
        
        result = {
            "deleted": deleted_count,
            "kept": len(files_to_keep),
            "deleted_size_bytes": deleted_size,
            "directory": str(search_dir)
        }
        
        if deleted_count > 0:
            self.logger.info(f"✅ Cleanup complete: deleted {deleted_count} files ({deleted_size:,} bytes)")
        else:
            self.logger.info("✅ No files needed cleanup")
        
        return result 