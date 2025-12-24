'use client'

import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface BadgeProps {
  children: ReactNode
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Badge({ 
  children, 
  variant = 'default', 
  size = 'md',
  className 
}: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full font-medium',
        {
          // Variants
          'bg-bitcoin-orange text-white': variant === 'default',
          'bg-success text-white': variant === 'success',
          'bg-warning text-white': variant === 'warning',
          'bg-error text-white': variant === 'error',
          'bg-blue-500 text-white': variant === 'info',
          // Sizes
          'px-2 py-0.5 text-xs': size === 'sm',
          'px-2.5 py-1 text-sm': size === 'md',
          'px-3 py-1.5 text-base': size === 'lg',
        },
        className
      )}
    >
      {children}
    </span>
  )
}

