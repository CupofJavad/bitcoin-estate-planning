'use client'

import { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { LucideIcon } from 'lucide-react'

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
}

export function StatCard({ 
  title, 
  value, 
  icon: Icon,
  trend,
  description,
  className 
}: StatCardProps) {
  return (
    <div className={cn(
      'bg-white rounded-lg border border-gray-200 p-6 shadow-soft hover:shadow-medium transition-shadow',
      className
    )}>
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        {Icon && (
          <Icon className="h-5 w-5 text-gray-400" />
        )}
      </div>
      <div className="flex items-baseline justify-between">
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        {trend && (
          <span className={cn(
            'text-sm font-medium',
            trend.isPositive ? 'text-success' : 'text-error'
          )}>
            {trend.isPositive ? '+' : ''}{trend.value}%
          </span>
        )}
      </div>
      {description && (
        <p className="mt-2 text-xs text-gray-500">{description}</p>
      )}
    </div>
  )
}

