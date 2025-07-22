"""
Appium client for iOS automation.

This module provides a clean interface to Appium automation services,
handling connection management, script generation, and execution.
"""

import os
import sys
import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import aiohttp

from config.settings import settings
from shared.utils.logger import get_logger
from shared.utils.exceptions import AppiumConnectionError, AutomationError

logger = get_logger(__name__)


class AppiumClient:
    """
    Client for communicating with Appium server and executing iOS automation.
    
    This class follows the Single Responsibility Principle by focusing
    solely on Appium automation operations.
    """
    
    def __init__(self, appium_url: Optional[str] = None):
        """
        Initialize the Appium client.
        
        Args:
            appium_url: Override for Appium server URL (uses config default if None)
        """
        self.appium_url = appium_url or settings.appium.url
        self.session_active = False
        self.logger = get_logger(__name__)
    
    async def start_session(self) -> None:
        """
        Initialize connection to Appium server.
        
        This method verifies that the Appium server is running and accessible
        before attempting any automation operations.
        
        Raises:
            AppiumConnectionError: If unable to connect to Appium server
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.appium_url}/status") as response:
                    if response.status == 200:
                        status_data = await response.json()
                        self.logger.info(f"✅ Connected to Appium server: {self.appium_url}")
                        self.logger.debug(f"🔍 Appium status: {status_data}")
                        self.session_active = True
                    else:
                        raise AppiumConnectionError(
                            f"Appium server returned status {response.status}",
                            context={"url": self.appium_url, "status": response.status}
                        )
        except aiohttp.ClientError as e:
            raise AppiumConnectionError(
                f"Failed to connect to Appium server at {self.appium_url}",
                context={
                    "url": self.appium_url,
                    "error": str(e),
                    "suggestion": "Make sure Appium server is running: appium server --port 4723"
                }
            )
        except Exception as e:
            raise AppiumConnectionError(
                f"Unexpected error connecting to Appium: {str(e)}",
                context={"url": self.appium_url, "error_type": type(e).__name__}
            )
    
    async def close_session(self) -> None:
        """
        Clean up Appium session resources.
        
        This method should be called when automation is complete
        to properly release resources.
        """
        self.session_active = False
        self.logger.info("🔌 Appium session closed")
    
    async def tap_and_type(
        self, 
        text: str, 
        app_bundle_id: Optional[str] = None,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Execute tap and type automation using Appium.
        
        This method generates and executes a temporary Python script that:
        1. Connects to the specified iOS app
        2. Finds a text field element
        3. Taps the element to focus it
        4. Types the specified text
        5. Takes a screenshot as proof
        
        Args:
            text: Text to type into the field
            app_bundle_id: iOS app bundle ID (uses default if None)
            timeout: Timeout for element finding in seconds
            
        Returns:
            Dictionary with success status and details
            
        Raises:
            AutomationError: If automation script execution fails
        """
        
        # Use configured default bundle ID if none provided
        bundle_id = app_bundle_id or settings.ios.default_bundle_id
        
        self.logger.info(f"🚀 Starting tap and type automation")
        self.logger.debug(f"📱 Target app: {bundle_id}")
        self.logger.debug(f"⌨️ Text to type: '{text}'")
        
        # Generate the automation script
        script_content = self._generate_automation_script(text, bundle_id, timeout)
        
        try:
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            self.logger.debug(f"📝 Generated automation script: {script_path}")
            
            # Execute the automation script
            process = await asyncio.create_subprocess_exec(
                'python3', script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up temporary file
            Path(script_path).unlink(missing_ok=True)
            
            # Parse results
            stdout_str = stdout.decode('utf-8', errors='replace')
            stderr_str = stderr.decode('utf-8', errors='replace')
            
            if process.returncode == 0 and "SUCCESS" in stdout_str:
                self.logger.info(f"✅ Automation successful: '{text}' typed successfully")
                return {
                    "success": True,
                    "message": f"Successfully tapped and typed: '{text}'",
                    "app_bundle_id": bundle_id,
                    "screenshot_saved": True
                }
            else:
                # Extract meaningful error from output
                error_details = stderr_str or stdout_str or "Unknown automation error"
                self.logger.error(f"❌ Automation failed: {error_details}")
                
                raise AutomationError(
                    f"Tap and type automation failed: {error_details}",
                    context={
                        "text": text,
                        "bundle_id": bundle_id,
                        "return_code": process.returncode,
                        "stdout": stdout_str,
                        "stderr": stderr_str
                    }
                )
                
        except FileNotFoundError:
            raise AutomationError(
                "Python3 not found - required for automation script execution",
                context={"text": text, "bundle_id": bundle_id}
            )
        except Exception as e:
            raise AutomationError(
                f"Failed to execute automation script: {str(e)}",
                context={
                    "text": text,
                    "bundle_id": bundle_id,
                    "error_type": type(e).__name__
                }
            )
    
    def _generate_automation_script(self, text: str, bundle_id: str, timeout: int) -> str:
        """
        Generate the Python automation script for Appium execution.
        
        This method creates a self-contained Python script that includes
        all necessary imports and configuration for iOS automation.
        
        Args:
            text: Text to type
            bundle_id: iOS app bundle identifier
            timeout: Element finding timeout
            
        Returns:
            Complete Python script as string
        """
        
        # Escape text for Python string literals
        escaped_text = text.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        
        # Import settings for configuration
        from config.settings import settings
        
        # Generate the automation script with proper error handling
        script = f'''
import sys
import os

# Add virtual environment packages to path
venv_path = "{settings.server.venv_path}"
site_packages = os.path.join(venv_path, "lib", "{settings.server.python_version}", "site-packages")
if os.path.exists(site_packages):
    sys.path.insert(0, site_packages)

try:
    from appium import webdriver
    from appium.options.ios import XCUITestOptions
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
except ImportError as e:
    print(f"ERROR: Failed to import required packages: {{e}}")
    print("Make sure Appium Python client is installed in the virtual environment")
    sys.exit(1)

def main():
    """Main automation function with comprehensive error handling."""
    driver = None
    
    try:
        # Configure iOS automation options
        options = XCUITestOptions()
        options.platform_name = "{settings.ios.platform_name}"
        options.platform_version = "{settings.ios.platform_version}"
        options.device_name = "{settings.ios.device_name}"
        options.automation_name = "{settings.ios.automation_name}"
        options.no_reset = {settings.ios.no_reset}
        options.new_command_timeout = 30
        options.bundle_id = "{bundle_id}"
        
        print(f"Connecting to Appium server at {settings.appium.url}")
        driver = webdriver.Remote("{settings.appium.url}", options=options)
        
        print(f"Looking for text field (timeout: {timeout}s)")
        # Find text field with multiple strategies for better reliability
        text_field = None
        
        # Strategy 1: Try XCUIElementTypeTextField
        try:
            text_field = WebDriverWait(driver, {timeout}).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"))
            )
            print("Found text field using XCUIElementTypeTextField")
        except:
            # Strategy 2: Try XCUIElementTypeTextView
            try:
                text_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeTextView"))
                )
                print("Found text field using XCUIElementTypeTextView")
            except:
                # Strategy 3: Try any element with "text" in accessibility label
                try:
                    text_field = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@label, 'text') or contains(@name, 'text')]"))
                    )
                    print("Found text field using accessibility label search")
                except:
                    raise Exception("No text field found using any strategy")
        
        if not text_field:
            raise Exception("Failed to locate any text input element")
        
        print("Tapping text field to focus it")
        text_field.click()
        
        # Small delay to ensure field is focused
        time.sleep(0.5)
        
        print(f"Typing text: '{escaped_text}'")
        text_field.send_keys("{escaped_text}")
        
        # Take screenshot as proof of success
        screenshot_path = "appium_success.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {{screenshot_path}}")
        
        print("SUCCESS: Tapped and typed text successfully")
        
    except Exception as e:
        print(f"ERROR: {{type(e).__name__}}: {{str(e)}}")
        # Try to get more context about the error
        if driver:
            try:
                page_source = driver.page_source
                print(f"Page source length: {{len(page_source)}} characters")
            except:
                pass
        sys.exit(1)
        
    finally:
        if driver:
            try:
                driver.quit()
                print("WebDriver session closed")
            except:
                pass

if __name__ == "__main__":
    main()
'''
        
        return script 