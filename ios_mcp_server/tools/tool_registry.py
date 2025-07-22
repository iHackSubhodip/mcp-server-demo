"""
Tool registry for managing MCP tools.

This module provides a centralized registry for all available MCP tools,
implementing the Registry pattern for clean tool management.
"""

import sys
from pathlib import Path
from typing import Dict, List, Type, Optional
from abc import ABC

# Add the ios_mcp_server directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .base_tool import BaseTool
from .ios.appium_tap_type_tool import AppiumTapTypeTool
from .ios.screenshot_tool import ScreenshotTool
from .ios.launch_app_tool import LaunchAppTool
from .ios.find_and_tap_tool import FindAndTapTool
from utils.logger import get_logger

logger = get_logger(__name__)


class ToolRegistry:
    """
    Registry for managing all available MCP tools.
    
    This class implements the Registry pattern, providing a centralized
    way to register, discover, and access all available tools.
    """
    
    def __init__(self):
        """Initialize the tool registry."""
        self.logger = get_logger(__name__)
        self._tools: Dict[str, BaseTool] = {}
        self._tool_classes: Dict[str, Type[BaseTool]] = {}
        
        # Register all available tools
        self._register_builtin_tools()
    
    def _register_builtin_tools(self) -> None:
        """
        Register all built-in tools.
        
        This method automatically registers all the core tools that
        are part of the iOS MCP server.
        """
        
        # Define all available tool classes
        builtin_tools = [
            AppiumTapTypeTool,
            ScreenshotTool,
            LaunchAppTool,
            FindAndTapTool,
        ]
        
        self.logger.info(f"🔧 Registering {len(builtin_tools)} built-in tools")
        
        # Register each tool class
        for tool_class in builtin_tools:
            try:
                self.register_tool_class(tool_class)
                self.logger.debug(f"✅ Registered tool class: {tool_class.__name__}")
            except Exception as e:
                self.logger.error(f"❌ Failed to register tool {tool_class.__name__}: {e}")
        
        self.logger.info(f"✅ Tool registration complete: {len(self._tools)} tools available")
    
    def register_tool_class(self, tool_class: Type[BaseTool]) -> None:
        """
        Register a tool class in the registry.
        
        Args:
            tool_class: The tool class to register
            
        Raises:
            ValueError: If tool class is invalid or name conflicts exist
        """
        
        if not issubclass(tool_class, BaseTool):
            raise ValueError(f"Tool class {tool_class.__name__} must inherit from BaseTool")
        
        # Create an instance to get the tool name
        try:
            tool_instance = tool_class()
            tool_name = tool_instance.name
        except Exception as e:
            raise ValueError(f"Failed to instantiate tool {tool_class.__name__}: {e}")
        
        # Check for name conflicts
        if tool_name in self._tools:
            raise ValueError(f"Tool with name '{tool_name}' is already registered")
        
        # Register the tool
        self._tool_classes[tool_name] = tool_class
        self._tools[tool_name] = tool_instance
        
        self.logger.debug(f"🔧 Registered tool: {tool_name}")
    
    def register_tool_instance(self, tool_instance: BaseTool) -> None:
        """
        Register a tool instance directly in the registry.
        
        Args:
            tool_instance: The tool instance to register
            
        Raises:
            ValueError: If tool instance is invalid or name conflicts exist
        """
        
        if not isinstance(tool_instance, BaseTool):
            raise ValueError("Tool must be an instance of BaseTool")
        
        tool_name = tool_instance.name
        
        # Check for name conflicts
        if tool_name in self._tools:
            raise ValueError(f"Tool with name '{tool_name}' is already registered")
        
        # Register the tool
        self._tool_classes[tool_name] = type(tool_instance)
        self._tools[tool_name] = tool_instance
        
        self.logger.debug(f"🔧 Registered tool instance: {tool_name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool instance by name.
        
        Args:
            name: The tool name
            
        Returns:
            Tool instance if found, None otherwise
        """
        
        return self._tools.get(name)
    
    def get_all_tools(self) -> Dict[str, BaseTool]:
        """
        Get all registered tools.
        
        Returns:
            Dictionary mapping tool names to tool instances
        """
        
        return self._tools.copy()
    
    def get_tool_names(self) -> List[str]:
        """
        Get all registered tool names.
        
        Returns:
            List of tool names
        """
        
        return list(self._tools.keys())
    
    def has_tool(self, name: str) -> bool:
        """
        Check if a tool is registered.
        
        Args:
            name: The tool name to check
            
        Returns:
            True if tool is registered, False otherwise
        """
        
        return name in self._tools
    
    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool from the registry.
        
        Args:
            name: The tool name to unregister
            
        Returns:
            True if tool was unregistered, False if not found
        """
        
        if name not in self._tools:
            return False
        
        del self._tools[name]
        del self._tool_classes[name]
        
        self.logger.debug(f"🗑️ Unregistered tool: {name}")
        return True
    
    def get_mcp_tool_definitions(self) -> List[Dict[str, any]]:
        """
        Get MCP tool definitions for all registered tools.
        
        This method returns the tool definitions in the format
        required by the MCP protocol.
        
        Returns:
            List of MCP tool definition dictionaries
        """
        
        definitions = []
        
        for tool_name, tool_instance in self._tools.items():
            try:
                definition = tool_instance.to_mcp_tool_definition()
                definitions.append(definition)
                self.logger.debug(f"📋 Generated MCP definition for: {tool_name}")
            except Exception as e:
                self.logger.error(f"❌ Failed to generate MCP definition for {tool_name}: {e}")
        
        self.logger.info(f"📋 Generated {len(definitions)} MCP tool definitions")
        return definitions
    
    def get_tool_info(self) -> Dict[str, Dict[str, any]]:
        """
        Get detailed information about all registered tools.
        
        Returns:
            Dictionary with tool information including descriptions and arguments
        """
        
        info = {}
        
        for tool_name, tool_instance in self._tools.items():
            try:
                info[tool_name] = {
                    "name": tool_instance.name,
                    "description": tool_instance.description,
                    "class_name": type(tool_instance).__name__,
                    "argument_count": len(tool_instance.arguments),
                    "arguments": [
                        {
                            "name": arg.name,
                            "type": arg.type,
                            "required": arg.required,
                            "description": arg.description
                        }
                        for arg in tool_instance.arguments
                    ]
                }
            except Exception as e:
                self.logger.error(f"❌ Failed to get info for tool {tool_name}: {e}")
                info[tool_name] = {
                    "name": tool_name,
                    "error": str(e)
                }
        
        return info
    
    def validate_all_tools(self) -> Dict[str, bool]:
        """
        Validate all registered tools.
        
        This method performs basic validation on all tools to ensure
        they are properly configured and functional.
        
        Returns:
            Dictionary mapping tool names to validation results
        """
        
        results = {}
        
        for tool_name, tool_instance in self._tools.items():
            try:
                # Basic validation checks
                assert tool_instance.name, "Tool name cannot be empty"
                assert tool_instance.description, "Tool description cannot be empty"
                assert isinstance(tool_instance.arguments, list), "Arguments must be a list"
                
                # Try to generate MCP definition
                definition = tool_instance.to_mcp_tool_definition()
                assert "name" in definition, "MCP definition must have name"
                assert "description" in definition, "MCP definition must have description"
                
                results[tool_name] = True
                self.logger.debug(f"✅ Tool validation passed: {tool_name}")
                
            except Exception as e:
                results[tool_name] = False
                self.logger.error(f"❌ Tool validation failed for {tool_name}: {e}")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        self.logger.info(f"🔍 Tool validation complete: {passed}/{total} tools passed")
        
        return results


# Global tool registry instance
tool_registry = ToolRegistry() 