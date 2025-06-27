/** @type {import('tailwindcss').Config} */

// Tailwind CSS configuration for iOS MCP Server
// This configuration customizes Tailwind's default settings for our specific needs

module.exports = {
  // Content paths - tells Tailwind where to look for classes to include in the final CSS
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',     // Pages directory (if using Pages Router)
    './components/**/*.{js,ts,jsx,tsx,mdx}', // Components directory
    './app/**/*.{js,ts,jsx,tsx,mdx}',       // App directory (App Router)
    './src/**/*.{js,ts,jsx,tsx,mdx}',       // Source directory (if using src folder)
  ],
  
  // Theme customization - extend or override Tailwind's default theme
  theme: {
    extend: {
      // Custom color palette for the iOS MCP Server brand
      colors: {
        // Primary brand colors
        primary: {
          50: '#eff6ff',   // Very light blue
          100: '#dbeafe',  // Light blue
          200: '#bfdbfe',  // Medium light blue
          300: '#93c5fd',  // Medium blue
          400: '#60a5fa',  // Medium dark blue
          500: '#3b82f6',  // Default blue (primary)
          600: '#2563eb',  // Dark blue
          700: '#1d4ed8',  // Darker blue
          800: '#1e40af',  // Very dark blue
          900: '#1e3a8a',  // Darkest blue
        },
        
        // Secondary colors for accents
        secondary: {
          50: '#f8fafc',   // Very light gray
          100: '#f1f5f9',  // Light gray
          200: '#e2e8f0',  // Medium light gray
          300: '#cbd5e1',  // Medium gray
          400: '#94a3b8',  // Medium dark gray
          500: '#64748b',  // Default gray (secondary)
          600: '#475569',  // Dark gray
          700: '#334155',  // Darker gray
          800: '#1e293b',  // Very dark gray
          900: '#0f172a',  // Darkest gray
        },
        
        // Success colors for positive feedback
        success: {
          50: '#f0fdf4',   // Very light green
          100: '#dcfce7',  // Light green
          200: '#bbf7d0',  // Medium light green
          300: '#86efac',  // Medium green
          400: '#4ade80',  // Medium dark green
          500: '#22c55e',  // Default green (success)
          600: '#16a34a',  // Dark green
          700: '#15803d',  // Darker green
          800: '#166534',  // Very dark green
          900: '#14532d',  // Darkest green
        },
        
        // Warning colors for caution states
        warning: {
          50: '#fffbeb',   // Very light yellow
          100: '#fef3c7',  // Light yellow
          200: '#fde68a',  // Medium light yellow
          300: '#fcd34d',  // Medium yellow
          400: '#fbbf24',  // Medium dark yellow
          500: '#f59e0b',  // Default yellow (warning)
          600: '#d97706',  // Dark yellow
          700: '#b45309',  // Darker yellow
          800: '#92400e',  // Very dark yellow
          900: '#78350f',  // Darkest yellow
        },
        
        // Error colors for error states
        error: {
          50: '#fef2f2',   // Very light red
          100: '#fee2e2',  // Light red
          200: '#fecaca',  // Medium light red
          300: '#fca5a5',  // Medium red
          400: '#f87171',  // Medium dark red
          500: '#ef4444',  // Default red (error)
          600: '#dc2626',  // Dark red
          700: '#b91c1c',  // Darker red
          800: '#991b1b',  // Very dark red
          900: '#7f1d1d',  // Darkest red
        },
      },
      
      // Custom font families
      fontFamily: {
        sans: [
          'Inter',                    // Modern, clean font
          '-apple-system',            // Apple system font
          'BlinkMacSystemFont',       // Blink engine system font
          'Segoe UI',                 // Windows system font
          'Roboto',                   // Android system font
          'Oxygen',                   // KDE system font
          'Ubuntu',                   // Ubuntu system font
          'Cantarell',                // GNOME system font
          'sans-serif',               // Fallback
        ],
        mono: [
          'JetBrains Mono',           // Developer-friendly monospace
          'Fira Code',                // Another good monospace option
          'Monaco',                   // macOS monospace
          'Consolas',                 // Windows monospace
          'Liberation Mono',          // Linux monospace
          'Courier New',              // Universal monospace fallback
          'monospace',                // System monospace fallback
        ],
      },
      
      // Custom spacing values
      spacing: {
        '18': '4.5rem',    // 72px - useful for custom layouts
        '88': '22rem',     // 352px - for larger components
        '128': '32rem',    // 512px - for very large components
      },
      
      // Custom border radius values
      borderRadius: {
        'xl': '1rem',      // 16px - larger rounded corners
        '2xl': '1.5rem',   // 24px - very large rounded corners
        '3xl': '2rem',     // 32px - extra large rounded corners
      },
      
      // Custom box shadows for depth
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 30px -5px rgba(0, 0, 0, 0.05)',
        'hard': '0 10px 40px -10px rgba(0, 0, 0, 0.15), 0 20px 50px -10px rgba(0, 0, 0, 0.1)',
      },
      
      // Custom animations and transitions
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'bounce-subtle': 'bounceSubtle 1s ease-in-out infinite',
      },
      
      // Custom keyframes for animations
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
      
      // Custom breakpoints for responsive design
      screens: {
        'xs': '475px',     // Extra small devices
        'sm': '640px',     // Small devices (default)
        'md': '768px',     // Medium devices (default)
        'lg': '1024px',    // Large devices (default)
        'xl': '1280px',    // Extra large devices (default)
        '2xl': '1536px',   // 2X large devices (default)
        '3xl': '1920px',   // Ultra wide screens
      },
      
      // Custom typography settings
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],      // 12px
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],   // 14px
        'base': ['1rem', { lineHeight: '1.5rem' }],      // 16px
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],   // 18px
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],    // 20px
        '2xl': ['1.5rem', { lineHeight: '2rem' }],       // 24px
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],  // 30px
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],    // 36px
        '5xl': ['3rem', { lineHeight: '1' }],            // 48px
        '6xl': ['3.75rem', { lineHeight: '1' }],         // 60px
        '7xl': ['4.5rem', { lineHeight: '1' }],          // 72px
        '8xl': ['6rem', { lineHeight: '1' }],            // 96px
        '9xl': ['8rem', { lineHeight: '1' }],            // 128px
      },
    },
  },
  
  // Plugins - extend Tailwind's functionality
  plugins: [
    // Add forms plugin for better form styling
    // require('@tailwindcss/forms'),
    
    // Add typography plugin for rich text content
    // require('@tailwindcss/typography'),
    
    // Add aspect ratio plugin for responsive media
    // require('@tailwindcss/aspect-ratio'),
    
    // Add line clamp plugin for text truncation
    // require('@tailwindcss/line-clamp'),
  ],
  
  // Dark mode configuration
  darkMode: 'class', // Enable class-based dark mode (add 'dark' class to html/body)
  
  // Prefix for all Tailwind classes (useful for avoiding conflicts)
  // prefix: 'tw-',
  
  // Important modifier to make all utilities important
  // important: true,
  
  // Separator for responsive and state variants
  separator: ':',
  
  // Core plugins to disable (if you want to reduce bundle size)
  corePlugins: {
    // Disable unused core plugins to reduce CSS bundle size
    // preflight: false,        // Disable base styles
    // container: false,        // Disable container component
    // accessibility: false,    // Disable screen reader utilities
  },
} 