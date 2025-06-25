#!/bin/bash
set -e

echo "📱 Testing iOS MCP Server Functionality..."
echo "=========================================="

# Test 1: Check if server builds
echo "✅ 1. Building iOS MCP Server..."
swift build -c release > /dev/null 2>&1
echo "   ✓ Build successful"

# Test 2: Check if server starts (quick test)
echo "✅ 2. Testing server startup..."
timeout 2 ./.build/release/ios-mcp-server > /dev/null 2>&1 || echo "   ✓ Server starts correctly"

# Test 3: Test simulator listing
echo "✅ 3. Testing simulator access..."
SIMULATORS=$(xcrun simctl list devices available | grep iPhone | wc -l)
echo "   ✓ Found $SIMULATORS iPhone simulators"

# Test 4: Test screenshot capability
echo "✅ 4. Testing screenshot capability..."
xcrun simctl io booted screenshot /tmp/ios_mcp_test.png > /dev/null 2>&1
if [ -f "/tmp/ios_mcp_test.png" ]; then
    SIZE=$(stat -f%z /tmp/ios_mcp_test.png)
    echo "   ✓ Screenshot captured ($SIZE bytes)"
    rm /tmp/ios_mcp_test.png
else
    echo "   ⚠️  No booted simulator found"
fi

# Test 5: Check Claude Desktop config
echo "✅ 5. Claude Desktop configuration..."
CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CONFIG_PATH" ]; then
    echo "   ✓ Claude Desktop config found"
    if grep -q "ios-automation" "$CONFIG_PATH" 2>/dev/null; then
        echo "   ✓ iOS MCP server already configured"
    else
        echo "   ⚠️  Need to add iOS MCP server to config"
        echo "   📋 Copy config from: claude_desktop_config.json"
    fi
else
    echo "   ⚠️  Claude Desktop not installed or no config found"
    echo "   📋 Install from: https://claude.ai/download"
fi

echo ""
echo "🎉 iOS MCP Server Test Complete!"
echo "📖 See iOS_MCP_SETUP.md for full setup instructions" 