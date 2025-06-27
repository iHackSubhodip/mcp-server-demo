// Import necessary dependencies for MCP server implementation
import { createMcpHandler } from '@vercel/mcp-adapter';  // Vercel's official MCP adapter
import { z } from 'zod';  // Schema validation library for type-safe parameter validation

// ============================================================================
// MOCK AUTOMATION SERVICE
// ============================================================================
// Since Vercel runs on Linux and iOS automation requires macOS,
// we implement a mock service for demonstration purposes

class MockiOSAutomationService {
  // Simulate screenshot capture with realistic delay
  async takeScreenshot(filename?: string): Promise<{ success: boolean; message: string; filename?: string }> {
    // Simulate processing time for screenshot capture
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const screenshotName = filename || `screenshot_${Date.now()}.png`;
    
    return {
      success: true,
      message: `📸 Screenshot captured successfully: ${screenshotName}`,
      filename: screenshotName
    };
  }

  // Simulate iOS app launching with validation
  async launchApp(bundleId: string): Promise<{ success: boolean; message: string; bundleId: string }> {
    // Simulate app launch time
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Validate bundle ID format (basic validation)
    if (!bundleId.includes('.')) {
      return {
        success: false,
        message: `❌ Invalid bundle ID format: ${bundleId}`,
        bundleId
      };
    }
    
    return {
      success: true,
      message: `🚀 Successfully launched app: ${bundleId}`,
      bundleId
    };
  }

  // Advanced element finding and tapping simulation
  async findAndTap(params: {
    element_text?: string;
    accessibility_id?: string;
    element_type?: string;
    partial_match?: boolean;
    take_screenshot?: boolean;
    dismiss_after_screenshot?: boolean;
  }): Promise<{ success: boolean; message: string; strategy: string }> {
    // Simulate element search time
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Determine search strategy based on provided parameters
    let strategy = 'unknown';
    let searchCriteria = '';
    
    if (params.accessibility_id) {
      strategy = 'accessibility_id';
      searchCriteria = params.accessibility_id;
    } else if (params.element_text) {
      strategy = params.partial_match ? 'partial_text_match' : 'exact_text_match';
      searchCriteria = params.element_text;
    } else if (params.element_type) {
      strategy = 'element_type';
      searchCriteria = params.element_type;
    }
    
    // Simulate screenshot capture if requested
    const screenshotMsg = params.take_screenshot ? ' 📸 Screenshot taken.' : '';
    
    // Simulate modal dismissal if requested
    const dismissMsg = params.dismiss_after_screenshot ? ' 🗂️ Modal dismissed.' : '';
    
    return {
      success: true,
      message: `✅ Element found and tapped using ${strategy}: "${searchCriteria}".${screenshotMsg}${dismissMsg}`,
      strategy
    };
  }

  // Text field automation with intelligent detection
  async tapAndType(params: {
    text: string;
    element_type: string;
    timeout: number;
  }): Promise<{ success: boolean; message: string; text: string }> {
    // Simulate element detection and typing time
    await new Promise(resolve => setTimeout(resolve, 1200));
    
    // Validate text input
    if (!params.text.trim()) {
      return {
        success: false,
        message: '❌ Empty text provided for typing',
        text: params.text
      };
    }
    
    return {
      success: true,
      message: `⌨️ Successfully typed "${params.text}" into ${params.element_type} element (timeout: ${params.timeout}s)`,
      text: params.text
    };
  }

  // Complete automation workflow demonstration
  async runDemo(params: {
    app_bundle_id: string;
    demo_text: string;
  }): Promise<{ success: boolean; message: string; steps: string[] }> {
    // Simulate complete workflow with multiple steps
    const steps = [
      '🚀 Launching app...',
      '📸 Taking initial screenshot...',
      '🔍 Finding UI elements...',
      '⚙️ Tapping navigation buttons...',
      '⌨️ Typing demo text...',
      '📤 Sending message...',
      '📸 Taking final screenshot...'
    ];
    
    // Simulate each step with realistic timing
    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 300 + Math.random() * 200));
    }
    
    return {
      success: true,
      message: `🎉 Demo workflow completed successfully for ${params.app_bundle_id}`,
      steps
    };
  }
}

// ============================================================================
// MCP SERVER CONFIGURATION
// ============================================================================

// Create an instance of the mock automation service
const automationService = new MockiOSAutomationService();

