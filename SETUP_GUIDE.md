# 🚀 Mobile automation iOS MCP server Setup Guide

Complete step-by-step guide to recreate the working iOS automation setup with Railway + ngrok.

## 📋 Prerequisites

- **macOS** (required for iOS Simulator)
- **Xcode** with iOS Simulator installed
- **Node.js** (for Appium)
- **Python 3.11+**
- **ngrok account** with auth token
- **Railway account** with deployed project

## 🔧 Step-by-Step Setup

### 1. Configure ngrok Authentication

```bash
# Add your ngrok auth token (replace with your actual token)
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN_HERE

# Verify configuration
cat ~/.ngrok2/ngrok.yml
```

### 2. Start iOS Simulator

```bash
# List available simulators
xcrun simctl list devices | grep "iPhone 16 Pro"

# Boot the simulator (if not already running)
xcrun simctl boot "iPhone 16 Pro"

# Verify it's running
xcrun simctl list devices | grep "iPhone 16 Pro" | grep "Booted"
```

### 3. Start Appium Server

```bash
# Install Appium globally (if not installed)
npm install -g appium
appium driver install xcuitest

# Start Appium server
appium server --port 4723
```

**Keep this terminal open** - you should see:
```
[Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

### 4. Start ngrok Tunnel

**Open a new terminal** and run:

```bash
# Start ngrok tunnel to expose Appium server
ngrok http 4723
```

**Keep this terminal open** - you'll see something like:
```
Forwarding    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:4723
```

**📝 Important**: Copy the ngrok URL (the `xxxx-xxxx-xxxx.ngrok-free.app` part without `https://`)

### 5. Test Local Setup

```bash
# Test Appium server
curl http://localhost:4723/status

# Test ngrok tunnel (replace with your actual ngrok URL)
curl https://YOUR-NGROK-URL.ngrok-free.app/status
```

Both should return status information with `"ready": true`.

### 6. Update Railway Environment Variable

1. **Go to Railway Dashboard**: [railway.app](https://railway.app)
2. **Navigate to your project**: `mcp-server-demo`
3. **Click on Variables tab**
4. **Find or create**: `REMOTE_IOS_HOST`
5. **Set value to**: `YOUR-NGROK-URL.ngrok-free.app` (hostname only, no `https://`)
6. **Save** - Railway will auto-redeploy

### 7. Test Cloud Connection

```bash
# Test Railway health
curl https://mcp-server-demo-production.up.railway.app/health

# Test MCP endpoint
curl https://mcp-server-demo-production.up.railway.app/sse/
```

### 8. Test iOS Automation in Claude Desktop

Add this to your Claude Desktop config:

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

## ✅ Verification Checklist

- [ ] **Appium server** running on `localhost:4723`
- [ ] **iPhone 16 Pro simulator** booted and visible
- [ ] **ngrok tunnel** active and forwarding to Appium
- [ ] **Railway environment variable** updated with new ngrok URL
- [ ] **Railway deployment** healthy and responding
- [ ] **MCP tools** working in Claude Desktop

## 🧪 Test Commands

### Test Screenshot
```json
{
  "tool": "take_screenshot",
  "parameters": {
    "filename": "test.png"
  }
}
```

### Test App Launch
```json
{
  "tool": "launch_app",
  "parameters": {
    "bundle_id": "com.apple.mobilesafari"
  }
}
```

## 🚨 Troubleshooting

### Problem: "ngrok tunnel offline"
```bash
# Check ngrok status
curl https://YOUR-NGROK-URL.ngrok-free.app/status

# Restart ngrok if needed
pkill -f ngrok
ngrok http 4723
```

### Problem: "Appium not responding"
```bash
# Check Appium status
curl http://localhost:4723/status

# Restart Appium if needed
pkill -f appium
appium server --port 4723
```

### Problem: "Railway still using old URL"
1. Verify environment variable in Railway dashboard
2. Check Railway deployment logs
3. Force redeploy if needed

### Problem: "iOS Simulator not found"
```bash
# List all simulators
xcrun simctl list devices

# Boot correct simulator
xcrun simctl boot "iPhone 16 Pro"
```

## 📝 Important Notes

### Keep Running
These processes must stay running for the system to work:
- **Appium server** (`appium server --port 4723`)
- **ngrok tunnel** (`ngrok http 4723`)
- **iOS Simulator** (iPhone 16 Pro)

### ngrok URLs Change
- **Free ngrok URLs change** when you restart ngrok
- **Always update Railway** environment variable after restarting ngrok
- **Authenticated ngrok** is more stable than anonymous

### Railway Environment Variables
- Variable name: `REMOTE_IOS_HOST`
- Value format: `domain.ngrok-free.app` (no protocol)
- Railway auto-redeploys when changed

## 🔄 Quick Restart Procedure

When you come back to your laptop:

1. **Start iOS Simulator**
2. **Start Appium**: `appium server --port 4723`
3. **Start ngrok**: `ngrok http 4723`
4. **Copy new ngrok URL**
5. **Update Railway environment variable**
6. **Wait for Railway to redeploy** (~2-3 minutes)
7. **Test in Claude Desktop**

## 🎯 Success Indicators

### In ngrok console:
```
HTTP Requests
-------------
POST /session                   200 OK
GET  /session/xxx/screenshot     200 OK
POST /session/xxx/element        200 OK
```

### In Appium logs:
```
[XCUITestDriver] New XCUITestDriver session created successfully
[XCUITestDriver] Taking screenshot with WDA
[XCUITestDriver] Executing command 'getScreenshot'
```

### In Claude Desktop:
- Screenshot tools return actual iOS screenshots
- App launch tools successfully start apps
- Element interaction tools work properly

---

**🎉 Once everything is green, your iOS automation is working through the cloud!** 