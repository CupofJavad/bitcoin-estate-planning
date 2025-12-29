'use client'

import { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { LucideIcon } from 'lucide-react'
import { AnimatedCounter } from './animated-counter'

interface StatCardProps {
  title: string
  value: string | number
  icon?: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
  description?: string
  className?: string
  animate?: boolean
}

export function StatCard({ 
  title, 
  value, 
  icon: Icon,
  trend,
  description,
  className,
  animate = true
}: StatCardProps) {
  const numericValue = typeof value === 'number' ? value : parseFloat(String(value)) || 0
  
  return (
    <div className={cn(
      'bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 shadow-sm hover:shadow-md transition-all duration-200 transform hover:scale-[1.02]',
      className
    )}>
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
        {Icon && (
          <Icon className="h-5 w-5 text-gray-400 dark:text-gray-500" />
        )}
      </div>
      <div className="flex items-baseline justify-between">
        {animate && typeof value === 'number' ? (
          <AnimatedCounter 
            value={numericValue} 
            className="text-2xl font-bold text-gray-900 dark:text-gray-100"
          />
        ) : (
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{value}</p>
        )}
        {trend && (
          <span className={cn(
            'text-sm font-medium',
            trend.isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
          )}>
            {trend.isPositive ? '+' : ''}{trend.value}%
          </span>
        )}
      </div>
      {description && (
        <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">{description}</p>
      )}
    </div>
  )
}

