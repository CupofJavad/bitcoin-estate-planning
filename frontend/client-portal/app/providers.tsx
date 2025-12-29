'use client'

import { SessionProvider } from 'next-auth/react'
import { useEffect } from 'react'
import { errorLogger } from '@/lib/error-logger'

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Log any session errors - use a safer approach that won't fail
    const originalError = console.error.bind(console)
    const wrappedError = (...args: any[]) => {
      // Always call original first to ensure error is logged
      try {
        originalError(...args)
      } catch {
        // If even original fails, try direct console access
        if (typeof window !== 'undefined' && window.console && window.console.error) {
          try {
            window.console.error(...args)
          } catch {
            // Silently fail if all error logging fails
          }
        }
      }
      
      // Then try to log to our error logger (non-blocking)
      try {
        const firstArg = args[0]
        const firstArgStr = typeof firstArg === 'string' ? firstArg : String(firstArg)
        
        // Only log specific errors to avoid noise
        if (firstArgStr.includes('Login error') || 
            firstArgStr.includes('CredentialsSignin') ||
            firstArgStr.includes('next-auth') || 
            firstArgStr.includes('getSession')) {
          const error = firstArg instanceof Error 
            ? firstArg 
            : new Error(firstArgStr)
          // Use setTimeout to make this non-blocking
          setTimeout(() => {
            try {
              errorLogger.logError(
                'Authentication error',
                error,
                { action: 'auth_error', component: 'SessionProvider' }
              )
            } catch {
              // Silently fail if error logging fails
            }
          }, 0)
        }
      } catch {
        // Silently fail if error processing fails
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

