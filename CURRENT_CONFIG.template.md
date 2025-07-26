# Current Working Configuration Template


## ngrok Configuration
### ngrok Auth Token
```
YOUR_NGROK_AUTH_TOKEN_HERE
```

### Current ngrok URL
```
https://YOUR-NGROK-URL.ngrok-free.app
```

## Railway Configuration
### Environment Variables
- `REMOTE_IOS_HOST` = `YOUR-NGROK-URL.ngrok-free.app`

## iOS Simulator Configuration
### Current Device
- **Device**: iPhone 16 Pro
- **iOS Version**: 18.2
- **UDID**: `YOUR-SIMULATOR-UDID`

## Port Configuration
### Local Development
- **Appium Server**: `localhost:4723`
- **ngrok Tunnel**: `4723 -> https://YOUR-NGROK-URL.ngrok-free.app`

### Railway MCP Server
- **HTTP Endpoint**: `https://mcp-server-demo-production.up.railway.app/`
- **SSE Endpoint**: `https://mcp-server-demo-production.up.railway.app/sse/`

## Claude Desktop Configuration
### MCP Server Config
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

## Quick Commands
### Start ngrok Tunnel
```bash
ngrok http 4723
```

### Start Appium Server
```bash
appium server --port 4723
```

### Boot iOS Simulator
```bash
xcrun simctl boot "iPhone 16 Pro"
```

### Check Appium Status
```bash
curl http://localhost:4723/status
```

## Setup Instructions
1. Copy this template to `CURRENT_CONFIG.md`
2. Replace all placeholder values with your actual configuration
3. Never commit `CURRENT_CONFIG.md` to git (it's in .gitignore)
4. Use this template for sharing setup instructions publicly 