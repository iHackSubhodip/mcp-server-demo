"""
Configuration settings for iOS MCP Server.

This module centralizes all configuration values, making the application
easier to configure and deploy in different environments.
"""

import os
import sys
from typing import Optional
from dataclasses import dataclass


@dataclass
class AppiumConfig:
    """Configuration for Appium server connection."""
    
    host: str = "localhost"
    port: int = 4723
    timeout: int = 60
    
    @property
    def url(self) -> str:
        """Get the full Appium server URL."""
        return f"http://{self.host}:{self.port}"


@dataclass
class iOSConfig:
    """Configuration for iOS simulator and device settings."""
    
    platform_name: str = "iOS"
    platform_version: str = "18.2"
    device_name: str = "iPhone 16 Pro"
    automation_name: str = "XCUITest"
    no_reset: bool = True
    new_command_timeout: int = 60
    default_bundle_id: str = "com.apple.mobilesafari"


@dataclass
class ServerConfig:
    """Configuration for the MCP server itself."""
    
    name: str = "ios-automation-mcp"
    version: str = "2.0.0"
    log_level: str = "INFO"
    
    # Virtual environment path for Appium scripts (dynamically determined)
    venv_path: str = ""
    
    # Python version for site-packages path
    python_version: str = ""


class Settings:
    """
    Main settings class that loads configuration from environment variables
    with sensible defaults.
    
    This follows the 12-factor app methodology for configuration management.
    """
    
    def __init__(self):
        # Appium configuration
        self.appium = AppiumConfig(
            host=os.getenv("APPIUM_HOST", "localhost"),
            port=int(os.getenv("APPIUM_PORT", "4723")),
            timeout=int(os.getenv("APPIUM_TIMEOUT", "60"))
        )
        
        # iOS configuration  
        self.ios = iOSConfig(
            platform_version=os.getenv("IOS_PLATFORM_VERSION", "18.2"),
            device_name=os.getenv("IOS_DEVICE_NAME", "iPhone 16 Pro"),
            default_bundle_id=os.getenv("IOS_DEFAULT_BUNDLE_ID", "com.apple.mobilesafari")
        )
        
        # Server configuration
        # Use the directory where this config file is located as the project root
        config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(config_dir)
        default_venv_path = os.path.join(project_root, "ios_mcp_env")
        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        self.server = ServerConfig(
            name=os.getenv("MCP_SERVER_NAME", "ios-automation-mcp"),
            version=os.getenv("MCP_SERVER_VERSION", "2.0.0"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            venv_path=os.getenv("VENV_PATH", default_venv_path),
            python_version=os.getenv("PYTHON_VERSION", python_version)
        )


# Global settings instance
settings = Settings() 