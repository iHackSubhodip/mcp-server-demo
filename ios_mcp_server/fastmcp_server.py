#!/usr/bin/env python3
"""
Modern FastMCP iOS Automation Server

A clean FastMCP 2.0 implementation that leverages all existing iOS automation
services while providing FastMCP's modern, Pythonic interface.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from fastmcp import FastMCP, Context
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

# Add the current directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from automation.screenshot_service import ScreenshotService
from automation.appium_client import AppiumClient  
from automation.simulator_manager import SimulatorManager
from tools.find_and_tap_tool import FindAndTapTool
from config.settings import settings
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="iOS Automation MCP Server",
    description="FastMCP server for iOS automation",
    version="2.0.0"
)

# Initialize FastMCP server with proper naming
mcp = FastMCP(
    name=f"{settings.server.name} (FastMCP)",
    version="2.0.0"
)

# Initialize services only if not in cloud environment
IS_CLOUD = bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("HEROKU_APP_NAME") or os.getenv("GOOGLE_CLOUD_PROJECT"))

if not IS_CLOUD:
    # Initialize local services
    screenshot_service = ScreenshotService()
    appium_client = AppiumClient()
    simulator_manager = SimulatorManager()
    find_and_tap_tool = FindAndTapTool()
    logger.info(f"🚀 FastMCP Server initialized with local services")
else:
    logger.info(f"☁️ FastMCP Server running in cloud mode - local services disabled")

@mcp.tool
async def take_screenshot(
    filename: Optional[str] = None,
    device_id: str = "booted", 
    directory: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Take a screenshot of the iOS simulator using existing screenshot service.
    
    Args:
        filename: Custom filename for screenshot (auto-generated if not provided)
        device_id: iOS simulator device ID (defaults to 'booted')
        directory: Directory to save screenshot (defaults to project screenshots folder)
    
    Returns:
        Screenshot details and status
    """
    if ctx:
        await ctx.info(f"📸 Taking screenshot with FastMCP - Device: {device_id}")
    
    try:
        # Use existing robust screenshot service
        result = await screenshot_service.take_screenshot(
            filename=filename,
            device_id=device_id,
            directory=directory
        )
        
        if ctx:
            await ctx.info(f"✅ Screenshot saved: {result['filename']} ({result.get('size_bytes', 0):,} bytes)")
        
        # Return FastMCP-formatted response
        return {
            "success": True,
            "message": f"Screenshot saved successfully: {result['filename']}",
            "filename": result["filename"],
            "path": result["path"],
            "size_mb": round(result["size_bytes"] / (1024 * 1024), 2),
            "device_id": result["device_id"],
            "timestamp": result["timestamp"],
            "fastmcp": True
        }
        
    except Exception as e:
        error_msg = f"Screenshot failed: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP screenshot error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "device_id": device_id,
            "suggestions": [
                "Ensure iOS Simulator is running and visible",
                "Check device ID is correct",
                "Verify screenshot directory permissions"
            ],
            "fastmcp": True
        }

