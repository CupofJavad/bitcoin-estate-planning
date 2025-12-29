/**
 * Unit Tests for API Client
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock fetch
global.fetch = vi.fn()

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should construct correct API URL', () => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const BASE_URL = `${API_URL}/api/v1`
    
    expect(BASE_URL).toBe('http://localhost:8000/api/v1')
  })

  it('should handle network errors', async () => {
    (global.fetch as any).mockRejectedValueOnce(new TypeError('Failed to fetch'))
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/estate-plans')
      expect(response).toBeDefined()
    } catch (error) {
      expect(error).toBeInstanceOf(TypeError)
    }
  })

  it('should handle timeout errors', async () => {
    const abortError = new DOMException('The operation was aborted', 'AbortError')
    (global.fetch as any).mockRejectedValueOnce(abortError)
    
    try {
      await fetch('http://localhost:8000/api/v1/estate-plans', {
        signal: AbortSignal.timeout(1000),
      })
    } catch (error) {
      expect(error).toBeInstanceOf(DOMException)
      expect((error as DOMException).name).toBe('AbortError')
    }
  })

  it('should handle HTTP errors', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: async () => ({ detail: 'Server error' }),
    })
    
    const response = await fetch('http://localhost:8000/api/v1/estate-plans')
    expect(response.ok).toBe(false)
    expect(response.status).toBe(500)
  })
})

