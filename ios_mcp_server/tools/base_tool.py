"""
Base tool class for iOS automation tools.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.exceptions import ToolExecutionError, ValidationError


@dataclass
class ToolArgument:
    """
    Definition of a tool argument with validation rules.
    
    This provides a structured way to define tool parameters
    with built-in validation and documentation.
    """
    
    name: str
    type: str  # "string", "number", "boolean", "object", "array"
    description: str
    required: bool = True
    default: Any = None
    enum: Optional[List[Any]] = None
    pattern: Optional[str] = None  # Regex pattern for string validation
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Convert to JSON Schema format for MCP tool definition."""
        schema = {
            "type": self.type,
            "description": self.description
        }
        
        if self.enum:
            schema["enum"] = self.enum
        
        if self.pattern and self.type == "string":
            schema["pattern"] = self.pattern
        
        if self.default is not None:
            schema["default"] = self.default
        
        return schema


class BaseTool:
    """
    Abstract base class for all MCP tools.
    
    This class implements the Template Method pattern, providing a
    consistent structure for tool execution while allowing subclasses
    to implement their specific logic.
    
    The execution flow is:
    1. validate_arguments() - Validate input parameters
    2. execute_impl() - Perform the actual tool operation
    3. Format and return results
    """
    
    def __init__(self):
        """Initialize the base tool."""
        self.logger = get_logger(self.__class__.__name__)
    
    @property
    def name(self) -> str:
        """Return the tool name for MCP registration."""
        pass
    
    @property
    def description(self) -> str:
        """Return the tool description for MCP registration."""
        pass
    
    @property
    def arguments(self) -> List[ToolArgument]:
        """Return the list of tool arguments."""
        pass
    
    async def execute_impl(self, **kwargs) -> Dict[str, Any]:
        """
        Implement the actual tool functionality.
        
        This method should be overridden by subclasses to provide
        the specific tool behavior.
        
        Args:
            **kwargs: Validated tool arguments
            
        Returns:
            Dictionary with tool execution results
            
        Raises:
            Any exception that occurs during execution
        """
        pass
    
    def validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate tool arguments against the defined schema.
        
        This method performs comprehensive validation including:
        - Required argument checking
        - Type validation
        - Enum value validation
        - Pattern matching for strings
        
        Args:
            arguments: Raw arguments from MCP call
            
        Returns:
            Validated and normalized arguments
            
        Raises:
            ValidationError: If validation fails
        """
        
        validated = {}
        
        # Create a lookup for argument definitions
        arg_defs = {arg.name: arg for arg in self.arguments}
        
        # Check for required arguments
        for arg_def in self.arguments:
            if arg_def.required and arg_def.name not in arguments:
                if arg_def.default is not None:
                    validated[arg_def.name] = arg_def.default
                else:
                    raise ValidationError(
                        f"Required argument '{arg_def.name}' is missing",
                        context={"tool": self.name, "missing_arg": arg_def.name}
                    )
        
        # Validate provided arguments
        for arg_name, arg_value in arguments.items():
            if arg_name not in arg_defs:
                self.logger.warning(f"⚠️ Unknown argument '{arg_name}' ignored")
                continue
            
            arg_def = arg_defs[arg_name]
            
            # Type validation
            if not self._validate_type(arg_value, arg_def.type):
                raise ValidationError(
                    f"Argument '{arg_name}' must be of type {arg_def.type}",
                    context={
                        "tool": self.name,
                        "argument": arg_name,
                        "expected_type": arg_def.type,
                        "actual_type": type(arg_value).__name__,
                        "value": str(arg_value)[:100]  # Truncate for safety
                    }
                )
            
            # Enum validation
            if arg_def.enum and arg_value not in arg_def.enum:
                raise ValidationError(
                    f"Argument '{arg_name}' must be one of: {arg_def.enum}",
                    context={
                        "tool": self.name,
                        "argument": arg_name,
                        "allowed_values": arg_def.enum,
                        "provided_value": arg_value
                    }
                )
            
            # Pattern validation for strings
            if arg_def.pattern and arg_def.type == "string":
                import re
                if not re.match(arg_def.pattern, str(arg_value)):
                    raise ValidationError(
                        f"Argument '{arg_name}' does not match required pattern",
                        context={
                            "tool": self.name,
                            "argument": arg_name,
                            "pattern": arg_def.pattern,
                            "value": str(arg_value)
                        }
                    )
            
            validated[arg_name] = arg_value
        
        return validated
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """
        Validate that a value matches the expected type.
        
        Args:
            value: Value to validate
            expected_type: Expected type string
            
        Returns:
            True if type matches, False otherwise
        """
        
        type_mapping = {
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type is None:
            self.logger.warning(f"⚠️ Unknown type '{expected_type}', skipping validation")
            return True
        
        return isinstance(value, expected_python_type)
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with the provided arguments.
        
        This is the main entry point for tool execution and implements
        the Template Method pattern.
        
        Args:
            arguments: Raw arguments from MCP call
            
        Returns:
            Standardized tool execution results
        """
        
        self.logger.info(f"🔧 Executing tool: {self.name}")
        self.logger.debug(f"📥 Arguments: {arguments}")
        
        try:
            # Step 1: Validate arguments
            validated_args = self.validate_arguments(arguments)
            self.logger.debug(f"✅ Arguments validated: {list(validated_args.keys())}")
            
            # Step 2: Execute the tool implementation
            result = await self.execute_impl(**validated_args)
            
            # Step 3: Ensure result has standard format
            if not isinstance(result, dict):
                result = {"result": result}
            
            # Add metadata
            result.setdefault("success", True)
            result.setdefault("tool_name", self.name)
            
            self.logger.info(f"✅ Tool execution completed: {self.name}")
            return result
            
        except ValidationError as e:
            self.logger.error(f"❌ Validation error in {self.name}: {e}")
            raise ToolExecutionError(self.name, str(e), e)
        
        except Exception as e:
            self.logger.error(f"❌ Execution error in {self.name}: {e}")
            raise ToolExecutionError(self.name, f"Tool execution failed: {str(e)}", e)
    
    def to_mcp_tool_definition(self) -> Dict[str, Any]:
        """
        Convert tool definition to MCP tool format.
        
        Returns:
            MCP tool definition dictionary
        """
        
        # Build properties for required and optional arguments
        properties = {}
        required = []
        
        for arg in self.arguments:
            properties[arg.name] = arg.to_json_schema()
            if arg.required and arg.default is None:
                required.append(arg.name)
        
        definition = {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": properties
            }
        }
        
        if required:
            definition["inputSchema"]["required"] = required
        
        return definition 