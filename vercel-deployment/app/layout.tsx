// Import React for TypeScript compatibility
import React from 'react';
// Import global CSS styles for the entire application
import './globals.css'

// ============================================================================
// METADATA CONFIGURATION
// ============================================================================
// Define metadata for SEO, social sharing, and browser display
// This metadata is used by Next.js for automatic head tag generation

export const metadata = {
  // Basic page information
  title: 'iOS MCP Server - Professional iOS Automation on Vercel',
  description: 'Professional iOS automation server deployed on Vercel with 5 powerful tools for iOS app testing, screenshot capture, element finding, and workflow automation. Compatible with Claude Desktop and Cursor.',
  
  // Additional SEO metadata
  keywords: 'iOS automation, MCP server, Vercel deployment, mobile testing, Appium, Claude Desktop, Cursor, TypeScript',
  authors: [{ name: 'iHackSubhodip', url: 'https://github.com/iHackSubhodip' }],
  creator: 'iHackSubhodip',
  
  // Open Graph metadata for social media sharing
  openGraph: {
    title: 'iOS MCP Server - Professional iOS Automation',
    description: 'Professional iOS automation server with 5 powerful tools deployed on Vercel',
    url: 'https://ios-mcp-server.vercel.app',
    siteName: 'iOS MCP Server',
    images: [
      {
        url: '/og-image.png', // You can add this image later
        width: 1200,
        height: 630,
        alt: 'iOS MCP Server - Professional iOS Automation',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  
  // Twitter Card metadata
  twitter: {
    card: 'summary_large_image',
    title: 'iOS MCP Server - Professional iOS Automation',
    description: 'Professional iOS automation server with 5 powerful tools deployed on Vercel',
    creator: '@iHackSubhodip', // Add your Twitter handle if you have one
    images: ['/og-image.png'], // Same image as Open Graph
  },
  
  // Additional metadata
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  
  // Verification for search engines (add your verification codes)
  verification: {
    // google: 'your-google-verification-code',
    // yandex: 'your-yandex-verification-code',
    // yahoo: 'your-yahoo-verification-code',
  },
}

// ============================================================================
// ROOT LAYOUT COMPONENT
// ============================================================================
// This is the root layout that wraps all pages in the application
// It provides the basic HTML structure and global styles

export default function RootLayout({
  children,
}: {
  children: React.ReactNode  // Type definition for child components
}) {
  return (
    <html lang="en">
      {/* HTML head is automatically managed by Next.js using the metadata above */}
      
      <body className="antialiased">
        {/* Global body classes for better typography and styling */}
        {/* antialiased: Improves font rendering on various devices */}
        
        {/* Main content wrapper */}
        <main>
          {/* All page content will be rendered here */}
          {children}
        </main>
        
        {/* Optional: Add global scripts or components here */}
        {/* Example: Analytics, chat widgets, etc. */}
        
        {/* Development mode indicator (only visible in development) */}
        {typeof process !== 'undefined' && process.env.NODE_ENV === 'development' && (
          <div className="fixed bottom-4 right-4 bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium z-50">
            🚧 Development Mode
          </div>
        )}
      </body>
    </html>
  )
} 