@mcp.tool  
async def launch_app(
    bundle_id: str,
    device_id: str = "booted",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Launch an iOS application using existing simulator manager.
    
    Args:
        bundle_id: iOS app bundle identifier (e.g., com.apple.mobilesafari)
        device_id: iOS simulator device ID (defaults to 'booted')
    
    Returns:
        Launch details and status
    """
    if ctx:
        await ctx.info(f"🚀 Launching app with FastMCP - {bundle_id}")
    
    try:
        # Use existing robust simulator manager
        result = await simulator_manager.launch_app(bundle_id, device_id)
        
        if ctx:
            await ctx.info(f"✅ App launched successfully: {bundle_id}")
        
        return {
            "success": True,
            "message": f"App launched successfully: {bundle_id}",
            "bundle_id": bundle_id,
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "fastmcp": True
        }
        
    except Exception as e:
        error_msg = f"App launch failed: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP app launch error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "bundle_id": bundle_id,
            "device_id": device_id,
            "suggestions": [
                "Verify bundle ID is correct",
                "Ensure app is installed on simulator", 
                "Check iOS Simulator is running"
            ],
            "fastmcp": True
        }

@mcp.tool
async def find_and_tap(
    accessibility_id: Optional[str] = None,
    element_text: Optional[str] = None,
    device_id: str = "booted",
    take_screenshot: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Find and tap UI elements using existing Appium client.
    
    Args:
        accessibility_id: Accessibility identifier of element to tap
        element_text: Text content of element to find and tap  
        device_id: iOS simulator device ID (defaults to 'booted')
        take_screenshot: Whether to take screenshot after tapping
    
    Returns:
        Tap operation results
    """
    if ctx:
        identifier = accessibility_id or element_text
        await ctx.info(f"👆 Finding and tapping with FastMCP - {identifier}")
    
    if not accessibility_id and not element_text:
        error_msg = "Either accessibility_id or element_text must be provided"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "fastmcp": True
        }
    
    try:
        # Use existing robust find and tap tool
        result = await find_and_tap_tool.execute_impl(
            accessibility_id=accessibility_id,
            element_text=element_text,
            device_id=device_id
        )
        
        response = {
            "success": True,
            "message": f"Element tapped successfully: {accessibility_id or element_text}",
            "element_identifier": accessibility_id or element_text,
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "fastmcp": True
        }
        
        # Take screenshot if requested
        if take_screenshot:
            try:
                screenshot_result = await screenshot_service.take_screenshot(device_id=device_id)
                response["screenshot"] = {
                    "filename": screenshot_result["filename"],
                    "path": screenshot_result["path"]
                }
                if ctx:
                    await ctx.info(f"📸 Screenshot taken: {screenshot_result['filename']}")
            except Exception as e:
                logger.warning(f"Screenshot after tap failed: {e}")
        
        if ctx:
            await ctx.info(f"✅ Element tapped successfully")
        
        return response
        
    except Exception as e:
        error_msg = f"Find and tap failed: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP find and tap error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "element_identifier": accessibility_id or element_text,
            "device_id": device_id,
            "suggestions": [
                "Check element identifier is correct",
                "Ensure element is visible on screen",
                "Verify Appium server is running"
            ],
            "fastmcp": True
        }

@mcp.tool
async def appium_tap_and_type(
    text: str,
    element_type: str = "textField",
    device_id: str = "booted",
    timeout: int = 10,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Find text fields and type text using existing Appium client.
    
    Args:
        text: Text to type into the text field
        element_type: Type of element to find (defaults to 'textField')
        device_id: iOS simulator device ID (defaults to 'booted')  
        timeout: Timeout for finding text field
    
    Returns:
        Text input operation results
    """
    if ctx:
        await ctx.info(f"⌨️ Typing text with FastMCP - '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    try:
        # Use existing robust Appium client
        result = await appium_client.tap_and_type(
            text=text,
            timeout=timeout
        )
        
        if ctx:
            await ctx.info(f"✅ Text typed successfully")
        
        return {
            "success": True,
            "message": f"Text typed successfully: {len(text)} characters",
            "text": text,
            "element_type": element_type,
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "fastmcp": True
        }
        
    except Exception as e:
        error_msg = f"Text input failed: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP text input error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "text": text,
            "element_type": element_type,
            "device_id": device_id,
            "suggestions": [
                "Ensure text field is visible and active",
                "Check element type is correct",
                "Verify Appium server is running"
            ],
            "fastmcp": True
        }

@mcp.tool
async def list_simulators(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    List available iOS simulators using existing simulator manager.
    
    Returns:
        List of available iOS simulators
    """
    if ctx:
        await ctx.info("📱 Listing iOS simulators with FastMCP")
    
    try:
        # Use existing robust simulator manager
        result = await simulator_manager.list_simulators()
        
        if ctx:
            await ctx.info(f"✅ Found {len(result.get('devices', []))} simulators")
        
        return {
            "success": True,
            "simulators": result.get("devices", []),
            "timestamp": datetime.now().isoformat(),
            "fastmcp": True
        }
        
    except Exception as e:
        error_msg = f"Failed to list simulators: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP simulator list error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "suggestions": [
                "Ensure Xcode is properly installed",
                "Check iOS Simulator is accessible"
            ],
            "fastmcp": True
        }

