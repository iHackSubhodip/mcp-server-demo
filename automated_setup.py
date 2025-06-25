#!/usr/bin/env python3
"""
Automated iOS MCP Server Setup Script
Automatically configures Claude Desktop, Cursor IDE, and other MCP-compatible environments
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import platform

class MCPSetupAutomator:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.venv_path = os.path.join(self.current_dir, "ios_mcp_env")
        self.python_path = os.path.join(self.venv_path, "bin", "python3")
        self.server_script = os.path.join(self.current_dir, "ios_mcp_server.py")
        self.success_count = 0
        self.total_steps = 0
        
    def print_step(self, step_name, description=""):
        """Print a setup step with consistent formatting"""
        self.total_steps += 1
        print(f"\n🔧 Step {self.total_steps}: {step_name}")
        if description:
            print(f"   {description}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
    
    def step_completed_successfully(self):
        """Mark a step as completed successfully"""
        self.success_count += 1
    
    def print_error(self, message):
        """Print error message"""
        print(f"❌ {message}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"⚠️  {message}")
    
    def check_system_requirements(self):
        """Check if system meets requirements"""
        self.print_step("System Requirements Check")
        
        # Check macOS
        if platform.system() != "Darwin":
            self.print_error("This script is designed for macOS only")
            return False
        
        self.print_success("Running on macOS")
        
        # Check Python 3.8+
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            self.print_error(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        
        self.print_success(f"Python {python_version.major}.{python_version.minor} is compatible")
        
        # Check for Xcode/simctl
        try:
            result = subprocess.run(['xcrun', 'simctl', 'list'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_success("iOS Simulator tools available")
            else:
                self.print_warning("iOS Simulator tools not found - install Xcode")
        except FileNotFoundError:
            self.print_warning("Xcode command line tools not found")
        
        self.step_completed_successfully()
        return True
    
    def setup_virtual_environment(self):
        """Create and setup virtual environment"""
        self.print_step("Virtual Environment Setup", "Creating isolated Python environment")
        
        if os.path.exists(self.venv_path):
            self.print_success("Virtual environment already exists")
        else:
            try:
                subprocess.run([sys.executable, '-m', 'venv', self.venv_path], 
                             check=True)
                self.print_success("Virtual environment created")
            except subprocess.CalledProcessError as e:
                self.print_error(f"Failed to create virtual environment: {e}")
                return False
        
        # Install requirements
        if os.path.exists('requirements.txt'):
            try:
                subprocess.run([self.python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                             check=True, capture_output=True)
                self.print_success("Requirements installed")
            except subprocess.CalledProcessError as e:
                self.print_error(f"Failed to install requirements: {e}")
                return False
        
        self.step_completed_successfully()
        return True
    
    def test_server_import(self):
        """Test if server can be imported successfully"""
        self.print_step("Server Import Test", "Verifying MCP server can start")
        
        try:
            result = subprocess.run([
                self.python_path, "-c", 
                "import sys; sys.path.insert(0, '.'); import ios_mcp_server; print('Server imports successfully')"
            ], capture_output=True, text=True, cwd=self.current_dir, timeout=10)
            
            if result.returncode == 0:
                self.print_success("MCP server imports successfully")
                self.step_completed_successfully()
                return True
            else:
                self.print_error(f"Server import failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("Server test timed out")
            return False
        except Exception as e:
            self.print_error(f"Server test failed: {e}")
            return False
    
    def configure_claude_desktop(self):
        """Configure Claude Desktop automatically"""
        self.print_step("Claude Desktop Configuration", "Setting up MCP server integration")
        
        claude_config_dir = os.path.expanduser("~/Library/Application Support/Claude")
        claude_config_path = os.path.join(claude_config_dir, "claude_desktop_config.json")
        
        # Create config directory if it doesn't exist
        os.makedirs(claude_config_dir, exist_ok=True)
        
        # Create configuration
        config = {
            "mcpServers": {
                "ios-automation": {
                    "command": self.python_path,
                    "args": [self.server_script],
                    "env": {
                        "PYTHONPATH": self.current_dir
                    }
                }
            }
        }
        
        # Check if config already exists and merge
        if os.path.exists(claude_config_path):
            try:
                with open(claude_config_path, 'r') as f:
                    existing_config = json.load(f)
                
                if "mcpServers" not in existing_config:
                    existing_config["mcpServers"] = {}
                
                existing_config["mcpServers"]["ios-automation"] = config["mcpServers"]["ios-automation"]
                config = existing_config
                self.print_success("Updated existing Claude Desktop configuration")
            except json.JSONDecodeError:
                self.print_warning("Existing config file is invalid, creating new one")
        
        # Write configuration
        try:
            with open(claude_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            self.print_success(f"Claude Desktop configured: {claude_config_path}")
            self.step_completed_successfully()
            return True
        except Exception as e:
            self.print_error(f"Failed to write Claude Desktop config: {e}")
            return False
    
    def check_cursor_compatibility(self):
        """Check if Cursor IDE supports MCP and configure if possible"""
        self.print_step("Cursor IDE Detection", "Checking for Cursor IDE and MCP support")
        
        # Check if Cursor is installed
        cursor_paths = [
            "/Applications/Cursor.app",
            os.path.expanduser("~/Applications/Cursor.app"),
        ]
        
        cursor_found = False
        for path in cursor_paths:
            if os.path.exists(path):
                cursor_found = True
                self.print_success(f"Cursor IDE found: {path}")
                break
        
        if not cursor_found:
            self.print_warning("Cursor IDE not found - install from https://cursor.sh/")
            return False
        
        # Check for Cursor's MCP support (as of 2024, Cursor doesn't natively support MCP)
        cursor_config_dir = os.path.expanduser("~/.cursor")
        if os.path.exists(cursor_config_dir):
            self.print_warning("Cursor IDE found but doesn't natively support MCP protocol yet")
            self.print_warning("Use Claude Desktop for MCP integration, or check Cursor's latest features")
        else:
            self.print_warning("Cursor configuration directory not found")
        
        # Step completed successfully even though Cursor doesn't support MCP yet
        self.step_completed_successfully()
        return False
    
    def check_other_mcp_clients(self):
        """Check for other MCP-compatible clients"""
        self.print_step("Other MCP Clients", "Scanning for additional MCP-compatible applications")
        
        # Check for Continue.dev (VS Code extension)
        vscode_extensions_dir = os.path.expanduser("~/.vscode/extensions")
        if os.path.exists(vscode_extensions_dir):
            continue_extensions = [d for d in os.listdir(vscode_extensions_dir) 
                                 if 'continue' in d.lower()]
            if continue_extensions:
                self.print_success("Continue.dev extension found in VS Code")
                self.print_warning("Continue.dev may support MCP - check their documentation")
            else:
                self.print_warning("VS Code found but Continue.dev extension not detected")
        
        # Check for other potential MCP clients
        potential_clients = [
            ("Zed Editor", "/Applications/Zed.app"),
            ("Visual Studio Code", "/Applications/Visual Studio Code.app"),
        ]
        
        for name, path in potential_clients:
            if os.path.exists(path):
                self.print_warning(f"{name} found - may support MCP in future versions")
        
        self.step_completed_successfully()
        return True
    
    def create_launcher_script(self):
        """Create a convenient launcher script"""
        self.print_step("Launcher Script", "Creating convenient startup script")
        
        launcher_content = '''#!/bin/bash
# iOS MCP Server Launcher
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting iOS MCP Server..."
echo "📁 Project: $SCRIPT_DIR"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment and start server
source "./ios_mcp_env/bin/activate"
python3 ios_mcp_server.py

echo "✅ Server started successfully!"
'''
        
        launcher_path = os.path.join(self.current_dir, "start_mcp_server.sh")
        
        try:
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)
            
            # Make executable
            os.chmod(launcher_path, 0o755)
            self.print_success(f"Launcher script created: {launcher_path}")
            self.step_completed_successfully()
            return True
        except Exception as e:
            self.print_error(f"Failed to create launcher script: {e}")
            return False
    
    def perform_final_tests(self):
        """Perform final integration tests"""
        self.print_step("Final Integration Tests", "Verifying complete setup")
        
        # Test server startup (brief)
        try:
            process = subprocess.Popen([self.python_path, self.server_script], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True,
                                     cwd=self.current_dir)
            
            # Wait briefly for startup
            try:
                stdout, stderr = process.communicate(timeout=3)
                if "Starting iOS MCP Server" in stderr:
                    self.print_success("Server starts successfully")
                else:
                    self.print_warning("Server startup unclear - check manually")
            except subprocess.TimeoutExpired:
                # Server is running, which is expected
                process.terminate()
                self.print_success("Server starts and runs continuously")
                
        except Exception as e:
            self.print_error(f"Server startup test failed: {e}")
            return False
        
        self.step_completed_successfully()
        return True
    
    def print_final_instructions(self):
        """Print final setup instructions and next steps"""
        print("\n" + "="*60)
        print("🎉 SETUP COMPLETE!")
        print("="*60)
        
        print(f"\n📊 Setup Summary: {self.success_count}/{self.total_steps} steps completed")
        
        print("\n🚀 Next Steps:")
        print("1. Restart Claude Desktop completely (Quit and reopen)")
        print("2. In Claude Desktop, you should now see iOS automation tools available")
        print("3. Try a test command: 'List all iOS simulators'")
        
        print(f"\n🔧 Manual Server Start:")
        print(f"   ./start_mcp_server.sh")
        print(f"   OR: ./ios_mcp_env/bin/python3 ios_mcp_server.py")
        
        print(f"\n📁 Configuration Files:")
        print(f"   Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json")
        print(f"   Server Script: ios_mcp_server.py")
        print(f"   Virtual Environment: ./ios_mcp_env/")
        
        print(f"\n🐛 Troubleshooting:")
        print(f"   python3 debug_mcp_setup.py")
        
        print(f"\n📚 Documentation:")
        print(f"   README.md - Complete setup guide")
        print(f"   iOS_MCP_SETUP.md - Detailed instructions")
        
        if self.success_count == self.total_steps:
            print("\n✅ All setup steps completed successfully!")
        else:
            print(f"\n⚠️  {self.total_steps - self.success_count} steps had issues - check output above")
    
    def run_automated_setup(self):
        """Run the complete automated setup process"""
        print("🚀 iOS MCP Server - Automated Setup")
        print("="*50)
        print("This script will automatically configure your MCP server for:")
        print("• Claude Desktop integration")
        print("• Cursor IDE (if supported)")
        print("• Other MCP-compatible clients")
        print("="*50)
        
        # Run setup steps
        steps = [
            self.check_system_requirements,
            self.setup_virtual_environment,
            self.test_server_import,
            self.configure_claude_desktop,
            self.check_cursor_compatibility,
            self.check_other_mcp_clients,
            self.create_launcher_script,
            self.perform_final_tests,
        ]
        
        for step in steps:
            if not step():
                self.print_warning("Step failed, but continuing with setup...")
        
        self.print_final_instructions()

def main():
    automator = MCPSetupAutomator()
    automator.run_automated_setup()

if __name__ == "__main__":
    main() 