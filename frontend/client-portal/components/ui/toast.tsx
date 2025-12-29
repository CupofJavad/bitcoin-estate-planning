'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, Info, AlertCircle, X } from 'lucide-react'
import { cn } from '@/lib/utils'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

interface Toast {
  id: string
  message: string
  type: ToastType
}

let toastListeners: ((toasts: Toast[]) => void)[] = []
let toasts: Toast[] = []

function notify() {
  toastListeners.forEach(listener => listener([...toasts]))
}

export function toast(message: string, type: ToastType = 'info') {
  const id = Math.random().toString(36).substring(7)
  toasts.push({ id, message, type })
  notify()
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    toasts = toasts.filter(t => t.id !== id)
    notify()
  }, 5000)
}

export function ToastContainer() {
  const [currentToasts, setCurrentToasts] = useState<Toast[]>([])

  useEffect(() => {
    const listener = (newToasts: Toast[]) => {
      setCurrentToasts(newToasts)
    }
    toastListeners.push(listener)
    return () => {
      toastListeners = toastListeners.filter(l => l !== listener)
    }
  }, [])

  if (currentToasts.length === 0) return null

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {currentToasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            'flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg min-w-[300px] max-w-md transition-all duration-300 ease-in-out animate-in slide-in-from-right',
            {
              'bg-green-50 text-green-800 border border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800': toast.type === 'success',
              'bg-red-50 text-red-800 border border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800': toast.type === 'error',
              'bg-blue-50 text-blue-800 border border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800': toast.type === 'info',
              'bg-yellow-50 text-yellow-800 border border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800': toast.type === 'warning',
            }
          )}
        >
          {toast.type === 'success' && <CheckCircle className="h-5 w-5 animate-pulse" />}
          {toast.type === 'error' && <XCircle className="h-5 w-5" />}
          {toast.type === 'info' && <Info className="h-5 w-5" />}
          {toast.type === 'warning' && <AlertCircle className="h-5 w-5" />}
          <p className="flex-1 text-sm font-medium">{toast.message}</p>
          <button
            onClick={() => {
              toasts = toasts.filter(t => t.id !== toast.id)
              notify()
            }}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ))}
    </div>
  )
}

