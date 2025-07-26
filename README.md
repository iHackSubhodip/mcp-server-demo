# Mobile automation iOS MCP server

> Modern iOS automation server built with FastMCP 2.0 and clean architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0-green.svg)](https://github.com/jlowin/fastmcp)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%26%20Modular-brightgreen.svg)](#architecture)

A production-ready iOS automation MCP server built with FastMCP 2.0, featuring **clean modular architecture** with complete platform segregation. Ready for cross-platform expansion with iOS-specific and shared components properly separated.

## 📺 Demo Video

[![Mobile automation iOS MCP server Demo](https://img.youtube.com/vi/480AmvL9ziQ/maxresdefault.jpg)](https://youtu.be/fVqE7nLfqoE)

**🎬 Watch the Complete Demo**: [Mobile automation iOS MCP server in Action](https://youtu.be/fVqE7nLfqoE)

## ✨ Features

- 🚀 **FastMCP 2.0** - Modern Python-first MCP implementation
- 🌐 **Cloud Deployment** - Ready for Railway, Heroku, or other platforms
- 📱 **Real iOS Automation** - Appium + WebDriverAgent integration
- 🏗️ **Clean Modular Architecture** - Complete platform segregation & SOLID principles
- 🔄 **Cross-Platform Ready** - Shared utilities for future Android/other platforms
- 🎨 **Beautiful Logging** - Colored console output with emojis
- 🔧 **Type-Safe** - Comprehensive type hints throughout
- 🔌 **Extensible** - Plugin-style tool system with modular configuration
- 📦 **Zero Code Duplication** - DRY principles with shared utilities

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
   - [uv](https://docs.astral.sh/uv/) (recommended) or pip
   - Xcode with iOS Simulator
   - Node.js (for Appium)

2. **Installation**
   ```bash
   git clone https://github.com/iHackSubhodip/mcp-server-demo.git
   cd mcp-server-demo
   
   # Using uv (recommended)
   uv sync
   
   # Or using pip (legacy)
   pip install -e .
   ```

3. **Claude Desktop Configuration**
   ```json
   {
     "mcpServers": {
       "ios-automation-local": {
         "command": "uv",
         "args": ["run", "python", "ios_mcp_server/fastmcp_server.py"],
         "cwd": "/path/to/mcp-server-demo"
       }
     }
   }
   ```

## 🏗️ Architecture

The Mobile automation iOS MCP server features a **clean, modular architecture** with complete platform segregation achieved through a comprehensive 6-phase refactoring. This design enables maximum maintainability, zero code duplication, and seamless cross-platform expansion.

### ✨ Architecture Achievements

**🎯 Complete Platform Segregation**
- **Cross-platform utilities** isolated in `shared/` package
- **iOS-specific code** contained in `platforms/ios/` package  
- **Clean separation** of concerns across all components
- **Future-ready** for Android in `platforms/android/`

**🔄 DRY Principles Applied**
- **Shared utilities**: Logger, exceptions, command runner
- **Base configuration**: AppiumConfig, ServerConfig for reuse
- **Platform configs**: iOS-specific settings separate
- **Zero duplication** between current/future platforms

**🛡️ Maintainable & Extensible**
- **Self-contained platforms**: Each platform completely independent
- **Unified interface**: Single configuration entry point
- **Backward compatible**: All existing interfaces preserved
- **Professional structure**: Enterprise-grade organization

### Directory Structure
```
ios_mcp_server/
├── fastmcp_server.py          # 🚀 FastMCP 2.0 server (main entry)
├── config/
│   └── settings.py           # 🔧 Unified configuration interface
├── shared/                   # 🌐 Cross-platform utilities & config
│   ├── utils/               # 🛠️ Platform-agnostic utilities  
│   │   ├── logger.py       # 📝 Colored logging with emojis
│   │   ├── exceptions.py   # ⚠️ Exception hierarchy
│   │   └── command_runner.py # 💻 Shell command execution
│   └── config/             # ⚙️ Base configuration classes
│       └── base_settings.py # 📋 AppiumConfig, ServerConfig
├── platforms/ios/          # 🍎 iOS-specific platform code
│   ├── automation/         # 🤖 iOS automation services
│   │   ├── appium_client.py # 📱 iOS automation client
│   │   ├── screenshot_service.py # 📸 Screenshot handling
│   │   └── simulator_manager.py # 🎮 Simulator management
│   ├── tools/             # 🔨 iOS-specific MCP tools
│   │   ├── appium_tap_type_tool.py # ⌨️ Text field automation
│   │   ├── find_and_tap_tool.py    # 👆 Advanced element finding
│   │   ├── launch_app_tool.py      # 🚀 App launching
│   │   └── screenshot_tool.py      # 📷 Screenshot capture
│   └── config/            # ⚙️ iOS-specific configuration
│       └── ios_settings.py # 🍎 iOSConfig (XCUITest, iPhone)
├── screenshots/             # 📁 Screenshot storage
├── Dockerfile              # 🐳 Container deployment
├── Procfile                # 🚂 Railway deployment
└── pyproject.toml          # 📦 Dependencies & project config
```

### 🎯 Benefits Achieved

| Aspect | Before Refactoring | After Refactoring |
|--------|-------------------|-------------------|
| **Structure** | Mixed iOS/shared code | Clean platform segregation |
| **Maintainability** | Monolithic | Modular & self-contained |
| **Extensibility** | iOS-only | Cross-platform ready |
| **Code Reuse** | Duplication likely | Shared utilities for all platforms |
| **Configuration** | Single settings file | Modular config hierarchy |
| **Organization** | Flat structure | Professional enterprise structure |

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

### Local Development Commands
```bash
# Run FastMCP server locally (with uv)
uv run python ios_mcp_server/fastmcp_server.py

# Install dependencies (if needed)
uv sync

# Development mode (with dev dependencies)
uv sync --dev
```

### Appium Setup
```bash
# Install Appium
npm install -g appium
appium driver install xcuitest

# Start Appium server
appium server --port 4723
```

### Architecture Development
```bash
# The modular structure makes development easier:

# Work on shared utilities (affects all platforms)
cd shared/utils/

# Work on iOS-specific features  
cd platforms/ios/

# Work on configuration
cd config/

# Add new platforms (future)
mkdir platforms/android/
```

## 🌐 Cloud Deployment

This server is deployed on Railway and accessible via:
- **HTTP Endpoint**: `https://mcp-server-demo-production.up.railway.app/`
- **SSE Endpoint**: `https://mcp-server-demo-production.up.railway.app/sse/`

The cloud deployment simulates iOS automation responses for demonstration purposes.

## 📊 Key Improvements

| Feature | Traditional MCP | FastMCP 2.0 + Clean Architecture |
|---------|----------------|----------------------------------|
| **Setup** | Complex configuration | Simple Python decorators |
| **Architecture** | Monolithic | Modular platform segregation |
| **Code Reuse** | Manual duplication | Shared utilities package |
| **Type Safety** | Manual validation | Built-in Pydantic models |
| **Error Handling** | Basic try-catch | Rich context and logging |
| **Deployment** | Local only | Cloud-ready with Railway |
| **Extensibility** | Hard to extend | Easy platform addition |
| **Maintainability** | Complex | Clean separation of concerns |

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

Core dependencies managed via `pyproject.toml`:
- `fastmcp>=2.9.2` - FastMCP 2.0 framework
- `mcp>=1.0.0` - Traditional MCP protocol
- `aiohttp>=3.9.0` - HTTP client for automation
- `appium-python-client>=3.0.0` - iOS automation
- `pydantic>=2.4.0` - Data validation

Install with:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the clean architecture patterns:
   - **Shared utilities** go in `shared/`
   - **Platform-specific code** goes in `platforms/{platform}/`
   - **Configuration** follows the modular hierarchy
4. Add comprehensive error handling
5. Submit a pull request

## 🚀 Future Expansion

Thanks to the clean architecture, adding new platforms is straightforward:

```bash
# Add Android platform (example)
mkdir -p platforms/android/{automation,tools,config}

# Reuse shared utilities
from shared.utils import get_logger, AutomationMCPError
from shared.config import AppiumConfig, ServerConfig

# Create Android-specific config
from platforms.android.config import AndroidConfig
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

