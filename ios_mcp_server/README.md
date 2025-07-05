# iOS MCP Automation Server

🎉 **Production-Ready iOS Automation System** 🎉

A complete end-to-end iOS automation solution that enables remote control of iOS simulators through Claude Desktop using the Model Context Protocol (MCP).

## 🏆 **What This System Does**

- **Remote iOS Automation**: Control iOS simulators from anywhere in the world
- **Claude Desktop Integration**: Direct integration with Claude's MCP protocol
- **Real App Control**: Actually launches and controls iOS apps (not simulations)
- **Multi-step Workflows**: Complex automation sequences with screenshots
- **Modal Handling**: Automatically dismisses modals and screens
- **Global Deployment**: Deployed on Railway, accessible globally

## 🚀 **Architecture**

```
Claude Desktop → Railway (FastMCP Server) → ngrok → Local Mac (iOS Simulator)
```

## 📁 **Repository Structure**

```
mcp-server-demo-proj/
├── ios_mcp_server/              # Main automation server
│   ├── fastmcp_server.py        # FastMCP 2.0 server (MAIN FILE)
│   ├── automation/              # Core automation services
│   ├── tools/                   # Automation tools
│   ├── config/                  # Configuration
│   ├── utils/                   # Utilities
│   ├── Dockerfile              # Railway deployment
│   ├── Procfile                # Railway process config
│   └── requirements.txt        # Python dependencies
├── ios_mcp_env/                # Python virtual environment
├── claude_desktop_config.json  # Claude Desktop MCP config
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## ⚡ **Quick Start**

### 1. Prerequisites

- macOS with Xcode and iOS Simulator
- Python 3.13+
- Appium 2.x
- ngrok account (for remote access)
- Railway account (for cloud deployment)

### 2. Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd mcp-server-demo-proj

# Activate virtual environment
source ios_mcp_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Appium server
appium server --port 4723

# Start iOS Simulator (iPhone 16 Pro recommended)
xcrun simctl boot "iPhone 16 Pro"
```

### 3. Cloud Deployment (Railway)

The FastMCP server is already deployed on Railway at:
- **Health Check**: `https://mcp-server-demo-production.up.railway.app/health`
- **SSE Endpoint**: `https://mcp-server-demo-production.up.railway.app/sse`

### 4. Remote Access Setup

```bash
# Start ngrok tunnel to expose local Appium server
ngrok http 4723

# Note the ngrok URL (e.g., https://xxxx.ngrok-free.app)
# This is automatically configured in Railway environment variables
```

### 5. Claude Desktop Configuration

Copy the contents of `claude_desktop_config.json` to your Claude Desktop MCP configuration.

## 🛠 **Available Tools**

### Core Automation Tools

1. **`launch_app`** - Launch iOS applications
   ```python
   launch_app(bundle_id="com.apple.mobilesafari")
   ```

2. **`find_and_tap`** - Find and tap UI elements
   ```python
   find_and_tap(
       accessibility_id="settingsButton",
       take_screenshot=True,
       dismiss_after_screenshot=True
   )
   ```

3. **`appium_tap_and_type`** - Type text into text fields
   ```python
   appium_tap_and_type(text="Hello, world!")
   ```

4. **`take_screenshot`** - Capture screenshots
   ```python
   take_screenshot(filename="current_state.png")
   ```

5. **`list_simulators`** - List available iOS simulators

### Advanced Features

- **Modal Dismissal**: Automatically dismiss modals after screenshots
- **Multiple Element Finding Strategies**: Accessibility ID, XPath, text matching
- **Session Management**: Proper Appium session handling
- **Error Recovery**: Robust error handling and recovery

## 🔧 **Configuration**

### Environment Variables (Railway)

```bash
REMOTE_IOS_HOST=xxxx.ngrok-free.app
REMOTE_IOS_PORT=443
MCP_TRANSPORT=sse
PORT=8000
```

### iOS Simulator Configuration

- **Device**: iPhone 16 Pro (recommended)
- **UDID**: `4013533D-4166-4991-B3AD-5E4660AC2DD1`
- **iOS Version**: 18.2+

## 📱 **Example Automation Workflow**

```python
# Complete automation sequence
automation_steps = [
    "Launch app with bundle_id: 'com.google.doc-retrival-agent'",
    "Take initial screenshot",
    "Find and tap settingsButton with dismiss_after_screenshot: true",
    "Find and tap documentButton with dismiss_after_screenshot: true", 
    "Type text: 'Tell me about swift language in 5 bullet points'",
    "Find and tap sendButton",
    "Take final screenshot"
]
```

## 🎯 **Key Features**

### ✅ **Production Ready**
- Deployed on Railway cloud platform
- Global accessibility via HTTPS/SSE
- Robust error handling and logging
- Proper session management

### ✅ **Real Automation**
- Actually controls iOS simulators (not simulated)
- Prevents app auto-termination
- Handles complex UI interactions
- Takes real screenshots

### ✅ **Advanced UI Handling**
- Multiple element finding strategies
- Automatic modal dismissal
- Text input with proper field detection
- Screenshot capture at each step

### ✅ **Claude Desktop Integration**
- Native MCP protocol support
- SSE transport for real-time communication
- Comprehensive tool descriptions
- Error reporting and suggestions

## 🚨 **Troubleshooting**

### Common Issues

1. **App Auto-Termination**
   - Fixed with `shouldTerminateApp: False` capability

2. **Element Not Found**
   - Uses multiple finding strategies
   - Provides available element suggestions

3. **Connection Issues**
   - Check ngrok tunnel status
   - Verify Railway deployment health
   - Ensure Appium server is running

### Debug Commands

```bash
# Check Appium server status
curl http://localhost:4723/status

# Check Railway deployment
curl https://mcp-server-demo-production.up.railway.app/health

# Check ngrok tunnel
curl https://your-ngrok-url.ngrok-free.app/status
```

## 🎉 **Success Metrics**

This system successfully achieves:

- ✅ **End-to-End Automation**: Claude Desktop → Railway → ngrok → iOS Simulator
- ✅ **Real App Control**: Actually launches and controls iOS apps
- ✅ **Global Accessibility**: Works from anywhere in the world
- ✅ **Production Stability**: Handles errors gracefully
- ✅ **Complex Workflows**: Multi-step automation with screenshots
- ✅ **Professional Quality**: Enterprise-grade iOS automation

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **FastMCP 2.0** - Modern MCP framework
- **Appium** - Mobile automation framework
- **Railway** - Cloud deployment platform
- **ngrok** - Secure tunneling service
- **Claude Desktop** - AI assistant with MCP support

---

**Built with ❤️ for iOS automation enthusiasts!** 🚀 