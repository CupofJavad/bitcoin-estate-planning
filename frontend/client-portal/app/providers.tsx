'use client'

import { SessionProvider } from 'next-auth/react'
import { useEffect } from 'react'
import { errorLogger } from '@/lib/error-logger'

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Log any session errors - use a safer approach
    const originalError = console.error.bind(console)
    const wrappedError = (...args: any[]) => {
      try {
        const firstArg = args[0]
        const firstArgStr = typeof firstArg === 'string' ? firstArg : String(firstArg)
        
        if (firstArgStr.includes('next-auth') || firstArgStr.includes('getSession')) {
          const error = firstArg instanceof Error 
            ? firstArg 
            : new Error(firstArgStr)
          errorLogger.logError(
            'NextAuth session error',
            error,
            { action: 'session_error', component: 'SessionProvider' }
          )
        }
        // Call original error function
        originalError(...args)
      } catch (err) {
        // Fallback if error logging fails - use native console.error
        try {
          originalError('Error in error handler:', err)
          originalError(...args)
        } catch {
          // Last resort - direct console access
          if (typeof window !== 'undefined' && window.console && window.console.error) {
            window.console.error(...args)
          }
        }
      }
    }
    
    console.error = wrappedError
    
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

