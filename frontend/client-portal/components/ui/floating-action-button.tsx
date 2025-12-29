'use client'

import { ButtonHTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { Plus } from 'lucide-react'

interface FloatingActionButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon?: ReactNode
  label?: string
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left'
}

export function FloatingActionButton({
  icon,
  label,
  position = 'bottom-right',
  className,
  ...props
}: FloatingActionButtonProps) {
  const positions = {
    'bottom-right': 'bottom-6 right-6',
    'bottom-left': 'bottom-6 left-6',
    'top-right': 'top-6 right-6',
    'top-left': 'top-6 left-6',
  }

  return (
    <button
      className={cn(
        'fixed z-50 flex items-center gap-2 px-6 py-4 bg-bitcoin-orange text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-110 active:scale-95',
        positions[position],
        className
      )}
      {...props}
    >
      {icon || <Plus className="h-5 w-5" />}
      {label && <span className="font-medium">{label}</span>}
    </button>
  )
}

