"""
Main configuration settings for Mobile automation iOS MCP server.

This module combines shared and platform-specific configurations,
providing a unified interface while supporting the new modular structure.
"""

import sys
from pathlib import Path

# Add the mobile-automation-mcp-server directory to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared configuration classes and factories
from shared.config import (
    AppiumConfig,
    ServerConfig,
    create_appium_config,
    create_server_config
)

# Import iOS-specific configuration classes and factories  
from platforms.ios.config import (
    iOSConfig,
    create_ios_config
)


class Settings:
    """
    Main settings class that combines shared and platform-specific configurations.
    
    This class maintains the same interface as before while internally using
    the new modular configuration structure. It loads configuration from 
    environment variables with sensible defaults following 12-factor app methodology.
    """
    
    def __init__(self):
        # Create shared configurations
        self.appium = create_appium_config()
        self.server = create_server_config(platform_name="ios")
        
        # Create iOS-specific configuration
        self.ios = create_ios_config()


# Global settings instance - maintains backward compatibility
settings = Settings() 