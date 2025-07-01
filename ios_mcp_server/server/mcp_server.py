"""
Main MCP server implementation for iOS automation.

This module provides the core MCP server functionality, handling
protocol communication and tool execution.
"""

import asyncio
import json
import sys
from typing import Dict, Any, List, Optional

from mcp.server import Server
from mcp.types import Tool as MCPTool, TextContent

from ..tools.tool_registry import tool_registry
from ..config.settings import settings
from ..utils.logger import get_logger
from ..utils.exceptions import ToolExecutionError

logger = get_logger(__name__)


class iOSMCPServer:
    """
    Main MCP server for iOS automation.
    
    This class implements the MCP protocol for iOS automation tools,
    providing a clean interface between Claude Desktop and iOS automation
    capabilities.
    """
    
    def __init__(self):
        """Initialize the iOS MCP server."""
        self.logger = get_logger(__name__)
        self.server = Server(settings.server.name)
        self.tool_registry = tool_registry
        
        # Setup MCP server handlers
        self._setup_handlers()
        
        self.logger.info(f"🚀 iOS MCP Server initialized: {settings.server.name} v{settings.server.version}")
    
    def _setup_handlers(self) -> None:
        """
        Set up MCP protocol handlers.
        
        This method registers all the necessary handlers for the MCP protocol
        including tool listing and execution.
        """
        
        # Register tools list handler
        @self.server.list_tools()
        async def list_tools() -> List[MCPTool]:
            """
            Handle MCP tools list request.
            
            Returns:
                List of available tools in MCP format
            """
            
            self.logger.info("📋 Listing available tools")
            
            try:
                # Get tool definitions from registry
                tool_definitions = self.tool_registry.get_mcp_tool_definitions()
                
                # Convert to MCP Tool objects
                mcp_tools = []
                for definition in tool_definitions:
                    mcp_tool = MCPTool(
                        name=definition["name"],
                        description=definition["description"],
                        inputSchema=definition["inputSchema"]
                    )
                    mcp_tools.append(mcp_tool)
                
                self.logger.info(f"✅ Returning {len(mcp_tools)} available tools")
                return mcp_tools
                
            except Exception as e:
                self.logger.error(f"❌ Error listing tools: {e}")
                # Return empty list on error to avoid breaking MCP protocol
                return []
        
        # Register tool call handler
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """
            Handle MCP tool execution request.
            
            Args:
                name: Tool name to execute
                arguments: Tool arguments
                
            Returns:
                List of text content with execution results
            """
            
            self.logger.info(f"🔧 Tool call request: {name}")
            self.logger.debug(f"📥 Arguments: {arguments}")
            
            try:
                # Get tool from registry
                tool = self.tool_registry.get_tool(name)
                if not tool:
                    error_msg = f"Tool '{name}' not found"
                    self.logger.error(f"❌ {error_msg}")
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": error_msg,
                            "available_tools": self.tool_registry.get_tool_names()
                        }, indent=2)
                    )]
                
                # Execute the tool
                result = await tool.execute(arguments)
                
                # Format result as JSON for better readability
                result_text = json.dumps(result, indent=2, default=str)
                
                if result.get("success", True):
                    self.logger.info(f"✅ Tool execution completed: {name}")
                else:
                    self.logger.warning(f"⚠️ Tool execution failed: {name}")
                
                return [TextContent(type="text", text=result_text)]
                
            except ToolExecutionError as e:
                self.logger.error(f"❌ Tool execution error: {e}")
                
                error_result = {
                    "success": False,
                    "error": str(e),
                    "tool_name": name,
                    "context": getattr(e, 'context', {}),
                    "suggestions": [
                        "Check tool arguments are correct",
                        "Verify required services are running (Appium, iOS Simulator)",
                        "Review server logs for detailed error information"
                    ]
                }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(error_result, indent=2, default=str)
                )]
                
            except Exception as e:
                self.logger.error(f"❌ Unexpected error executing tool {name}: {e}")
                
                error_result = {
                    "success": False,
                    "error": f"Unexpected error: {str(e)}",
                    "tool_name": name,
                    "error_type": type(e).__name__,
                    "suggestions": [
                        "Check server logs for detailed error information",
                        "Verify all dependencies are properly installed",
                        "Try restarting the MCP server"
                    ]
                }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(error_result, indent=2, default=str)
                )]
        
        self.logger.info("✅ MCP handlers registered successfully")
    
    async def run(self) -> None:
        """
        Run the MCP server.
        
        This method starts the server and handles the MCP protocol
        communication with Claude Desktop.
        """
        
        self.logger.info("🚀 Starting iOS MCP Server")
        
        try:
            # Validate tools before starting
            validation_results = self.tool_registry.validate_all_tools()
            failed_tools = [name for name, passed in validation_results.items() if not passed]
            
            if failed_tools:
                self.logger.warning(f"⚠️ Some tools failed validation: {failed_tools}")
            else:
                self.logger.info("✅ All tools validated successfully")
            
            # Log available tools
            tool_names = self.tool_registry.get_tool_names()
            self.logger.info(f"🔧 Available tools: {', '.join(tool_names)}")
            
            # Start the server
            self.logger.info("🔌 Connecting to Claude Desktop - Server ready!")
            
            # Run the server (this will handle stdin/stdout communication)
            import mcp.server.stdio
            from mcp.server import InitializationOptions, NotificationOptions
            
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name=settings.server.name,
                        server_version=settings.server.version,
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
                
        except KeyboardInterrupt:
            self.logger.info("⏹️ Server stopped by user")
        except Exception as e:
            self.logger.error(f"💥 Server error: {e}")
            raise
        finally:
            self.logger.info("🔌 iOS MCP Server shutdown complete")
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the server and its capabilities.
        
        Returns:
            Dictionary with server information
        """
        
        tool_info = self.tool_registry.get_tool_info()
        
        return {
            "server": {
                "name": settings.server.name,
                "version": settings.server.version,
                "log_level": settings.server.log_level
            },
            "configuration": {
                "appium_url": settings.appium.url,
                "ios_platform": f"{settings.ios.platform_name} {settings.ios.platform_version}",
                "device_name": settings.ios.device_name,
                "default_bundle_id": settings.ios.default_bundle_id
            },
            "tools": {
                "count": len(tool_info),
                "names": list(tool_info.keys()),
                "details": tool_info
            },
            "capabilities": [
                "Real iOS automation using Appium",
                "Screenshot capture",
                "App launching and management",
                "Text input automation",
                "Comprehensive error handling and logging"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the server and its dependencies.
        
        Returns:
            Dictionary with health check results
        """
        
        health = {
            "server": "healthy",
            "tools": "unknown",
            "appium": "unknown",
            "simulator": "unknown",
            "overall": "unknown"
        }
        
        try:
            # Check tools
            validation_results = self.tool_registry.validate_all_tools()
            all_tools_valid = all(validation_results.values())
            health["tools"] = "healthy" if all_tools_valid else "degraded"
            
            # Check Appium connectivity (basic check)
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    timeout = aiohttp.ClientTimeout(total=5)
                    async with session.get(f"{settings.appium.url}/status", timeout=timeout) as response:
                        if response.status == 200:
                            health["appium"] = "healthy"
                        else:
                            health["appium"] = "unhealthy"
            except:
                health["appium"] = "unreachable"
            
            # Determine overall health
            if health["tools"] == "healthy" and health["appium"] == "healthy":
                health["overall"] = "healthy"
            elif health["tools"] == "healthy" or health["appium"] == "healthy":
                health["overall"] = "degraded"
            else:
                health["overall"] = "unhealthy"
            
        except Exception as e:
            self.logger.error(f"❌ Health check error: {e}")
            health["overall"] = "error"
            health["error"] = str(e)
        
        return health 