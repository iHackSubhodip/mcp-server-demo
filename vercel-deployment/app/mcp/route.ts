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

  // Find and tap tool with advanced element finding
  server.tool(
    'find_and_tap',
    'Find and tap elements using multiple strategies (accessibility ID, text content, element type)',
    {
      element_text: z.string().optional().describe('Text content to find'),
      accessibility_id: z.string().optional().describe('Accessibility identifier'),
      element_type: z.string().optional().describe('Element type (button, textField, etc.)'),
      partial_match: z.boolean().optional().describe('Use partial text matching'),
      take_screenshot: z.boolean().optional().describe('Take screenshot after action'),
      dismiss_after_screenshot: z.boolean().optional().describe('Dismiss screenshot after taking it')
    },
    async ({ element_text, accessibility_id, element_type, partial_match, take_screenshot, dismiss_after_screenshot }) => {
      // Simulate finding and tapping element
      let foundBy = '';
      if (accessibility_id) foundBy = `accessibility_id: "${accessibility_id}"`;
      else if (element_text) foundBy = `text: "${element_text}"${partial_match ? ' (partial)' : ''}`;
      else if (element_type) foundBy = `element_type: "${element_type}"`;
      
      let result = `🔍 Found and tapped element by ${foundBy}`;
      
      if (take_screenshot) {
        result += `\n📸 Screenshot taken after tap`;
        if (dismiss_after_screenshot) {
          result += ` (dismissed)`;
        }
      }
      
      return {
        content: [{
          type: 'text',
          text: result
        }]
      };
    }
  );

  // Appium tap and type tool
  server.tool(
    'appium_tap_and_type',
    'Intelligent text field detection and typing with configurable timeouts',
    {
      text: z.string().describe('Text to type'),
      element_type: z.string().optional().describe('Element type to find (textField, searchField, etc.)'),
      timeout: z.number().optional().describe('Timeout in seconds (default: 10)')
    },
    async ({ text, element_type, timeout }) => {
      const elementTypeStr = element_type || 'textField';
      const timeoutStr = timeout || 10;
      
      return {
        content: [{
          type: 'text',
          text: `⌨️ Found ${elementTypeStr} and typed: "${text}" (timeout: ${timeoutStr}s)`
        }]
      };
    }
  );

  // iOS automation demo workflow
  server.tool(
    'ios_automation_demo',
    'Complete automation workflow demonstration with configurable app and demo content',
    {
      app_bundle_id: z.string().optional().describe('App bundle ID to launch'),
      demo_text: z.string().optional().describe('Demo text content')
    },
    async ({ app_bundle_id, demo_text }) => {
      const bundleId = app_bundle_id || 'com.example.app';
      const demoContent = demo_text || 'Demo automation workflow';
      
      return {
        content: [{
          type: 'text',
          text: `🎭 Running iOS automation demo:\n• Launched: ${bundleId}\n• Demo content: "${demoContent}"\n• Workflow completed successfully`
        }]
      };
    }
  );
});

export { handler as GET, handler as POST, handler as DELETE }; 