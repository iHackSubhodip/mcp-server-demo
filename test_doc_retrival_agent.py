#!/usr/bin/env python3
"""
iOS App Testing Script for doc-retrival-agent
Automated testing workflow using simctl commands
"""

import asyncio
import subprocess
import json
import time
from pathlib import Path

class iOSAppTester:
    def __init__(self, app_bundle_id="com.google.doc-retrival-agent"):
        self.app_bundle_id = app_bundle_id
        self.device_id = "booted"  # Use currently booted simulator
        self.screenshots_dir = Path("~/Desktop/ios_test_screenshots").expanduser()
        self.screenshots_dir.mkdir(exist_ok=True)
        
    async def run_command(self, cmd: list[str]) -> tuple[str, bool]:
        """Run a shell command and return (output, success)"""
        try:
            print(f"🚧 Executing: {' '.join(cmd)}")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                print(f"✅ Command succeeded")
                return stdout.decode(), True
            else:
                print(f"❌ Command failed: {stderr.decode()}")
                return stderr.decode() or "Command failed", False
        except Exception as e:
            print(f"💥 Exception: {str(e)}")
            return f"Error: {str(e)}", False

    async def take_screenshot(self, name: str) -> str:
        """Take a screenshot with a descriptive name"""
        timestamp = int(time.time())
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        output, success = await self.run_command([
            "xcrun", "simctl", "io", self.device_id, "screenshot", str(filepath)
        ])
        
        if success:
            print(f"📸 Screenshot saved: {filepath}")
            return str(filepath)
        else:
            print(f"❌ Screenshot failed: {output}")
            return ""

    async def launch_app(self) -> bool:
        """Launch the target app"""
        print(f"🚀 Launching {self.app_bundle_id}")
        output, success = await self.run_command([
            "xcrun", "simctl", "launch", self.device_id, self.app_bundle_id
        ])
        
        if success:
            print(f"✅ App launched successfully")
            await asyncio.sleep(3)  # Wait for app to load
            return True
        else:
            print(f"❌ Failed to launch app: {output}")
            return False

    async def get_accessibility_tree(self) -> dict:
        """Get the accessibility tree for UI analysis"""
        print("🌳 Getting accessibility tree...")
        output, success = await self.run_command([
            "xcrun", "simctl", "io", self.device_id, "accessibility", "tree", "--format", "json"
        ])
        
        if success:
            try:
                tree = json.loads(output)
                print("✅ Accessibility tree retrieved")
                return tree
            except json.JSONDecodeError:
                print("❌ Failed to parse accessibility tree JSON")
                return {}
        else:
            print(f"❌ Failed to get accessibility tree: {output}")
            return {}

    async def tap_coordinate(self, x: int, y: int) -> bool:
        """Tap at specific coordinates"""
        print(f"👆 Tapping at ({x}, {y})")
        output, success = await self.run_command([
            "xcrun", "simctl", "io", self.device_id, "tap", str(x), str(y)
        ])
        
        if success:
            print(f"✅ Tapped successfully at ({x}, {y})")
            await asyncio.sleep(1)  # Wait for UI response
            return True
        else:
            print(f"❌ Tap failed: {output}")
            return False

    async def type_text(self, text: str) -> bool:
        """Type text into the currently focused input field"""
        print(f"⌨️ Typing: '{text}'")
        # Note: simctl doesn't have direct text input, but we can simulate key presses
        # For now, we'll use a placeholder approach
        print("ℹ️ Text typing would require additional UI automation setup")
        return True

    def find_elements_by_type(self, tree: dict, element_type: str) -> list:
        """Find UI elements by type in accessibility tree"""
        elements = []
        
        def search_recursive(node):
            if isinstance(node, dict):
                if node.get("type") == element_type or element_type.lower() in str(node.get("label", "")).lower():
                    elements.append(node)
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        search_recursive(value)
            elif isinstance(node, list):
                for item in node:
                    search_recursive(item)
        
        search_recursive(tree)
        return elements

    async def run_test_workflow(self):
        """Run the complete testing workflow"""
        print("🎯 Starting iOS App Testing Workflow for doc-retrival-agent")
        print("=" * 60)
        
        # Step 1: Take initial screenshot
        print("\n📸 Step 1: Taking initial home screen screenshot")
        await self.take_screenshot("01_home_screen")
        
        # Step 2: Launch the app
        print("\n🚀 Step 2: Launching doc-retrival-agent app")
        if not await self.launch_app():
            print("❌ Test failed: Could not launch app")
            return False
        
        # Step 3: Take screenshot after launch
        print("\n📸 Step 3: Taking screenshot after app launch")
        await self.take_screenshot("02_app_launched")
        
        # Step 4: Get accessibility tree
        print("\n🌳 Step 4: Analyzing app UI structure")
        tree = await self.get_accessibility_tree()
        
        if tree:
            # Look for common UI elements
            buttons = self.find_elements_by_type(tree, "button")
            settings_buttons = [b for b in buttons if "settings" in str(b.get("label", "")).lower()]
            
            print(f"📊 Found {len(buttons)} buttons in the app")
            if settings_buttons:
                print(f"⚙️ Found {len(settings_buttons)} settings-related buttons")
            
            # Look for text fields
            text_fields = self.find_elements_by_type(tree, "textField")
            chat_fields = [t for t in text_fields if any(word in str(t.get("label", "")).lower() 
                          for word in ["chat", "message", "input", "text"])]
            
            print(f"📝 Found {len(text_fields)} text fields")
            if chat_fields:
                print(f"💬 Found {len(chat_fields)} chat-related text fields")
        
        # Step 5: Try to tap settings (if found)
        print("\n⚙️ Step 5: Looking for settings button")
        # Common settings button locations (you may need to adjust these)
        settings_coordinates = [
            (50, 50),    # Top-left corner
            (350, 50),   # Top-right corner
            (200, 100),  # Top-center
        ]
        
        for i, (x, y) in enumerate(settings_coordinates):
            print(f"🎯 Trying settings location {i+1}: ({x}, {y})")
            await self.tap_coordinate(x, y)
            await self.take_screenshot(f"03_after_tap_{i+1}")
            await asyncio.sleep(2)
        
        # Step 6: Look for chat input
        print("\n💬 Step 6: Looking for chat input field")
        # Common chat input locations
        chat_coordinates = [
            (200, 600),  # Bottom center
            (200, 500),  # Middle center
            (200, 400),  # Upper middle
        ]
        
        for i, (x, y) in enumerate(chat_coordinates):
            print(f"🎯 Trying chat input location {i+1}: ({x}, {y})")
            await self.tap_coordinate(x, y)
            await self.take_screenshot(f"04_chat_tap_{i+1}")
            
            # Try to type test message
            await self.type_text("Hello, this is a test message from iOS automation!")
            await asyncio.sleep(2)
        
        # Step 7: Final screenshot
        print("\n📸 Step 7: Taking final screenshot")
        await self.take_screenshot("05_final_state")
        
        print("\n🎉 Testing workflow completed!")
        print(f"📁 Screenshots saved to: {self.screenshots_dir}")
        print("=" * 60)
        
        return True

async def main():
    """Main function to run the testing workflow"""
    tester = iOSAppTester()
    await tester.run_test_workflow()

if __name__ == "__main__":
    asyncio.run(main()) 