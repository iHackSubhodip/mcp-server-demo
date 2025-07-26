"""
Shared configuration classes for cross-platform MCP automation.

This module contains configuration classes that can be used across
iOS, Android, and other automation platforms.
"""

import os
import sys
from typing import Optional
from dataclasses import dataclass


@dataclass
class AppiumConfig:
    """
    Configuration for Appium server connection.
    
    This configuration works for both iOS (XCUITest) and Android (UIAutomator2)
    automation platforms.
    """
    
    host: str = "localhost"
    port: int = 4723
    timeout: int = 60
    
    @property
    def url(self) -> str:
        """Get the full Appium server URL."""
        return f"http://{self.host}:{self.port}"


@dataclass 
class ServerConfig:
    """
    Configuration for the MCP server itself.
    
    This configuration is platform-agnostic and applies to the
    overall MCP server behavior regardless of target platform.
    """
    
    name: str = "automation-mcp"
    version: str = "2.0.0"
    log_level: str = "INFO"
    
    # Virtual environment path for automation scripts (dynamically determined)
    venv_path: str = ""
    
    # Python version for site-packages path
    python_version: str = ""


def create_appium_config() -> AppiumConfig:
    """
    Create AppiumConfig from environment variables.
    
    Returns:
        AppiumConfig instance with values from environment or defaults
    """
    return AppiumConfig(
        host=os.getenv("APPIUM_HOST", "localhost"),
        port=int(os.getenv("APPIUM_PORT", "4723")),
        timeout=int(os.getenv("APPIUM_TIMEOUT", "60"))
    )


def create_server_config(platform_name: str = "automation") -> ServerConfig:
    """
    Create ServerConfig from environment variables.
    
    Args:
        platform_name: Name of the platform (ios, android, etc.) for default naming
        
    Returns:
        ServerConfig instance with values from environment or defaults
    """
    # Determine paths relative to the project structure
    # This function is in shared/config/, so project root is 3 levels up
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent
    default_venv_path = str(project_root / f"{platform_name}_mcp_env")
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    
    return ServerConfig(
        name=os.getenv("MCP_SERVER_NAME", f"{platform_name}-automation-mcp"),
        version=os.getenv("MCP_SERVER_VERSION", "2.0.0"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        venv_path=os.getenv("VENV_PATH", default_venv_path),
        python_version=os.getenv("PYTHON_VERSION", python_version)
    ) 