"""
Find and tap tool for iOS automation.

This module provides a comprehensive tool for finding and tapping any UI element
on iOS screens using multiple finding strategies. Built following SOLID principles
with production-level error handling and logging.
"""

import asyncio
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Add the ios_mcp_server directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from automation.appium_client import AppiumClient
from config.settings import settings
from shared.utils.logger import get_logger
from shared.utils.exceptions import AutomationError, ValidationError


class FindAndTapTool:
    """
    Advanced tool for finding and tapping UI elements on iOS.
    
    This tool implements multiple element finding strategies following the
    Strategy pattern, allowing flexible element location and interaction.
    Supports various element types including buttons, text, images, and more.
    
    Key Features:
    - Multiple finding strategies with priority ordering
    - Robust error handling with detailed context
    - Screenshot capture for debugging
    - Comprehensive element validation
    - Production-ready logging and monitoring
    """
    
    # Element finding strategies in priority order
    FINDING_STRATEGIES = [
        "accessibility_id",
        "text_content", 
        "partial_text",
        "element_type_with_text",
        "xpath_selector",
        "class_name"
    ]
    
    # Supported iOS element types for XCUITest
    SUPPORTED_ELEMENT_TYPES = [
        "button", "staticText", "textField", "secureTextField",
        "image", "cell", "navigationBar", "tabBar", "toolbar",
        "scrollView", "table", "collectionView", "switch",
        "slider", "progressIndicator", "activityIndicator",
        "alert", "sheet", "popover", "menuItem", "menuButton",
        "link", "searchField", "any"
    ]
    
    def __init__(self):
        """Initialize the Find and Tap tool with logging."""
        super().__init__()
        self.logger = get_logger(__name__)
        
    @property
    def name(self) -> str:
        """Return the tool name for MCP registration."""
        return "find_and_tap"
    
    @property
    def description(self) -> str:
        """Return comprehensive tool description."""
        return (
            "Find and tap any UI element on iOS screen using intelligent "
            "element finding strategies. Supports text-based finding, "
            "accessibility IDs, element types, and XPath selectors."
        )
    
    async def execute_impl(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the find and tap operation.
        
        This method orchestrates the entire find and tap workflow:
        1. Validates input arguments
        2. Attempts multiple finding strategies
        3. Performs the tap operation
        4. Captures results and screenshots
        5. Provides detailed execution feedback
        
        Args:
            **kwargs: Validated tool arguments
            
        Returns:
            Dictionary containing execution results, element info, and metadata
            
        Raises:
            AutomationError: If element finding or tapping fails
            ValidationError: If arguments are invalid
        """
        
        # Extract and validate arguments
        element_text = kwargs.get("element_text")
        element_type = kwargs.get("element_type", "any")
        accessibility_id = kwargs.get("accessibility_id")
        partial_match = kwargs.get("partial_match", False)
        xpath = kwargs.get("xpath")
        timeout = kwargs.get("timeout", 10)
        take_screenshot = kwargs.get("take_screenshot", True)
        app_bundle_id = kwargs.get("app_bundle_id", settings.ios.default_bundle_id)
        dismiss_after_screenshot = kwargs.get("dismiss_after_screenshot", False)
        dismiss_button_text = kwargs.get("dismiss_button_text")
        
        self.logger.info(f"🎯 Starting find and tap operation")
        self.logger.debug(f"📋 Search criteria: text='{element_text}', type='{element_type}', "
                         f"accessibility_id='{accessibility_id}', xpath='{xpath}'")
        
        # Validate that at least one search criterion is provided
        if not any([element_text, accessibility_id, xpath]):
            raise ValidationError(
                "At least one search criterion must be provided: element_text, accessibility_id, or xpath",
                context={
                    "provided_args": kwargs,
                    "required_criteria": ["element_text", "accessibility_id", "xpath"]
                }
            )
        
        try:
            # Initialize Appium client
            appium_client = AppiumClient()
            await appium_client.start_session()
            
            # Build search criteria for element finding
            search_criteria = self._build_search_criteria(
                element_text=element_text,
                element_type=element_type, 
                accessibility_id=accessibility_id,
                partial_match=partial_match,
                xpath=xpath
            )
            
            # Generate and execute the automation script
            script_content = self._generate_find_and_tap_script(
                search_criteria=search_criteria,
                timeout=timeout,
                take_screenshot=take_screenshot,
                app_bundle_id=app_bundle_id,
                dismiss_after_screenshot=dismiss_after_screenshot,
                dismiss_button_text=dismiss_button_text
            )
            
            # Execute the automation script
            execution_result = await self._execute_automation_script(script_content)
            
            # Clean up Appium session
            await appium_client.close_session()
            
            # Parse and return results
            return self._parse_execution_results(execution_result, search_criteria)
            
        except Exception as e:
            self.logger.error(f"❌ Find and tap operation failed: {e}")
            raise AutomationError(
                f"Failed to find and tap element: {str(e)}",
                context={
                    "search_criteria": locals().get("search_criteria", {}),
                    "timeout": timeout,
                    "error_type": type(e).__name__
                }
            )
    
    def _build_search_criteria(
        self,
        element_text: Optional[str] = None,
        element_type: str = "any",
        accessibility_id: Optional[str] = None, 
        partial_match: bool = False,
        xpath: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build comprehensive search criteria for element finding.
        
        This method creates a structured search criteria object that will be
        used to generate the appropriate Appium automation script.
        
        Args:
            element_text: Text content to search for
            element_type: iOS element type filter
            accessibility_id: Accessibility identifier
            partial_match: Whether to use partial text matching
            xpath: XPath selector
            
        Returns:
            Dictionary containing structured search criteria
        """
        
        criteria = {
            "strategies": [],
            "primary_text": element_text,
            "element_type": element_type,
            "timeout": 10
        }
        
        # Strategy 1: Accessibility ID (highest priority)
        if accessibility_id:
            criteria["strategies"].append({
                "method": "accessibility_id",
                "value": accessibility_id,
                "description": f"Finding by accessibility ID: {accessibility_id}"
            })
        
        # Strategy 2: Exact text content
        if element_text and not partial_match:
            criteria["strategies"].append({
                "method": "text_exact",
                "value": element_text,
                "description": f"Finding by exact text: '{element_text}'"
            })
        
        # Strategy 3: Partial text content  
        if element_text and partial_match:
            criteria["strategies"].append({
                "method": "text_partial",
                "value": element_text,
                "description": f"Finding by partial text: '{element_text}'"
            })
        
        # Strategy 4: Element type with text combination
        if element_text and element_type != "any":
            criteria["strategies"].append({
                "method": "type_with_text",
                "element_type": element_type,
                "text_value": element_text,
                "description": f"Finding {element_type} with text: '{element_text}'"
            })
        
        # Strategy 5: XPath selector
        if xpath:
            criteria["strategies"].append({
                "method": "xpath",
                "value": xpath,
                "description": f"Finding by XPath: {xpath}"
            })
        
        # Strategy 6: Element type only (lowest priority)
        if element_type != "any" and not element_text:
            criteria["strategies"].append({
                "method": "element_type",
                "value": element_type,
                "description": f"Finding first {element_type} element"
            })
        
        self.logger.debug(f"🔍 Built search criteria with {len(criteria['strategies'])} strategies")
        return criteria
    
    def _generate_find_and_tap_script(
        self,
        search_criteria: Dict[str, Any],
        timeout: int,
        take_screenshot: bool,
        app_bundle_id: str,
        dismiss_after_screenshot: bool = False,
        dismiss_button_text: str = None
    ) -> str:
        """
        Generate comprehensive Appium automation script.
        
        This method creates a self-contained Python script that implements
        all finding strategies with proper error handling and logging.
        
        Args:
            search_criteria: Structured search criteria
            timeout: Element finding timeout
            take_screenshot: Whether to capture screenshot
            
        Returns:
            Complete Python automation script as string
        """
        
        # Import settings for configuration
        from ios_mcp_server.config.settings import settings
        
        # Build strategy implementations
        strategy_implementations = []
        for i, strategy in enumerate(search_criteria["strategies"]):
            strategy_code = self._generate_strategy_code(strategy, i + 1)
            strategy_implementations.append(strategy_code)
        
        # Generate the complete script
        script = f'''
import sys
import os
import time

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
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError as e:
    print(f"ERROR: Failed to import required packages: {{e}}")
    print("Make sure Appium Python client is installed in the virtual environment")
    sys.exit(1)

def main():
    """Main automation execution function."""
    driver = None
    try:
        print("🚀 Starting find and tap automation")
        
        # Configure Appium options (new API)
        options = XCUITestOptions()
        options.platform_name = "{settings.ios.platform_name}"
        options.platform_version = "{settings.ios.platform_version}"
        options.device_name = "{settings.ios.device_name}"
        options.automation_name = "{settings.ios.automation_name}"
        options.bundle_id = "{app_bundle_id}"
        options.no_reset = {settings.ios.no_reset}
        options.new_command_timeout = {timeout * 2}
        
        print(f"📱 Connecting to device: {{options.device_name}}")
        driver = webdriver.Remote("{settings.appium.url}", options=options)
        
        # Wait for app to be ready
        time.sleep(2)
        
        element = None
        successful_strategy = None
        
        # Try each finding strategy in order
        {chr(10).join(strategy_implementations)}
        
        # If no element found, raise error
        if element is None:
            available_elements = []
            try:
                # Get some context about available elements
                all_elements = driver.find_elements(AppiumBy.XPATH, "//*[@name or @label or @value]")
                for elem in all_elements[:10]:  # Limit to first 10
                    try:
                        name = elem.get_attribute("name") or elem.get_attribute("label") or elem.get_attribute("value")
                        elem_type = elem.get_attribute("type") or elem.tag_name
                        if name:
                            available_elements.append(f"{{elem_type}}: '{{name}}'")
                    except Exception:
                        continue
            except:
                pass
            
            error_msg = "❌ Element not found with any strategy"
            if available_elements:
                error_msg += f"\\n📋 Available elements: {{', '.join(available_elements[:5])}}"
            
            print(error_msg)
            return
        
        # Perform the tap
        print(f"✅ Element found using: {{successful_strategy}}")
        print("👆 Performing tap...")
        element.click()
        
        # Wait a moment for the action to complete
        time.sleep(1)
        
        # Take screenshot if requested
        screenshot_path = None
        if {str(take_screenshot)}:
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"ios_findtap_{{timestamp}}.png"
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {{screenshot_path}}")
            except Exception as e:
                print(f"⚠️ Screenshot failed: {{e}}")
        
        # Dismiss modal/screen if requested
        if {str(dismiss_after_screenshot)}:
            try:
                print("🔙 Attempting to dismiss modal/screen...")
                dismiss_success = False
                
                # Define dismiss button texts to try
                dismiss_texts = []
                if "{dismiss_button_text}":
                    dismiss_texts.append("{dismiss_button_text}")
                else:
                    # Common dismiss button texts
                    dismiss_texts = ["Done", "Cancel", "Close", "Back", "Dismiss", "OK"]
                
                # Try to find and tap dismiss buttons
                for dismiss_text in dismiss_texts:
                    try:
                        # Try multiple selectors for dismiss button
                        selectors = [
                            (AppiumBy.XPATH, f"//*[@name='{{dismiss_text}}']"),
                            (AppiumBy.XPATH, f"//XCUIElementTypeButton[@name='{{dismiss_text}}']"),
                            (AppiumBy.XPATH, f"//*[contains(@name, '{{dismiss_text}}')]"),
                            (AppiumBy.ACCESSIBILITY_ID, dismiss_text)
                        ]
                        
                        for selector_type, selector_value in selectors:
                            try:
                                dismiss_button = driver.find_element(selector_type, selector_value)
                                dismiss_button.click()
                                print(f"✅ Dismissed using '{{dismiss_text}}' button")
                                dismiss_success = True
                                time.sleep(1)  # Wait for dismiss animation
                                break
                            except:
                                continue
                        
                        if dismiss_success:
                            break
                            
                    except Exception as e:
                        continue
                
                # If no specific dismiss button found, try navigation bar back button
                if not dismiss_success:
                    try:
                        # Try common navigation patterns
                        nav_selectors = [
                            (AppiumBy.XPATH, "//XCUIElementTypeNavigationBar//XCUIElementTypeButton[1]"),  # First button in nav bar (usually back)
                            (AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Back']"),
                            (AppiumBy.XPATH, "//*[@name='chevron.left']"),  # iOS back chevron
                            (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'back')]")
                        ]
                        
                        for selector_type, selector_value in nav_selectors:
                            try:
                                back_button = driver.find_element(selector_type, selector_value)
                                back_button.click()
                                print("✅ Dismissed using navigation back button")
                                dismiss_success = True
                                time.sleep(1)
                                break
                            except:
                                continue
                                
                    except Exception as e:
                        pass
                
                if not dismiss_success:
                    print("⚠️ Could not find dismiss button - modal may still be open")
                    
            except Exception as e:
                print(f"⚠️ Dismiss failed: {{e}}")
        
        print("SUCCESS: Element tapped successfully")
        
    except Exception as e:
        print(f"ERROR: {{str(e)}}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    main()
'''
        return script
    
    def _generate_strategy_code(self, strategy: Dict[str, Any], strategy_num: int) -> str:
        """
        Generate code for a specific finding strategy.
        
        Args:
            strategy: Strategy configuration dictionary
            strategy_num: Strategy number for logging
            
        Returns:
            Python code implementing the strategy
        """
        
        method = strategy["method"]
        
        if method == "accessibility_id":
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                element = WebDriverWait(driver, {10}).until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "{strategy['value']}"))
                )
                successful_strategy = "Accessibility ID: {strategy['value']}"
            except TimeoutException:
                print("⏰ Strategy {strategy_num} timed out")
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        elif method == "text_exact":
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                # Try multiple text-based selectors
                selectors = [
                    (AppiumBy.XPATH, f"//*[@name='{strategy['value']}']"),
                    (AppiumBy.XPATH, f"//*[@label='{strategy['value']}']"),
                    (AppiumBy.XPATH, f"//*[@value='{strategy['value']}']"),
                    (AppiumBy.XPATH, f"//*[text()='{strategy['value']}']")
                ]
                
                for selector_type, selector_value in selectors:
                    try:
                        element = driver.find_element(selector_type, selector_value)
                        successful_strategy = f"Exact text: {strategy['value']}"
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        elif method == "text_partial":
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                # Try partial text matching
                selectors = [
                    (AppiumBy.XPATH, f"//*[contains(@name, '{strategy['value']}')]"),
                    (AppiumBy.XPATH, f"//*[contains(@label, '{strategy['value']}')]"),
                    (AppiumBy.XPATH, f"//*[contains(@value, '{strategy['value']}')]"),
                    (AppiumBy.XPATH, f"//*[contains(text(), '{strategy['value']}')]")
                ]
                
                for selector_type, selector_value in selectors:
                    try:
                        element = driver.find_element(selector_type, selector_value)
                        successful_strategy = f"Partial text: {strategy['value']}"
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        elif method == "type_with_text":
            element_type = strategy["element_type"]
            text_value = strategy["text_value"]
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                # Find element by type and text combination
                xpath_selectors = [
                    f"//XCUIElementType{element_type.title()}[@name='{text_value}']",
                    f"//XCUIElementType{element_type.title()}[@label='{text_value}']",
                    f"//XCUIElementType{element_type.title()}[contains(@name, '{text_value}')]",
                    f"//*[@type='{element_type}'][@name='{text_value}']"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        element = driver.find_element(AppiumBy.XPATH, xpath)
                        successful_strategy = f"{element_type} with text: {text_value}"
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        elif method == "xpath":
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "{strategy['value']}"))
                )
                successful_strategy = f"XPath: {strategy['value']}"
            except TimeoutException:
                print("⏰ Strategy {strategy_num} timed out")
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        elif method == "element_type":
            element_type = strategy["value"]
            return f'''
        # Strategy {strategy_num}: {strategy["description"]}
        if element is None:
            try:
                print("🔍 Strategy {strategy_num}: {strategy['description']}")
                # Find first element of specified type
                xpath_selectors = [
                    f"//XCUIElementType{element_type.title()}",
                    f"//*[@type='{element_type}']"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        element = driver.find_element(AppiumBy.XPATH, xpath)
                        successful_strategy = f"First {element_type} element"
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {{e}}")
'''
        
        return f"# Unknown strategy: {method}"
    
    async def _execute_automation_script(self, script_content: str) -> Dict[str, Any]:
        """
        Execute the generated automation script.
        
        Args:
            script_content: Complete Python automation script
            
        Returns:
            Dictionary containing execution results
            
        Raises:
            AutomationError: If script execution fails
        """
        
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
            
            return {
                "return_code": process.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "success": process.returncode == 0 and "SUCCESS" in stdout_str
            }
            
        except Exception as e:
            raise AutomationError(
                f"Failed to execute automation script: {str(e)}",
                context={"error_type": type(e).__name__}
            )
    
    def _parse_execution_results(
        self, 
        execution_result: Dict[str, Any], 
        search_criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse and format execution results.
        
        Args:
            execution_result: Raw execution results from script
            search_criteria: Original search criteria used
            
        Returns:
            Formatted results dictionary
        """
        
        stdout = execution_result.get("stdout", "")
        stderr = execution_result.get("stderr", "")
        success = execution_result.get("success", False)
        
        # Extract key information from output
        successful_strategy = None
        screenshot_path = None
        
        for line in stdout.split('\n'):
            if "Element found using:" in line:
                successful_strategy = line.split("Element found using:")[-1].strip()
            elif "Screenshot saved:" in line:
                screenshot_path = line.split("Screenshot saved:")[-1].strip()
        
        if success:
            self.logger.info(f"✅ Find and tap completed successfully")
            if successful_strategy:
                self.logger.info(f"🎯 Used strategy: {successful_strategy}")
            
            return {
                "success": True,
                "message": "Element found and tapped successfully",
                "strategy_used": successful_strategy,
                "screenshot_path": screenshot_path,
                "search_criteria": search_criteria,
                "execution_time": "< 1s",  # Could be enhanced with actual timing
                "strategies_attempted": len(search_criteria.get("strategies", [])),
                "details": {
                    "stdout": stdout,
                    "element_found": True,
                    "tap_completed": True
                }
            }
        else:
            # Extract error details
            error_details = stderr or "Unknown automation error"
            if "Element not found" in stdout:
                error_details = "Element not found with any search strategy"
            
            self.logger.error(f"❌ Find and tap failed: {error_details}")
            
            raise AutomationError(
                f"Find and tap operation failed: {error_details}",
                context={
                    "search_criteria": search_criteria,
                    "strategies_attempted": len(search_criteria.get("strategies", [])),
                    "stdout": stdout,
                    "stderr": stderr,
                    "suggestions": [
                        "Verify the element text or accessibility ID is correct",
                        "Try using partial_match=true for text searches",
                        "Check if the element is visible on screen",
                        "Take a screenshot to verify the current screen state"
                    ]
                }
            ) 