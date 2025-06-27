/** @type {import('next').NextConfig} */

// Next.js configuration for iOS MCP Server deployment on Vercel
const nextConfig = {
  // Experimental features for better compatibility
  experimental: {
    // Prevent bundling of server-side packages that should remain external
    // This is crucial for @vercel/mcp-adapter to work properly
    serverComponentsExternalPackages: ['@vercel/mcp-adapter']
  },

  // Custom headers configuration for API routes
  async headers() {
    return [
      {
        // Apply CORS headers specifically to the MCP API endpoint
        source: '/api/mcp',
        headers: [
          // Allow requests from any origin (required for MCP clients)
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          // Specify allowed HTTP methods for the MCP protocol
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, DELETE, OPTIONS',
          },
          // Allow necessary headers for MCP communication
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization, x-requested-with',
          },
          // Enable credentials for authenticated requests if needed
          {
            key: 'Access-Control-Allow-Credentials',
            value: 'true',
          },
          // Cache preflight requests for 24 hours to improve performance
          {
            key: 'Access-Control-Max-Age',
            value: '86400',
          },
        ],
      },
    ]
  },

  // Optimize images for better performance
  images: {
    // Allow external image domains if needed for screenshots or icons
    domains: [],
    // Use modern image formats for better compression
    formats: ['image/webp', 'image/avif'],
  },

  // Webpack configuration for additional optimizations
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add any custom webpack configurations here if needed
    return config
  },

  // Environment variables that will be available at build time
  env: {
    // Custom environment variable to identify Vercel deployment
    DEPLOYMENT_PLATFORM: 'vercel',
  },

  // Redirect configuration for better SEO and UX
  async redirects() {
    return [
      // Redirect old paths to new ones if needed
      // Example: redirect /old-path to /new-path
    ]
  },

  // Rewrite configuration for URL masking if needed
  async rewrites() {
    return [
      // Add URL rewrites here if needed
      // Example: rewrite /api/v1/mcp to /api/mcp
    ]
  },
}

// Export the configuration
module.exports = nextConfig 