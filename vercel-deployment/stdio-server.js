#!/usr/bin/env node

// Simple stdio MCP server for Claude Desktop
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

// Create MCP server
const server = new Server(
  {
    name: 'ios-automation-local',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Add echo tool
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'echo',
        description: 'Echo back a message',
        inputSchema: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              description: 'Message to echo back'
            }
          },
          required: ['message']
        }
      },
      {
        name: 'take_screenshot',
        description: 'Take a screenshot (mock)',
        inputSchema: {
          type: 'object',
          properties: {
            filename: {
              type: 'string',
              description: 'Optional filename'
            }
          }
        }
      },
      {
        name: 'launch_app',
        description: 'Launch an iOS app (mock)',
        inputSchema: {
          type: 'object',
          properties: {
            bundle_id: {
              type: 'string',
              description: 'App bundle ID'
            }
          },
          required: ['bundle_id']
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case 'echo':
      return {
        content: [{
          type: 'text',
          text: `Echo: ${args.message}`
        }]
      };
    
    case 'take_screenshot':
      const filename = args.filename || `screenshot_${Date.now()}.png`;
      return {
        content: [{
          type: 'text',
          text: `📸 Screenshot taken: ${filename}`
        }]
      };
    
    case 'launch_app':
      return {
        content: [{
          type: 'text',
          text: `🚀 Launched app: ${args.bundle_id}`
        }]
      };
    
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server with stdio transport
const transport = new StdioServerTransport();
server.connect(transport); 