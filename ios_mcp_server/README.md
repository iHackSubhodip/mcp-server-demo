# iOS MCP Server

Professional iOS automation server with clean architecture and SOLID principles.

## 📺 Demo Video

[![iOS MCP Server Demo](https://img.youtube.com/vi/480AmvL9ziQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=480AmvL9ziQ)

**Watch the complete demo**: [iOS MCP Server in Action](https://www.youtube.com/watch?v=480AmvL9ziQ) - See real iOS automation with Claude Desktop integration!

## Architecture

![Architecture Diagram](../archDiagram.png)

```
ios_mcp_server/
├── main.py                       # Entry point
├── config/settings.py           # Configuration
├── utils/                       # Shared utilities
│   ├── logger.py               # Colored logging
│   ├── exceptions.py           # Custom exceptions
│   └── command_runner.py       # Async commands
├── automation/                  # Core services
│   ├── appium_client.py        # iOS automation
│   ├── simulator_manager.py    # Simulator control
│   └── screenshot_service.py   # Screenshots
├── tools/                       # MCP tools
│   ├── base_tool.py            # Abstract base
│   ├── tool_registry.py        # Tool management
│   ├── appium_tap_type_tool.py # Main automation
│   ├── screenshot_tool.py      # Screenshot capture
│   └── launch_app_tool.py      # App launcher
└── server/mcp_server.py         # MCP protocol
```

## Design Patterns

- **Template Method**: `BaseTool` consistent execution
- **Registry**: `ToolRegistry` centralized management
- **Factory**: Tool instantiation
- **Strategy**: Multiple automation approaches
- **Dependency Injection**: Configuration injection

## Tools

### `appium_tap_and_type`
Find text fields and type text using intelligent element detection.
```json
{
  "text": "Hello World!",
  "element_type": "textField",
  "timeout": 10
}
```

### `find_and_tap` ⭐ **NEW**
Advanced element finding and tapping with multiple strategies.
```json
{
  "element_text": "Settings",
  "element_type": "button",
  "accessibility_id": "settingsButton",
  "partial_match": true,
  "take_screenshot": true,
  "dismiss_after_screenshot": false,
  "timeout": 10
}
```

**Finding Strategies:**
- **Accessibility ID**: `accessibility_id: "settingsButton"`
- **Text Content**: `element_text: "Settings"`
- **Partial Text**: `element_text: "Sett", partial_match: true`
- **Element Type**: `element_type: "button"`
- **XPath**: `xpath: "//XCUIElementTypeButton[@name='Settings']"`

**Auto-Dismiss**: Set `dismiss_after_screenshot: true` to automatically dismiss modals after screenshots.

### `take_screenshot`
Capture high-quality screenshots of the current screen.
```json
{
  "filename": "optional_name.png"
}
```

### `launch_app`
Launch iOS applications by bundle identifier.
```json
{
  "bundle_id": "com.example.app"
}
```

## Sequence Flow

### Complete Automation Test Example

![Sequence Diagram](../sequenceDiagram.png)

**Use Case: Complete App Automation Workflow**
1. Launch app with `bundle_id: "com.google.doc-retrival-agent"`
2. Take initial screenshot to see current state
3. Use **find_and_tap** with `accessibility_id: "settingsButton"`, `dismiss_after_screenshot: true`, and `take_screenshot: true`
4. Use **find_and_tap** with `accessibility_id: "documentButton"`, `dismiss_after_screenshot: true`, and `take_screenshot: true`
5. Use **appium_tap_and_type** to type "Tell me about swift language in 5 bullet points"
6. Use **find_and_tap** with `accessibility_id: "sendButton"`, and `take_screenshot: true`
7. Take final screenshot to verify the complete automation sequence

**Advanced Features:**
- **Smart Element Finding**: Multiple strategies (accessibility ID, text, XPath)
- **Auto-Dismiss Modals**: Automatically close popups after screenshots
- **Partial Text Matching**: Find elements with partial text matches
- **Screenshot Integration**: Capture proof of each automation step

## Quick Start

```bash
./start_ios_mcp.sh
```

## Configuration

Environment variables in `config/settings.py`:
- `APPIUM_URL`: Default `http://localhost:4723`
- `IOS_PLATFORM_VERSION`: Default `iOS 18.2`
- `IOS_DEVICE_NAME`: Default `iPhone 16 Pro`
- `LOG_LEVEL`: Default `INFO` 