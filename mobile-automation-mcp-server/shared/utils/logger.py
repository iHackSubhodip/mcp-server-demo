"""
Shared logging utilities for cross-platform automation.

This module provides colored logging with emojis for better terminal output
across iOS, Android, and other automation platforms.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Add the mobile-automation-mcp-server directory to sys.path
mobile_automation_mcp_server_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(mobile_automation_mcp_server_dir))

from config.settings import settings


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log levels for better readability
    in terminal output.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green  
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors and emojis for better UX."""
        
        # Add emoji indicators for different log levels
        emoji_map = {
            'DEBUG': '🔍',
            'INFO': '✅', 
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '💥'
        }
        
        # Get color and emoji for this log level
        color = self.COLORS.get(record.levelname, '')
        reset = self.COLORS['RESET']
        emoji = emoji_map.get(record.levelname, '📝')
        
        # Create colored log message
        colored_levelname = f"{color}{record.levelname}{reset}"
        record.levelname = colored_levelname
        
        # Format the message with emoji
        formatted = super().format(record)
        return f"{emoji} {formatted}"


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting and output configuration.
    
    Args:
        name: Logger name (usually __name__ of the module)
        level: Log level override (defaults to settings.server.log_level)
        
    Returns:
        Configured logger instance
    """
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Set log level from config or parameter
    log_level = level or settings.server.log_level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create console handler with colored formatter
    console_handler = logging.StreamHandler(sys.stderr)  # Use stderr to avoid MCP stdout issues
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter with timestamp and module info
    formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.
    
    This is the main function that should be used throughout the application.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return setup_logger(name) 