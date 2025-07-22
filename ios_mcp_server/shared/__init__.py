"""
Shared modules for cross-platform MCP automation.

This package contains utilities, configuration, and patterns that can be
shared between iOS, Android, and other automation platforms.

Structure:
- utils/: Platform-agnostic utilities (logging, command execution, exceptions)
- config/: Base configuration classes and patterns
- patterns/: Reusable patterns for FastMCP servers and tools
"""

__version__ = "2.0.0"
__all__ = ["utils", "config", "patterns"]
