# iOS MCP Server - Vercel Deployment

> 📁 **Organized Structure**: All Vercel deployment files are contained in this single folder for easy management.

## 📋 **Package.json Explained**

```json
{
  "scripts": {
    "dev": "next dev",           // Development server for local testing
    "build": "next build",       // Production build for Vercel deployment  
    "start": "next start",       // Start production server locally
    "lint": "next lint",         // Lint code for errors and style issues
    "test:mcp": "..."           // Test MCP server locally with inspector
  },
  "dependencies": {
    "@vercel/mcp-adapter": "...", // Vercel's official MCP adapter for seamless integration
    "next": "14.0.0",            // Next.js framework for the web application
    "react": "^18.0.0",          // React for UI components
    "zod": "^3.22.0",            // Schema validation for MCP tool parameters
    "typescript": "^5.0.0"       // TypeScript for type safety
  }
}
```

## 🚀 **Deploy to Vercel**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FiHackSubhodip%2Fmcp-server-demo%2Ftree%2Fmain%2Fvercel-deployment)

## 📁 **File Structure**

```
vercel-deployment/
├── package.json              # Dependencies and scripts
├── next.config.js           # Next.js configuration with CORS
├── vercel.json              # Vercel deployment settings
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.js        # PostCSS configuration for Tailwind
├── app/
│   ├── layout.tsx           # Root layout component
│   ├── page.tsx             # Landing page with MCP info
│   ├── globals.css          # Global styles with Tailwind
│   └── api/
│       └── mcp/
│           └── route.ts     # Main MCP API endpoint
└── README.md               # This documentation file
```

## 🔧 **Configuration Files Explained**

### **next.config.js**
```javascript
// Next.js configuration with CORS headers for MCP protocol
const nextConfig = {
  experimental: {
    // External packages that should not be bundled
    serverComponentsExternalPackages: ['@vercel/mcp-adapter']
  },
  async headers() {
    return [
      {
        source: '/api/mcp',  // MCP endpoint
        headers: [
          // CORS headers for cross-origin requests
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' }
        ]
      }
    ]
  }
}
```

### **vercel.json**
```json
{
  "functions": {
    // Set maximum duration for MCP function (5 minutes)
    "app/api/mcp/route.ts": { "maxDuration": 300 }
  },
  "framework": "nextjs",        // Framework detection
  "regions": ["iad1"],          // Deploy to US East region
  "env": {
    // Environment variable to indicate Vercel deployment
    "DEPLOYMENT_ENV": "vercel"
  }
}
```

## 🛠️ **MCP Tools Implementation**

The main MCP server (`app/api/mcp/route.ts`) includes:

### **1. take_screenshot**
```typescript
// Simulates iOS screenshot capture
server.tool(
  'take_screenshot',
  'Capture a screenshot of the iOS device screen',
  { filename: z.string().optional() },  // Optional filename parameter
  async ({ filename }) => {
    // Mock implementation returns simulated success
    const result = await automationService.takeScreenshot(filename);
    return { content: [{ type: 'text', text: result.message }] };
  }
);
```

### **2. launch_app**
```typescript
// Simulates iOS app launching
server.tool(
  'launch_app',
  'Launch an iOS application by bundle identifier',
  { bundle_id: z.string() },  // Required bundle ID parameter
  async ({ bundle_id }) => {
    // Mock implementation with 1-second delay
    const result = await automationService.launchApp(bundle_id);
    return { content: [{ type: 'text', text: result.message }] };
  }
);
```

### **3. find_and_tap**
```typescript
// Advanced element finding and tapping
server.tool(
  'find_and_tap',
  'Find and tap UI elements using multiple strategies',
  {
    element_text: z.string().optional(),        // Text-based finding
    accessibility_id: z.string().optional(),   // Accessibility ID finding
    element_type: z.string().optional(),       // Element type filtering
    partial_match: z.boolean().default(false), // Partial text matching
    take_screenshot: z.boolean().default(true), // Auto-screenshot
    dismiss_after_screenshot: z.boolean().default(false) // Auto-dismiss modals
  },
  async (params) => {
    // Validates at least one search criterion is provided
    if (!params.element_text && !params.accessibility_id && !params.element_type) {
      return { content: [{ type: 'text', text: 'Error: At least one search criterion required' }] };
    }
    // Mock implementation with 1.5-second delay
    const result = await automationService.findAndTap(params);
    return { content: [{ type: 'text', text: result.message }] };
  }
);
```

