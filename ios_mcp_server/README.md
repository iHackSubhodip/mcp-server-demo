# iOS MCP Server

Professional iOS automation server with clean architecture and SOLID principles.

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
```json
{
  "text": "Hello World!",
  "element_type": "textField",
  "timeout": 10
}
```

### `take_screenshot`
```json
{
  "filename": "optional_name.png"
}
```

### `launch_app`
```json
{
  "bundle_id": "com.example.app"
}
```

## Sequence Flow

### Complete Automation Test Example

![Sequence Diagram](../sequenceDiagram.png)

**Use Case: Chat App Testing**
1. Launch the app with bundle ID "com.google.doc-retrival-agent"
2. Take a screenshot to see the initial state
3. Use appium_tap_and_type to find the chat input field and type "Hello! Automated test! 🎉"
4. Take a screenshot to verify the first message
5. Use appium_tap_and_type again to type "Second message! ✨"
6. Take a final screenshot to show both messages

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