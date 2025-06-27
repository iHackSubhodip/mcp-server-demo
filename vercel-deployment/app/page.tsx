// Import React for TypeScript compatibility
import React from 'react';

// ============================================================================
// MAIN LANDING PAGE COMPONENT
// ============================================================================
// This component serves as the professional landing page for the iOS MCP Server
// deployed on Vercel, showcasing tools and providing configuration examples

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Main container with responsive padding and max width */}
      <div className="max-w-6xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        
        {/* ================================================================ */}
        {/* HERO SECTION */}
        {/* ================================================================ */}
        <div className="text-center mb-12">
          {/* Main heading with responsive typography */}
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
            📱 iOS MCP Server
          </h1>
          
          {/* Subtitle with professional description */}
          <p className="text-xl md:text-2xl text-gray-600 mb-6">
            Professional iOS Automation Server
          </p>
          
          {/* Status badge indicating deployment platform */}
          <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium mb-8">
            <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
            Deployed on Vercel
          </div>
          
          {/* Key features highlight */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              🚀 5 Automation Tools
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
              🔧 TypeScript
            </span>
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
              📡 MCP Protocol
            </span>
            <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
              ☁️ Serverless
            </span>
          </div>
        </div>

        {/* ================================================================ */}
        {/* MCP ENDPOINT CONFIGURATION */}
        {/* ================================================================ */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            🔧 MCP Endpoint Configuration
          </h2>
          
          {/* Current endpoint display */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <p className="text-sm text-gray-600 mb-2">MCP Server Endpoint:</p>
            <code className="text-lg font-mono text-blue-600 break-all">
              {/* Dynamic URL generation based on current host */}
              {typeof window !== 'undefined' 
                ? `${window.location.origin}/api/mcp`
                : 'https://your-app-name.vercel.app/api/mcp'
              }
            </code>
          </div>
          
          {/* Configuration examples for different MCP clients */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Claude Desktop Configuration */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Claude Desktop
              </h3>
              <div className="bg-gray-900 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
                <pre>{`{
  "mcpServers": {
    "ios-automation": {
      "url": "${typeof window !== 'undefined' 
        ? `${window.location.origin}/api/mcp`
        : 'https://your-app.vercel.app/api/mcp'
      }"
    }
  }
}`}</pre>
              </div>
            </div>
            
            {/* Cursor Configuration */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Cursor
              </h3>
              <div className="bg-gray-900 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
                <pre>{`{
  "mcpServers": {
    "ios-automation": {
      "url": "${typeof window !== 'undefined' 
        ? `${window.location.origin}/api/mcp`
        : 'https://your-app.vercel.app/api/mcp'
      }"
    }
  }
}`}</pre>
              </div>
            </div>
          </div>
        </div>

        {/* ================================================================ */}
        {/* AVAILABLE TOOLS SHOWCASE */}
        {/* ================================================================ */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            🛠️ Available Automation Tools
          </h2>
          
          {/* Tools grid with responsive layout */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            {/* Tool 1: Screenshot Capture */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">📸</span>
                <h3 className="text-lg font-semibold text-gray-800">take_screenshot</h3>
              </div>
              <p className="text-gray-600 text-sm mb-3">
                Capture high-quality screenshots of iOS device screens with optional custom filenames.
              </p>
              <div className="bg-gray-50 rounded p-2">
                <code className="text-xs text-gray-700">
                  filename?: string
                </code>
              </div>
            </div>
            
            {/* Tool 2: App Launching */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">🚀</span>
                <h3 className="text-lg font-semibold text-gray-800">launch_app</h3>
              </div>
              <p className="text-gray-600 text-sm mb-3">
                Launch iOS applications using bundle identifiers with validation and error handling.
              </p>
              <div className="bg-gray-50 rounded p-2">
                <code className="text-xs text-gray-700">
                  bundle_id: string
                </code>
              </div>
            </div>
            
            {/* Tool 3: Element Finding */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">🔍</span>
                <h3 className="text-lg font-semibold text-gray-800">find_and_tap</h3>
              </div>
              <p className="text-gray-600 text-sm mb-3">
                Advanced element finding with multiple strategies: text, accessibility ID, element type.
              </p>
              <div className="bg-gray-50 rounded p-2">
                <code className="text-xs text-gray-700">
                  element_text?, accessibility_id?, element_type?, partial_match?, take_screenshot?, dismiss_after_screenshot?
                </code>
              </div>
            </div>
            
            {/* Tool 4: Text Input */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">⌨️</span>
                <h3 className="text-lg font-semibold text-gray-800">appium_tap_and_type</h3>
              </div>
              <p className="text-gray-600 text-sm mb-3">
                Intelligent text field detection and typing with configurable timeouts and element types.
              </p>
              <div className="bg-gray-50 rounded p-2">
                <code className="text-xs text-gray-700">
                  text: string, element_type?: string, timeout?: number
                </code>
              </div>
            </div>
            
            {/* Tool 5: Demo Workflow */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">🎭</span>
                <h3 className="text-lg font-semibold text-gray-800">ios_automation_demo</h3>
              </div>
              <p className="text-gray-600 text-sm mb-3">
                Complete automation workflow demonstration with configurable app and demo content.
              </p>
              <div className="bg-gray-50 rounded p-2">
                <code className="text-xs text-gray-700">
                  app_bundle_id?: string, demo_text?: string
                </code>
              </div>
            </div>
            
            {/* Tool Count Summary */}
            <div className="border border-blue-200 bg-blue-50 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">🔢</span>
                <h3 className="text-lg font-semibold text-blue-800">Total Tools</h3>
              </div>
              <p className="text-blue-600 text-sm mb-3">
                5 professional automation tools ready for iOS app testing and interaction.
              </p>
              <div className="bg-blue-100 rounded p-2">
                <code className="text-xs text-blue-700">
                  All tools include comprehensive error handling and validation
                </code>
              </div>
            </div>
          </div>
        </div>

        {/* ================================================================ */}
        {/* TECHNICAL SPECIFICATIONS */}
        {/* ================================================================ */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            ⚙️ Technical Specifications
          </h2>
          
          {/* Specifications grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Runtime Environment */}
            <div className="text-center">
              <div className="text-3xl mb-2">🌐</div>
              <h3 className="font-semibold text-gray-800 mb-1">Runtime</h3>
              <p className="text-sm text-gray-600">Vercel Serverless</p>
              <p className="text-xs text-gray-500">Node.js 18+</p>
            </div>
            
            {/* Protocol Support */}
            <div className="text-center">
              <div className="text-3xl mb-2">📡</div>
              <h3 className="font-semibold text-gray-800 mb-1">Protocol</h3>
              <p className="text-sm text-gray-600">MCP 1.0.0</p>
              <p className="text-xs text-gray-500">SSE Transport</p>
            </div>
            
            {/* Type Safety */}
            <div className="text-center">
              <div className="text-3xl mb-2">🔒</div>
              <h3 className="font-semibold text-gray-800 mb-1">Type Safety</h3>
              <p className="text-sm text-gray-600">TypeScript</p>
              <p className="text-xs text-gray-500">Zod Validation</p>
            </div>
            
            {/* Performance */}
            <div className="text-center">
              <div className="text-3xl mb-2">⚡</div>
              <h3 className="font-semibold text-gray-800 mb-1">Performance</h3>
              <p className="text-sm text-gray-600">Cold Start: ~500ms</p>
              <p className="text-xs text-gray-500">5min Timeout</p>
            </div>
          </div>
        </div>

        {/* ================================================================ */}
        {/* EXTERNAL LINKS AND RESOURCES */}
        {/* ================================================================ */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            📚 Resources & Documentation
          </h2>
          
          {/* Links grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            {/* Demo Video */}
            <a 
              href="https://www.youtube.com/watch?v=480AmvL9ziQ"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <span className="text-2xl mr-3">🎥</span>
              <div>
                <h3 className="font-semibold text-gray-800">Demo Video</h3>
                <p className="text-sm text-gray-600">Watch iOS automation in action</p>
              </div>
            </a>
            
            {/* GitHub Repository */}
            <a 
              href="https://github.com/iHackSubhodip/mcp-server-demo"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <span className="text-2xl mr-3">📂</span>
              <div>
                <h3 className="font-semibold text-gray-800">Source Code</h3>
                <p className="text-sm text-gray-600">Full implementation on GitHub</p>
              </div>
            </a>
            
            {/* MCP Documentation */}
            <a 
              href="https://vercel.com/docs/mcp"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <span className="text-2xl mr-3">📖</span>
              <div>
                <h3 className="font-semibold text-gray-800">MCP Docs</h3>
                <p className="text-sm text-gray-600">Vercel MCP documentation</p>
              </div>
            </a>
          </div>
        </div>

        {/* ================================================================ */}
        {/* FOOTER */}
        {/* ================================================================ */}
        <div className="text-center mt-12 pt-8 border-t border-gray-200">
          <p className="text-gray-600 mb-2">
            Built with 💙 by{' '}
            <a 
              href="https://github.com/iHackSubhodip"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              iHackSubhodip
            </a>
          </p>
          <p className="text-sm text-gray-500">
            Deployed on Vercel • Powered by Next.js • MCP Protocol Compatible
          </p>
        </div>
      </div>
    </div>
  );
} 