@mcp.tool
async def get_server_status(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Get FastMCP server status and environment information.
    
    Returns:
        Server status and configuration details
    """
    if ctx:
        await ctx.info("📊 Getting FastMCP server status")
    
    try:
        import platform
        
        # Check Appium status
        appium_status = "unknown"
        try:
            await appium_client.start_session()
            appium_status = "running" if appium_client.session_active else "not running"
            await appium_client.close_session()
        except:
            appium_status = "unreachable"
        
        response = {
            "success": True,
            "server": {
                "name": "iOS Automation MCP Server (FastMCP)",
                "version": "2.0.0",
                "framework": "FastMCP 2.0",
                "status": "running",
                "timestamp": datetime.now().isoformat()
            },
            "system": {
                "python_version": sys.version,
                "platform": platform.platform(),
                "working_directory": str(Path.cwd())
            },
            "environment": {
                "fastmcp_available": True,
                "appium_status": appium_status,
                "xcode_tools_available": True,
                "screenshot_directory": str(screenshot_service.default_directory)
            },
            "tools": [
                "take_screenshot",
                "launch_app", 
                "find_and_tap",
                "appium_tap_and_type",
                "list_simulators",
                "get_server_status"
            ],
            "fastmcp": True
        }
        
        if ctx:
            await ctx.info("✅ Server status retrieved")
        
        return response
        
    except Exception as e:
        error_msg = f"Failed to get server status: {str(e)}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        
        logger.error(f"FastMCP server status error: {e}")
        return {
            "success": False,
            "error": error_msg,
            "fastmcp": True
        }

# Add health check endpoint for cloud deployment
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for cloud deployment monitoring."""
    return {
        "status": "healthy",
        "service": "iOS Automation MCP Server (FastMCP)",
        "version": "2.0.0",
        "environment": "cloud" if IS_CLOUD else "local",
        "timestamp": datetime.now().isoformat()
    }

# Add root endpoint for basic info
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint providing basic server information."""
    return {
        "name": "iOS Automation MCP Server (FastMCP)",
        "version": "2.0.0",
        "status": "running",
        "environment": "cloud" if IS_CLOUD else "local",
        "transport": os.getenv("MCP_TRANSPORT", "sse"),
        "timestamp": datetime.now().isoformat()
    }

# Add SSE endpoint
@app.get("/sse")
async def sse():
    """SSE endpoint for FastMCP communication."""
    try:
        async def event_generator():
            while True:
                if await mcp.has_message():
                    message = await mcp.get_message()
                    yield {
                        "event": "message",
                        "data": message
                    }
                await asyncio.sleep(0.1)
        
        return EventSourceResponse(event_generator())
    except Exception as e:
        logger.error(f"SSE endpoint error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    
    # Get transport configuration - prioritize environment for cloud deployment
    transport = os.getenv("MCP_TRANSPORT", "sse").lower()
    host = os.getenv("MCP_HOST", "0.0.0.0")  # Changed to 0.0.0.0 for cloud deployment
    port_str = os.getenv("MCP_PORT", os.getenv("PORT", "8000"))
    try:
        port = int(port_str)
    except (ValueError, TypeError):
        logger.warning(f"Invalid PORT value received: '{port_str}'. Defaulting to 8000.")
        port = 8000
    
    logger.info(f"🎯 iOS Automation Server (FastMCP 2.0)")
    logger.info(f"🐍 Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    logger.info(f"⚡ FastMCP: 2.9.2")
    logger.info(f"🔌 Transport: {transport}")
    
    if IS_CLOUD:
        logger.info("☁️  Cloud deployment detected - using SSE transport")
        transport = "sse"
        logger.info("🌍 Remote deployment - accessible globally via SSE")
        logger.info("🔍 Health check available at /health")
        logger.info(f"📡 SSE endpoint: /sse")
    else:
        logger.info("🔧 Local development mode")
        logger.info("🔧 Available tools: take_screenshot, launch_app, find_and_tap, appium_tap_and_type, list_simulators")
    
    # Run the server
    try:
        uvicorn.run(app, host=host, port=port, log_level="debug")
    except KeyboardInterrupt:
        logger.info("\n⏹️ FastMCP server stopped by user")
    except Exception as e:
        logger.error(f"💥 FastMCP server error: {e}")
        sys.exit(1) 