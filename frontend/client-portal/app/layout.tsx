import type { Metadata } from 'next'
import './globals.css'
import { ThemeProvider } from '@/contexts/theme-context'

export const metadata: Metadata = {
  title: 'Bitcoin Estate Planning Platform',
  description: 'Bitcoin-native estate planning with timelock policies and beneficiary management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}

