# 📱 iOS MCP Server Setup Guide

## ✅ **What You've Built**

Your iOS MCP server provides **8 automation tools** and **3 resources** for AI assistants:

### 🔧 **Available Tools:**
- `ios_simulator_list` - List all available simulators
- `ios_simulator_boot` - Boot a specific simulator
- `ios_simulator_shutdown` - Shutdown a simulator 
- `ios_take_screenshot` - Capture simulator screen
- `ios_accessibility_tree` - Get UI element tree
- `ios_tap_coordinate` - Simulate touch at coordinates
- `ios_app_install` - Install apps on simulator
- `ios_app_launch` - Launch apps by bundle ID

### 📊 **Available Resources:**
- `simulator://current-state` - Real-time simulator status
- `accessibility://hierarchy` - UI hierarchy data
- `logs://simulator` - System logs

---

## 🚀 **Claude Desktop Integration**

### **Step 1: Install Claude Desktop**
Download from: https://claude.ai/download

### **Step 2: Configure MCP Server**

1. **Find Claude Desktop config location:**
   ```bash
   # On macOS:
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Add iOS MCP server to config:**
   ```json
   {
     "mcpServers": {
       "ios-automation": {
         "command": "/Users/riju/Documents/mcp-server-demo/.build/release/ios-mcp-server",
         "args": [],
         "env": {}
       }
     }
   }
   ```

3. **Restart Claude Desktop**

### **Step 3: Test Integration**

Try these prompts in Claude Desktop:

```
"List all available iOS simulators"
"Take a screenshot of the current simulator"
"Show me the accessibility tree of the current app"
"Tap at coordinates 200, 300 on the simulator"
```

---

## 🧪 **Manual Testing**

Your server executable: `./build/release/ios-mcp-server`

Test individual functions:
```bash
# Take screenshot
xcrun simctl io booted screenshot /tmp/test.png

# List simulators  
xcrun simctl list devices

# Boot a simulator
xcrun simctl boot DEVICE_UDID

# Tap coordinates
xcrun simctl io booted tap 200 300
```

---

## 📋 **Requirements**

- ✅ macOS 13.0+
- ✅ Xcode with iOS Simulator
- ✅ Swift 6.0+
- ✅ Claude Desktop app

---

## 🎯 **What's Next**

1. **Extend functionality** - Add more iOS automation tools
2. **Add app testing** - Integrate XCTest for UI testing
3. **Error handling** - Improve error messages and validation
4. **Documentation** - Add detailed parameter schemas for tools

Your iOS MCP server is now ready for AI-powered iOS automation! 🚀 