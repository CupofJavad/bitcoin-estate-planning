'use client'

import { SessionProvider } from 'next-auth/react'
import { useEffect } from 'react'
import { errorLogger } from '@/lib/error-logger'

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Log any session errors
    const originalError = console.error
    console.error = (...args) => {
      if (args[0]?.includes?.('next-auth') || args[0]?.includes?.('getSession')) {
        errorLogger.logError(
          'NextAuth session error',
          args[0] instanceof Error ? args[0] : new Error(String(args[0])),
          { action: 'session_error', component: 'SessionProvider' }
        )
      }
      originalError.apply(console, args)
    }
    
    return () => {
      console.error = originalError
    }
  }, [])

  return (
    <SessionProvider
      refetchInterval={5 * 60} // Refetch session every 5 minutes
      refetchOnWindowFocus={true}
    >
      {children}
    </SessionProvider>
  )
}