### **4. appium_tap_and_type**
```typescript
// Text field automation
server.tool(
  'appium_tap_and_type',
  'Find text fields and type text using intelligent element detection',
  {
    text: z.string(),                           // Required text to type
    element_type: z.string().default('textField'), // Element type filter
    timeout: z.number().default(10)            // Timeout in seconds
  },
  async ({ text, element_type, timeout }) => {
    // Mock implementation with typing simulation
    const result = await automationService.tapAndType({ text, element_type, timeout });
    return { content: [{ type: 'text', text: result.message }] };
  }
);
```

### **5. ios_automation_demo**
```typescript
// Complete workflow demonstration
server.tool(
  'ios_automation_demo',
  'Run a complete iOS automation demo workflow',
  {
    app_bundle_id: z.string().default('com.google.doc-retrival-agent'),
    demo_text: z.string().default('Tell me about swift language in 5 bullet points')
  },
  async ({ app_bundle_id, demo_text }) => {
    // Simulates complete workflow:
    // 1. Launch app
    // 2. Take screenshots
    // 3. Navigate through UI
    // 4. Type text
    // 5. Send message
    const steps = [
      '🚀 Launching app',
      '📸 Taking screenshots', 
      '⚙️ Tapping buttons',
      '⌨️ Typing text',
      '📤 Sending message'
    ];
    return { content: [{ type: 'text', text: 'Demo completed: ' + steps.join(' → ') }] };
  }
);
```

## 🎨 **UI Components**

### **Landing Page (app/page.tsx)**
```typescript
// Professional landing page with:
// - Tool showcase
// - MCP endpoint information  
// - Configuration examples
// - Links to documentation and demo video
export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Beautiful gradient background with Tailwind CSS */}
      <div className="max-w-4xl mx-auto text-center">
        {/* Responsive design with mobile-first approach */}
        <h1 className="text-4xl md:text-6xl font-bold">📱 iOS MCP Server</h1>
        {/* Tool showcase grid */}
        {/* MCP configuration examples */}
        {/* External links to docs and video */}
      </div>
    </div>
  );
}
```

### **Root Layout (app/layout.tsx)**
```typescript
// Root layout with metadata and global styles
export const metadata = {
  title: 'iOS MCP Server',                    // Page title
  description: 'Professional iOS automation server deployed on Vercel'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>  {/* Global layout wrapper */}
    </html>
  )
}
```

## 🧪 **Local Development**

```bash
# 1. Navigate to deployment folder
cd vercel-deployment

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Test MCP endpoint
npm run test:mcp

# 5. Build for production
npm run build
```

## 🌐 **Deployment Steps**

### **Option 1: One-Click Deploy**
1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Deploy automatically

### **Option 2: Manual Deploy**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from this folder
cd vercel-deployment
vercel

# Follow prompts to configure
```

### **Option 3: GitHub Integration**
1. Push this folder to GitHub
2. Connect repository to Vercel
3. Set root directory to `vercel-deployment`
4. Auto-deploy on every push

## 🔧 **MCP Client Configuration**

### **Claude Desktop**
```json
{
  "mcpServers": {
    "ios-automation": {
      "url": "https://your-app-name.vercel.app/api/mcp"
    }
  }
}
```

### **Cursor**
```json
{
  "mcpServers": {
    "ios-automation": {
      "url": "https://your-app-name.vercel.app/api/mcp"
    }
  }
}
```

## 📊 **Architecture Benefits**

- ✅ **Single Folder**: All files organized in one place
- ✅ **Well Commented**: Extensive inline documentation
- ✅ **Type Safe**: Full TypeScript implementation
- ✅ **Mock Automation**: Simulated iOS automation for demo
- ✅ **Professional UI**: Beautiful landing page
- ✅ **Vercel Optimized**: Uses official MCP adapter
- ✅ **Error Handling**: Comprehensive error responses

## 🔄 **Future Enhancements**

For production iOS automation:
1. **Hybrid Architecture**: Connect to real macOS automation backend
2. **Authentication**: Add API key protection
3. **Rate Limiting**: Implement request throttling
4. **Monitoring**: Add observability and logging
5. **Caching**: Implement response caching

## 📚 **Resources**

- [Vercel MCP Documentation](https://vercel.com/docs/mcp)
- [Original iOS MCP Server](https://github.com/iHackSubhodip/mcp-server-demo)
- [Demo Video](https://www.youtube.com/watch?v=480AmvL9ziQ)

## 🎉 **Ready to Deploy!**

This organized structure makes it easy to:
- **Understand** each file's purpose
- **Modify** configurations as needed
- **Deploy** with confidence
- **Maintain** the codebase long-term 