"""
iOS MCP Server - Modern iOS automation server built with FastMCP 2.0
"""

__version__ = "1.0.0"
__author__ = "iHackSubhodip"
__email__ = "write2subhodip@gmail.com"

# Make the package importable without running the server
try:
    from .fastmcp_server import mcp
    __all__ = ["mcp"]
except ImportError:
    # Allow package to be built even if dependencies aren't available
    __all__ = []
