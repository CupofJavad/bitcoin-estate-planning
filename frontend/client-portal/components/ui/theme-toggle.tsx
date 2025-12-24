'use client'

import { Moon, Sun, Monitor } from 'lucide-react'
import { useTheme } from '@/contexts/theme-context'
import { Button } from './button'
import { cn } from '@/lib/utils'

export function ThemeToggle() {
  const { theme, resolvedTheme, toggleTheme } = useTheme()

  const getIcon = () => {
    if (theme === 'system') {
      return <Monitor className="h-4 w-4" />
    }
    return resolvedTheme === 'dark' ? (
      <Moon className="h-4 w-4" />
    ) : (
      <Sun className="h-4 w-4" />
    )
  }

  const getLabel = () => {
    if (theme === 'system') return 'System'
    return resolvedTheme === 'dark' ? 'Dark' : 'Light'
  }

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className={cn(
        'relative',
        'hover:bg-gray-100 dark:hover:bg-gray-800'
      )}
      aria-label={`Toggle theme (current: ${getLabel()})`}
    >
      {getIcon()}
    </Button>
  )
}

