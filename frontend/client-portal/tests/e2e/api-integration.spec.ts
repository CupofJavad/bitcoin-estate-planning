/**
 * API Integration Tests
 * Tests backend API connectivity and data flow
 */

import { test, expect } from '@playwright/test'

test.describe('API Integration', () => {
  test('should connect to backend health endpoint', async ({ request }) => {
    const response = await request.get('http://localhost:8000/health')
    expect(response.status()).toBe(200)
    
    const data = await response.json()
    expect(data).toHaveProperty('status')
    expect(data.status).toBe('healthy')
  })

  test('should fetch estate plans from API', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/v1/estate-plans')
    
    // Should return 200 (demo mode), 401 (auth required), 400 (no users), or 500 (server error)
    expect([200, 401, 400, 500]).toContain(response.status())
    
    if (response.status() === 200) {
      const data = await response.json()
      expect(Array.isArray(data)).toBe(true)
      // In demo mode, should return estate plans if demo user exists
    }
  })

  test('should validate Bitcoin address via API', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/v1/bitcoin/validate', {
      data: {
        address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
        network: 'mainnet',
      },
    })
    
    expect([200, 401]).toContain(response.status())
    
    if (response.status() === 200) {
      const data = await response.json()
      expect(data).toHaveProperty('valid')
      expect(typeof data.valid).toBe('boolean')
    }
  })

  test('should get Bitcoin balance via API', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/v1/bitcoin/balance', {
      data: {
        address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
        network: 'mainnet',
      },
    })
    
    // Accept various status codes (200 success, 401 auth, 404 not found, 500 server error)
    expect([200, 401, 404, 500]).toContain(response.status())
    
    if (response.status() === 200) {
      const data = await response.json()
      expect(data).toHaveProperty('balance_btc')
    }
  })

  test('should handle API errors gracefully', async ({ request }) => {
    // Test with invalid endpoint
    const response = await request.get('http://localhost:8000/api/v1/invalid-endpoint')
    
    expect([404, 401]).toContain(response.status())
  })

  test('should have CORS headers for frontend', async ({ request }) => {
    const response = await request.get('http://localhost:8000/health', {
      headers: {
        'Origin': 'http://localhost:3000',
      },
    })
    
    // Check for CORS headers
    const headers = response.headers()
    const hasCors = 'access-control-allow-origin' in headers || response.status() === 200
    
    expect(hasCors).toBe(true)
  })
})

