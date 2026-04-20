/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'blostem-bg': '#FFFFFF',
        'blostem-surface': '#F8F8F6',
        'blostem-border': '#E8E7E2',
        'blostem-text': '#1A1A1A',
        'blostem-text-secondary': '#6B6A65',
        'blostem-text-muted': '#9B9A95',
        'blostem-green': '#639922',
        'blostem-green-light': '#EAF3DE',
        'blostem-green-text': '#27500A',
        'blostem-amber': '#BA7517',
        'blostem-amber-light': '#FAEEDA',
        'blostem-amber-text': '#633806',
        'blostem-red': '#E24B4A',
        'blostem-red-light': '#FCEBEB',
        'blostem-red-text': '#791F1F',
        'blostem-blue': '#0C447C',
        'blostem-blue-light': '#E6F1FB',
        'blostem-purple': '#3C3489',
        'blostem-purple-light': '#EEEDFE',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      fontSize: {
        'xs': '11px',
        'sm': '13px',
        'base': '14px',
        'lg': '15px',
        'xl': '22px',
      },
      fontWeight: {
        'normal': '400',
        'medium': '500',
      },
      lineHeight: {
        'tight': '1.6',
      },
      spacing: {
        '0.5': '2px',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
      },
      borderRadius: {
        'sm': '6px',
        'md': '8px',
        'lg': '10px',
        'full': '20px',
      },
    },
  },
  plugins: [],
}