// Create and configure the MCP server using Vercel's adapter
const handler = createMcpHandler({
  // Server metadata for client identification
  name: 'ios-mcp-server-vercel',
  version: '1.0.0',
  description: 'Professional iOS automation server deployed on Vercel with mock automation capabilities',
  
  // Configure the MCP server with tools
  configure: (server) => {
    
    // ========================================================================
    // TOOL 1: SCREENSHOT CAPTURE
    // ========================================================================
    server.tool(
      'take_screenshot',
      'Capture a screenshot of the iOS device screen',
      {
        // Optional filename parameter with validation
        filename: z.string()
          .optional()
          .describe('Optional filename for the screenshot (auto-generated if not provided)')
      },
      async ({ filename }) => {
        try {
          // Execute screenshot capture with error handling
          const result = await automationService.takeScreenshot(filename);
          
          return {
            content: [{
              type: 'text',
              text: result.message + (result.filename ? `\nFile: ${result.filename}` : '')
            }]
          };
        } catch (error) {
          // Handle and return errors gracefully
          return {
            content: [{
              type: 'text',
              text: `❌ Screenshot failed: ${error instanceof Error ? error.message : 'Unknown error'}`
            }]
          };
        }
      }
    );

    // ========================================================================
    // TOOL 2: APP LAUNCHING
    // ========================================================================
    server.tool(
      'launch_app',
      'Launch an iOS application by bundle identifier',
      {
        // Required bundle ID parameter with validation
        bundle_id: z.string()
          .min(1)
          .describe('iOS app bundle identifier (e.g., com.apple.mobilesafari)')
      },
      async ({ bundle_id }) => {
        try {
          // Execute app launch with validation
          const result = await automationService.launchApp(bundle_id);
          
          return {
            content: [{
              type: 'text',
              text: result.message + `\nBundle ID: ${result.bundleId}\nSuccess: ${result.success}`
            }]
          };
        } catch (error) {
          // Handle launch errors
          return {
            content: [{
              type: 'text',
              text: `❌ App launch failed: ${error instanceof Error ? error.message : 'Unknown error'}`
            }]
          };
        }
      }
    );

    // ========================================================================
    // TOOL 3: ADVANCED ELEMENT FINDING AND TAPPING
    // ========================================================================
    server.tool(
      'find_and_tap',
      'Find and tap UI elements using multiple search strategies with intelligent fallback',
      {
        // Multiple search criteria options
        element_text: z.string()
          .optional()
          .describe('Text content of the element to find and tap'),
        
        accessibility_id: z.string()
          .optional()
          .describe('Accessibility identifier of the element'),
        
        element_type: z.string()
          .optional()
          .describe('Type of element to find (e.g., button, textField, cell)'),
        
        // Search behavior modifiers
        partial_match: z.boolean()
          .default(false)
          .describe('Enable partial text matching for more flexible element finding'),
        
        // Automation workflow options
        take_screenshot: z.boolean()
          .default(true)
          .describe('Automatically take screenshot before and after tapping'),
        
        dismiss_after_screenshot: z.boolean()
          .default(false)
          .describe('Automatically dismiss modals/alerts after taking screenshot')
      },
      async (params) => {
        try {
          // Validate that at least one search criterion is provided
          if (!params.element_text && !params.accessibility_id && !params.element_type) {
            return {
              content: [{
                type: 'text',
                text: '❌ Error: At least one search criterion must be provided (element_text, accessibility_id, or element_type)'
              }]
            };
          }
          
          // Execute element finding and tapping
          const result = await automationService.findAndTap(params);
          
          return {
            content: [{
              type: 'text',
              text: result.message + `\nStrategy used: ${result.strategy}\nSuccess: ${result.success}`
            }]
          };
        } catch (error) {
          // Handle element finding errors
          return {
            content: [{
              type: 'text',
              text: `❌ Element finding failed: ${error instanceof Error ? error.message : 'Unknown error'}`
            }]
          };
        }
      }
    );

    // ========================================================================
    // TOOL 4: TEXT FIELD AUTOMATION
    // ========================================================================
    server.tool(
      'appium_tap_and_type',
      'Find text fields and type text using intelligent element detection with timeout control',
      {
        // Required text input
        text: z.string()
          .min(1)
          .describe('Text to type into the text field'),
        
        // Element targeting options
        element_type: z.string()
          .default('textField')
          .describe('Type of element to target (textField, searchField, etc.)'),
        
        // Timeout configuration
        timeout: z.number()
          .min(1)
          .max(60)
          .default(10)
          .describe('Maximum time to wait for element (1-60 seconds)')
      },
      async ({ text, element_type, timeout }) => {
        try {
          // Execute text field automation
          const result = await automationService.tapAndType({ text, element_type, timeout });
          
          return {
            content: [{
              type: 'text',
              text: result.message + `\nElement type: ${element_type}\nTimeout: ${timeout}s\nSuccess: ${result.success}`
            }]
          };
        } catch (error) {
          // Handle typing errors
          return {
            content: [{
              type: 'text',
              text: `❌ Text input failed: ${error instanceof Error ? error.message : 'Unknown error'}`
            }]
          };
        }
      }
    );

    // ========================================================================
    // TOOL 5: COMPLETE AUTOMATION DEMO
    // ========================================================================
    server.tool(
      'ios_automation_demo',
      'Execute a complete iOS automation workflow demonstration with configurable parameters',
      {
        // App configuration
        app_bundle_id: z.string()
          .default('com.google.doc-retrival-agent')
          .describe('Bundle ID of the app to demonstrate automation'),
        
        // Demo content
        demo_text: z.string()
          .default('Tell me about swift language in 5 bullet points')
          .describe('Text to use in the automation demo')
      },
      async ({ app_bundle_id, demo_text }) => {
        try {
          // Execute complete demo workflow
          const result = await automationService.runDemo({ app_bundle_id, demo_text });
          
          // Format the response with step-by-step breakdown
          const stepsText = result.steps.map((step, index) => 
            `${index + 1}. ${step}`
          ).join('\n');
          
          return {
            content: [{
              type: 'text',
              text: `${result.message}\n\n📋 Workflow Steps:\n${stepsText}\n\n📱 App: ${app_bundle_id}\n💬 Demo Text: "${demo_text}"\n✅ Success: ${result.success}`
            }]
          };
        } catch (error) {
          // Handle demo execution errors
          return {
            content: [{
              type: 'text',
              text: `❌ Demo execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`
            }]
          };
        }
      }
    );
  }
});

// ============================================================================
// NEXT.JS API ROUTE EXPORTS
// ============================================================================

// Export HTTP method handlers for Next.js API routes
// These handle the MCP protocol communication over HTTP

export const GET = handler;     // Handle GET requests (server info, capabilities)
export const POST = handler;    // Handle POST requests (tool execution, resource access)
export const DELETE = handler;  // Handle DELETE requests (cleanup, session management)
export const OPTIONS = handler; // Handle OPTIONS requests (CORS preflight) 