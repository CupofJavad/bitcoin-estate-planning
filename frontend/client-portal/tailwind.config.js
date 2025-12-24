/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        // Bitcoin-inspired color palette
        bitcoin: {
          orange: '#F7931A',      // Bitcoin orange (primary)
          'orange-dark': '#E8820A',
          'orange-light': '#FFA64D',
        },
        // Enhanced status colors
        success: {
          DEFAULT: '#10B981',
          dark: '#059669',
          light: '#34D399',
        },
        warning: {
          DEFAULT: '#F59E0B',
          dark: '#D97706',
          light: '#FBBF24',
        },
        error: {
          DEFAULT: '#EF4444',
          dark: '#DC2626',
          light: '#F87171',
        },
      },
      // Enhanced spacing scale
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      // Enhanced border radius
      borderRadius: {
        '4xl': '2rem',
      },
      // Enhanced shadows
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'medium': '0 4px 12px rgba(0, 0, 0, 0.1)',
        'large': '0 8px 24px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  plugins: [],
}
