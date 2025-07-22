# iOS MCP Server

> Modern iOS automation server built with FastMCP 2.0 and clean architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0-green.svg)](https://github.com/jlowin/fastmcp)

A production-ready iOS automation MCP server built with FastMCP 2.0, offering both local and cloud deployment options. Features clean architecture, comprehensive error handling, and professional logging.

## 📺 Demo Video

[![iOS MCP Server Demo](https://img.youtube.com/vi/480AmvL9ziQ/maxresdefault.jpg)](https://youtu.be/fVqE7nLfqoE)

**🎬 Watch the Complete Demo**: [iOS MCP Server in Action](https://youtu.be/fVqE7nLfqoE)

## ✨ Features

- 🚀 **FastMCP 2.0** - Modern Python-first MCP implementation
- 🌐 **Cloud Deployment** - Ready for Railway, Heroku, or other platforms
- 📱 **Real iOS Automation** - Appium + WebDriverAgent integration
- 🏗️ **Clean Architecture** - SOLID principles and design patterns
- 🎨 **Beautiful Logging** - Colored console output with emojis
- 🔧 **Type-Safe** - Comprehensive type hints throughout
- 🔌 **Extensible** - Plugin-style tool system
- 📁 **Organized Structure** - iOS tools properly organized in dedicated subdirectories

## 🚀 Quick Start

### Option 1: Remote Server (Recommended)

Use the hosted version on Railway - no local setup required:

```json
{
  "mcpServers": {
    "ios-automation-railway": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp-server-demo-production.up.railway.app/sse/"
      ]
    }
  }
}
```

### Option 2: Local Development

1. **Prerequisites**
   - macOS (required for iOS automation)
   - Python 3.11+
   - Xcode with iOS Simulator
   - Node.js (for Appium)

2. **Installation**
   ```bash
   git clone https://github.com/iHackSubhodip/mcp-server-demo.git
   cd mcp-server-demo
   pip install -r ios_mcp_server/requirements.txt
   ```

3. **Claude Desktop Configuration**
   ```json
   {
     "mcpServers": {
       "ios-automation-local": {
         "command": "python",
         "args": ["-m", "ios_mcp_server.main"],
         "cwd": "/path/to/mcp-server-demo"
       }
     }
   }
   ```

## 🏗️ Architecture

The iOS MCP Server follows a clean, modular architecture with recently reorganized tool structure for better maintainability and extensibility.

### Recent Improvements ✨
- **Tool Organization**: iOS-specific tools moved to dedicated `tools/ios/` subdirectory
- **Package Structure**: Proper Python package initialization with `__init__.py` files
- **Import Clarity**: Clean separation between shared tools and platform-specific tools
- **Maintainability**: Easier to add new platform tools (Android, etc.) in the future

### Directory Structure
```
ios_mcp_server/
├── main.py                     # Entry point
├── fastmcp_server.py          # FastMCP 2.0 server
├── config/
│   └── settings.py           # Configuration management
├── automation/               # Core automation services
│   ├── appium_client.py     # iOS automation client
│   ├── screenshot_service.py # Screenshot handling
│   └── simulator_manager.py # Simulator management
├── tools/                   # MCP tools
│   ├── base_tool.py        # Abstract base class
│   ├── tool_registry.py    # Tool management
│   └── ios/                # iOS-specific tools
│       ├── __init__.py     # Package initialization
│       ├── appium_tap_type_tool.py # Text field automation
│       ├── find_and_tap_tool.py    # Advanced element finding
│       ├── launch_app_tool.py      # App launching
│       └── screenshot_tool.py      # Screenshot capture
├── utils/                   # Shared utilities
│   ├── logger.py           # Colored logging
│   ├── exceptions.py       # Custom exceptions
│   └── command_runner.py   # Async command execution
├── server/                  # Traditional MCP server
├── screenshots/             # Screenshot storage
├── Dockerfile              # Container deployment
├── Procfile                # Railway deployment
└── requirements.txt        # Dependencies
```

## 🔧 Available Tools

### `take_screenshot`
Capture iOS simulator screenshots
```json
{
  "filename": "optional_name.png",
  "device_id": "booted"
}
```

### `launch_app`
Launch iOS applications
```json
{
  "bundle_id": "com.apple.mobilesafari",
  "device_id": "booted"
}
```

### `find_and_tap`
Find and tap UI elements with smart automation
```json
{
  "accessibility_id": "submitButton",
  "take_screenshot": true,
  "dismiss_after_screenshot": false
}
```

### `appium_tap_and_type`
Enhanced text input with element finding
```json
{
  "text": "Hello World!",
  "element_type": "textField",
  "timeout": 10
}
```

### `list_simulators`
List available iOS simulators
```json
{}
```

### `get_server_status`
Check server and Appium status
```json
{}
```

## 🛠️ Development

### Local FastMCP Development
```bash
# Install dependencies
pip install -r ios_mcp_server/requirements.txt

# Run FastMCP server
python ios_mcp_server/fastmcp_server.py
```

### Traditional MCP Development
```bash
# Run traditional MCP server
python -m ios_mcp_server.main
```

### Appium Setup
```bash
# Install Appium
npm install -g appium
appium driver install xcuitest

# Start Appium server
appium server --port 4723
```

## 🌐 Cloud Deployment

This server is deployed on Railway and accessible via:
- **HTTP Endpoint**: `https://mcp-server-demo-production.up.railway.app/`
- **SSE Endpoint**: `https://mcp-server-demo-production.up.railway.app/sse/`

The cloud deployment simulates iOS automation responses for demonstration purposes.

## 📊 Key Improvements

| Feature | Traditional MCP | FastMCP 2.0 |
|---------|----------------|-------------|
| **Setup** | Complex configuration | Simple Python decorators |
| **Type Safety** | Manual validation | Built-in Pydantic models |
| **Error Handling** | Basic try-catch | Rich context and logging |
| **Deployment** | Local only | Cloud-ready with Railway |
| **Development** | Boilerplate heavy | Clean, intuitive API |

## 🔍 Troubleshooting

### Simulator Issues
```bash
# List available simulators
xcrun simctl list devices

# Boot a simulator
xcrun simctl boot "iPhone 16 Pro"
```

### Appium Connection
```bash
# Check Appium status
curl http://localhost:4723/status

# Restart Appium
pkill -f appium && appium server --port 4723
```

## 📝 Dependencies

Core dependencies:
- `fastmcp>=2.9.2` - FastMCP 2.0 framework
- `mcp>=1.0.0` - Traditional MCP protocol
- `aiohttp>=3.9.0` - HTTP client for automation
- `appium-python-client>=3.0.0` - iOS automation
- `pydantic>=2.4.0` - Data validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing architecture patterns
4. Add comprehensive error handling
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

