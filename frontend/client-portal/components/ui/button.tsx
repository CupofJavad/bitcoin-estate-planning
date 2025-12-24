'use client'

import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    return (
      <button
        className={cn(
          'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          {
            // Primary: Bitcoin orange (inspired by Bitcoin design system)
            'bg-bitcoin-orange text-white hover:bg-bitcoin-orange-dark focus:ring-bitcoin-orange': variant === 'default',
            // Destructive: Red for delete actions
            'bg-error text-white hover:bg-error-dark focus:ring-error': variant === 'destructive',
            // Outline: Border with hover effect
            'border-2 border-gray-300 bg-white hover:bg-gray-50 hover:border-bitcoin-orange focus:ring-bitcoin-orange': variant === 'outline',
            // Ghost: Minimal styling
            'hover:bg-gray-100 focus:ring-gray-300': variant === 'ghost',
            // Link: Text link style
            'text-bitcoin-orange underline-offset-4 hover:underline hover:text-bitcoin-orange-dark': variant === 'link',
            // Sizes
            'h-10 px-4 py-2': size === 'default',
            'h-9 rounded-md px-3 text-sm': size === 'sm',
            'h-11 rounded-md px-8 text-base': size === 'lg',
            'h-10 w-10': size === 'icon',
          },
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'

export { Button }

