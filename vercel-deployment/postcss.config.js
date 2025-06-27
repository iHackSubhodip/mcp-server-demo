// PostCSS configuration for iOS MCP Server
// PostCSS is a tool for transforming CSS with JavaScript plugins
// This configuration is required for Tailwind CSS to work properly

module.exports = {
  plugins: {
    // Tailwind CSS plugin - processes Tailwind directives and generates utility classes
    // This must be first in the plugins array to ensure proper processing order
    tailwindcss: {},
    
    // Autoprefixer plugin - adds vendor prefixes to CSS rules
    // Ensures cross-browser compatibility by automatically adding prefixes like -webkit-, -moz-, etc.
    // Uses browserslist configuration to determine which prefixes to add
    autoprefixer: {},
    
    // Optional: CSS Nano plugin for production optimization
    // Uncomment the following lines to enable CSS minification in production
    // This will reduce the final CSS bundle size significantly
    /*
    ...(process.env.NODE_ENV === 'production' ? {
      cssnano: {
        preset: 'default',  // Use default optimization preset
      }
    } : {})
    */
    
    // Optional: PostCSS Import plugin
    // Allows @import statements in CSS files
    // Uncomment if you need to import CSS files from node_modules or other locations
    /*
    'postcss-import': {},
    */
    
    // Optional: PostCSS Nested plugin
    // Allows nested CSS rules (similar to Sass)
    // Note: Tailwind CSS already supports some nesting, so this may not be necessary
    /*
    'postcss-nested': {},
    */
    
    // Optional: PostCSS Custom Properties plugin
    // Provides better support for CSS custom properties (variables)
    /*
    'postcss-custom-properties': {},
    */
    
    // Optional: PostCSS Flexbugs Fixes plugin
    // Fixes common flexbox bugs across different browsers
    /*
    'postcss-flexbugs-fixes': {},
    */
  },
}

// Alternative configuration using array syntax (if you need more control)
/*
module.exports = {
  plugins: [
    // Tailwind CSS with custom configuration
    require('tailwindcss')('./tailwind.config.js'),
    
    // Autoprefixer with custom browserslist
    require('autoprefixer')({
      overrideBrowserslist: [
        '> 1%',           // Support browsers with >1% market share
        'last 2 versions', // Support last 2 versions of each browser
        'Firefox ESR',     // Support Firefox Extended Support Release
        'not dead',        // Exclude browsers without official support
        'not ie <= 11',    // Exclude Internet Explorer 11 and below
      ],
    }),
    
    // Production optimizations
    ...(process.env.NODE_ENV === 'production' ? [
      require('cssnano')({
        preset: ['default', {
          discardComments: {
            removeAll: true,  // Remove all comments in production
          },
          normalizeWhitespace: true,  // Normalize whitespace
          colormin: true,             // Minimize color values
          convertValues: true,        // Convert values to shorter equivalents
          discardDuplicates: true,    // Remove duplicate rules
          discardEmpty: true,         // Remove empty rules
          mergeRules: true,           // Merge similar rules
          minifyFontValues: true,     // Minify font declarations
          minifyParams: true,         // Minify at-rule parameters
          minifySelectors: true,      // Minify selectors
          normalizeCharset: true,     // Normalize charset declarations
          normalizeDisplayValues: true, // Normalize display values
          normalizePositions: true,   // Normalize position values
          normalizeRepeatStyle: true, // Normalize repeat-style values
          normalizeString: true,      // Normalize string values
          normalizeTimingFunctions: true, // Normalize timing functions
          normalizeUnicode: true,     // Normalize unicode values
          normalizeUrl: true,         // Normalize URL values
          orderedValues: true,        // Order values consistently
          reduceIdents: true,         // Reduce custom identifiers
          reduceInitial: true,        // Reduce initial values
          reduceTransforms: true,     // Reduce transform functions
          svgo: true,                 // Optimize SVG values
          uniqueSelectors: true,      // Remove duplicate selectors
        }],
      }),
    ] : []),
  ],
}
*/ 