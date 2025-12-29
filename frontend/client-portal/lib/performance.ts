/**
 * Performance monitoring and optimization utilities
 * Based on Front-End Performance Checklist best practices
 */

// Performance metrics tracking
export interface PerformanceMetrics {
  pageLoadTime: number
  timeToFirstByte: number
  firstContentfulPaint: number
  largestContentfulPaint: number
  cumulativeLayoutShift: number
}

export function trackPerformanceMetrics(): PerformanceMetrics | null {
  if (typeof window === 'undefined' || !window.performance) {
    return null
  }

  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
  if (!navigation) return null

  const paint = performance.getEntriesByType('paint')
  const fcp = paint.find((entry) => entry.name === 'first-contentful-paint')
  const lcp = performance.getEntriesByType('largest-contentful-paint')[0] as PerformanceEntry & { renderTime?: number }

  return {
    pageLoadTime: navigation.loadEventEnd - navigation.fetchStart,
    timeToFirstByte: navigation.responseStart - navigation.requestStart,
    firstContentfulPaint: fcp ? fcp.startTime : 0,
    largestContentfulPaint: lcp?.renderTime || 0,
    cumulativeLayoutShift: 0, // Would need to use web-vitals library for accurate CLS
  }
}

// Lazy load images
export function lazyLoadImages() {
  if (typeof window === 'undefined') return

  const images = document.querySelectorAll('img[data-src]')
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target as HTMLImageElement
        img.src = img.dataset.src || ''
        img.removeAttribute('data-src')
        imageObserver.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))
}

// Debounce utility
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null
      func(...args)
    }

    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Throttle utility
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// Preload critical resources
export function preloadResource(href: string, as: string) {
  if (typeof document === 'undefined') return

  const link = document.createElement('link')
  link.rel = 'preload'
  link.href = href
  link.as = as
  document.head.appendChild(link)
}

// Prefetch resources
export function prefetchResource(href: string) {
  if (typeof document === 'undefined') return

  const link = document.createElement('link')
  link.rel = 'prefetch'
  link.href = href
  document.head.appendChild(link)
}

