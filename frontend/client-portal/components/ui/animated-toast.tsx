'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, Info, AlertCircle, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { toast, ToastType } from './toast'

interface AnimatedToastProps {
  id: string
  message: string
  type: ToastType
  onClose: (id: string) => void
}

export function AnimatedToast({ id, message, type, onClose }: AnimatedToastProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [isExiting, setIsExiting] = useState(false)

  useEffect(() => {
    // Trigger entrance animation
    setTimeout(() => setIsVisible(true), 10)
  }, [])

  const handleClose = () => {
    setIsExiting(true)
    setTimeout(() => onClose(id), 300)
  }

  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: Info,
    warning: AlertCircle,
  }

  const Icon = icons[type]

  return (
    <div
      className={cn(
        'flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg min-w-[300px] max-w-md transition-all duration-300 ease-in-out',
        {
          'bg-green-50 text-green-800 border border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800': type === 'success',
          'bg-red-50 text-red-800 border border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800': type === 'error',
          'bg-blue-50 text-blue-800 border border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800': type === 'info',
          'bg-yellow-50 text-yellow-800 border border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800': type === 'warning',
          'translate-x-0 opacity-100': isVisible && !isExiting,
          '-translate-x-full opacity-0': !isVisible || isExiting,
        }
      )}
    >
      <Icon className={cn('h-5 w-5 flex-shrink-0', {
        'animate-bounce': type === 'error',
        'animate-pulse': type === 'success',
      })} />
      <p className="flex-1 text-sm font-medium">{message}</p>
      <button
        onClick={handleClose}
        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  )
}

