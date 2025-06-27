"""
Main entry point for the iOS MCP Server.

This module provides the main entry point for starting the refactored
iOS MCP server with proper initialization and error handling.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ios_mcp_server.server.mcp_server import iOSMCPServer
from ios_mcp_server.config.settings import settings
from ios_mcp_server.utils.logger import get_logger


def main():
    """
    Main entry point for the iOS MCP Server.
    
    This function initializes and starts the server with proper
    error handling and logging.
    """
    
    # Initialize logger
    logger = get_logger(__name__)
    
    try:
        logger.info("🚀 iOS MCP Server starting up...")
        logger.info(f"📋 Server: {settings.server.name} v{settings.server.version}")
        logger.info(f"🔧 Log level: {settings.server.log_level}")
        logger.info(f"🌐 Appium URL: {settings.appium.url}")
        logger.info(f"📱 iOS Platform: {settings.ios.platform_name} {settings.ios.platform_version}")
        logger.info(f"📲 Device: {settings.ios.device_name}")
        
        # Create and run the server
        server = iOSMCPServer()
        
        # Run the server
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        logger.info("⏹️ Server stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        logger.error("🔍 Check the logs above for more details")
        sys.exit(1)


if __name__ == "__main__":
    main() 