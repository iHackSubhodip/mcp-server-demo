#!/usr/bin/env python3
"""
MCP Setup Diagnostic Script
Helps debug iOS MCP Server configuration issues
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and is accessible"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def check_executable(filepath):
    """Check if a file is executable"""
    if os.access(filepath, os.X_OK):
        print(f"✅ Executable: {filepath}")
        return True
    else:
        print(f"❌ Not executable: {filepath}")
        return False

def main():
    print("🔍 iOS MCP Server Setup Diagnostic")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check virtual environment
    venv_python = os.path.join(current_dir, "ios_mcp_env", "bin", "python3")
    venv_exists = check_file_exists(venv_python, "Virtual Environment Python")
    
    if venv_exists:
        check_executable(venv_python)
    
    # Check MCP server script
    mcp_script = os.path.join(current_dir, "ios_mcp_server.py")
    script_exists = check_file_exists(mcp_script, "MCP Server Script")
    
    # Check Claude Desktop config
    claude_config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    config_exists = check_file_exists(claude_config_path, "Claude Desktop Config")
    
    if config_exists:
        try:
            with open(claude_config_path, 'r') as f:
                config = json.load(f)
            
            print("\n📋 Claude Desktop Configuration:")
            if "mcpServers" in config:
                for server_name, server_config in config["mcpServers"].items():
                    print(f"  Server: {server_name}")
                    command = server_config.get("command", "")
                    args = server_config.get("args", [])
                    
                    print(f"    Command: {command}")
                    if args:
                        print(f"    Args: {args}")
                    
                    # Verify paths exist
                    check_file_exists(command, f"    Command Path")
                    if args:
                        for arg in args:
                            if arg.endswith('.py'):
                                check_file_exists(arg, f"    Script Path")
            else:
                print("  ❌ No mcpServers configuration found")
                
        except Exception as e:
            print(f"  ❌ Error reading config: {e}")
    
    # Test MCP module import
    print("\n🐍 Python Environment Check:")
    try:
        # Try to find site-packages directory
        possible_paths = [
            os.path.join(current_dir, "ios_mcp_env", "lib", "python3.13", "site-packages"),
            os.path.join(current_dir, "ios_mcp_env", "lib", "python3.12", "site-packages"),
            os.path.join(current_dir, "ios_mcp_env", "lib", "python3.11", "site-packages"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                sys.path.insert(0, path)
                break
        
        import mcp
        print("✅ MCP module can be imported")
        print(f"  MCP version: {getattr(mcp, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"❌ Cannot import MCP module: {e}")
        print("  Try: pip install mcp")
    
    # Test server startup
    print("\n🚀 Server Startup Test:")
    if venv_exists and script_exists:
        try:
            # Test if server can import without running
            result = subprocess.run([
                venv_python, "-c", 
                "import sys; sys.path.insert(0, '.'); import ios_mcp_server; print('✅ Server imports successfully')"
            ], capture_output=True, text=True, cwd=current_dir, timeout=10)
            
            if result.returncode == 0:
                print("✅ Server script imports successfully")
            else:
                print(f"❌ Server import failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Server test timed out")
        except Exception as e:
            print(f"❌ Server test failed: {e}")
    
    print("\n📝 Recommended Actions:")
    print("1. Restart Claude Desktop completely")
    print("2. Check that all paths in config use absolute paths")
    print("3. Verify Terminal has accessibility permissions")
    print("4. Check Claude Desktop logs: ~/Library/Logs/Claude/")
    
    print(f"\n💡 Your configuration should use these paths:")
    print(f"   Command: {venv_python}")
    print(f"   Args: [\"{mcp_script}\"]")
    print(f"   PYTHONPATH: \"{current_dir}\"")

if __name__ == "__main__":
    main() 