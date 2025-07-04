#!/usr/bin/env python3
"""
Test script to verify FastMCP server can start without errors
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    print("✅ Testing imports...")
    from fastmcp import FastMCP
    print("  ✓ FastMCP imported")
    
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    print("  ✓ Starlette imported")
    
    import uvicorn
    print("  ✓ Uvicorn imported")
    
    # Test basic FastMCP initialization
    print("\n✅ Testing FastMCP initialization...")
    mcp = FastMCP(name="Test Server", version="1.0.0")
    print("  ✓ FastMCP instance created")
    
    # Test creating app
    print("\n✅ Testing app creation...")
    app = mcp.http_app(transport="sse")
    print("  ✓ HTTP app created")
    
    print("\n🎉 All tests passed! FastMCP server should work on Railway.")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nMake sure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"  Type: {type(e).__name__}") 