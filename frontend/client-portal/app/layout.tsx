import type { Metadata } from 'next'
import './globals.css'
import { ThemeProvider } from '@/contexts/theme-context'
import { Providers } from './providers'

export const metadata: Metadata = {
  title: 'Bitcoin Estate Planning Platform',
  description: 'Bitcoin-native estate planning with timelock policies and beneficiary management',
  keywords: ['Bitcoin', 'Estate Planning', 'Cryptocurrency', 'Inheritance', 'Timelock'],
  authors: [{ name: 'Bitcoin Estate Planning Team' }],
  viewport: 'width=device-width, initial-scale=1, maximum-scale=5',
  themeColor: '#F7931A',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </Providers>
      </body>
    </html>
  )
}

