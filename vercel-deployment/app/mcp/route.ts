import { createMcpHandler } from '@vercel/mcp-adapter';
import { z } from 'zod';

// Simple MCP server using HTTP transport (no Redis required)
const handler = createMcpHandler((server) => {
  // Echo tool for testing
  server.tool(
    'echo',
    'Echo back a message',
    {
      message: z.string().describe('Message to echo back')
    },
    async ({ message }) => {
      return {
        content: [{
          type: 'text',
          text: `Echo: ${message}`
        }]
      };
    }
  );

  // Screenshot tool (mock)
  server.tool(
    'take_screenshot',
    'Take a screenshot (mock)',
    {
      filename: z.string().optional().describe('Optional filename')
    },
    async ({ filename }) => {
      const name = filename || `screenshot_${Date.now()}.png`;
      return {
        content: [{
          type: 'text',
          text: `📸 Screenshot taken: ${name}`
        }]
      };
    }
  );

  // App launch tool (mock)
  server.tool(
    'launch_app',
    'Launch an iOS app (mock)',
    {
      bundle_id: z.string().describe('App bundle ID')
    },
    async ({ bundle_id }) => {
      return {
        content: [{
          type: 'text',
          text: `🚀 Launched app: ${bundle_id}`
        }]
      };
    }
  );
});

export { handler as GET, handler as POST, handler as DELETE }; 