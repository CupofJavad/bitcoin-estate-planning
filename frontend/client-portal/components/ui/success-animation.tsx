'use client'

import { useEffect, useState } from 'react'
import { CheckCircle2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SuccessAnimationProps {
  show: boolean
  message?: string
  onComplete?: () => void
  className?: string
}

export function SuccessAnimation({ 
  show, 
  message, 
  onComplete,
  className 
}: SuccessAnimationProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [shouldAnimate, setShouldAnimate] = useState(false)

  useEffect(() => {
    if (show) {
      setIsVisible(true)
      // Trigger animation after mount
      setTimeout(() => setShouldAnimate(true), 10)
      // Auto-hide after animation
      const timer = setTimeout(() => {
        setIsVisible(false)
        setShouldAnimate(false)
        onComplete?.()
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [show, onComplete])

  if (!isVisible) return null

  return (
    <div
      className={cn(
        'fixed inset-0 z-50 flex items-center justify-center pointer-events-none',
        className
      )}
    >
      <div
        className={cn(
          'bg-white dark:bg-gray-800 rounded-lg shadow-large p-6 flex flex-col items-center space-y-4',
          'transform transition-all duration-300',
          shouldAnimate
            ? 'scale-100 opacity-100'
            : 'scale-75 opacity-0'
        )}
      >
        <CheckCircle2
          className={cn(
            'h-16 w-16 text-success',
            'transform transition-all duration-500',
            shouldAnimate ? 'scale-100 rotate-0' : 'scale-0 rotate-180'
          )}
        />
        {message && (
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {message}
          </p>
        )}
      </div>
    </div>
  )
}

