/**
 * Complete User Workflow Tests
 * Tests end-to-end user journeys
 */

import { test, expect } from '@playwright/test'

test.describe('Complete User Workflows', () => {
  test('User Journey: Create and Manage Estate Plan', async ({ page }) => {
    // Step 1: Navigate to dashboard
    await page.goto('http://localhost:3000')
    await page.waitForLoadState('networkidle')
    
    // Step 2: Verify dashboard loads
    await expect(page.locator('h1')).toContainText('Bitcoin Estate Planning Platform', { timeout: 10000 })
    
    // Step 3: Click create estate plan
    const createButton = page.locator('text=Create Estate Plan').first()
    await createButton.waitFor({ state: 'visible', timeout: 10000 })
    await createButton.click()
    
    // Step 4: Fill estate plan form
    await page.waitForSelector('input[name="name"]', { state: 'visible', timeout: 5000 })
    await page.fill('input[name="name"]', 'My Bitcoin Estate Plan')
    await page.fill('input[name="description"]', 'Test estate plan for Bitcoin inheritance')
    await page.fill('input[name="bitcoin_address"]', 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh')
    
    // Step 5: Wait for address validation
    await page.waitForTimeout(2000)
    
    // Step 6: Submit form
    const submitButton = page.locator('button:has-text("Create")')
    await submitButton.click()
    
    // Step 7: Wait for response
    await page.waitForTimeout(3000)
    
    // Step 8: Verify success (either toast or estate plan appears)
    const successIndicators = [
      page.locator('text=created successfully'),
      page.locator('text=My Bitcoin Estate Plan'),
      page.locator('[class*="toast"]'),
    ]
    
    let foundSuccess = false
    for (const indicator of successIndicators) {
      try {
        if (await indicator.isVisible({ timeout: 2000 })) {
          foundSuccess = true
          break
        }
      } catch {}
    }
    
    // Should show some form of success
    expect(foundSuccess).toBeTruthy()
  })

  test('User Journey: View Estate Plans List', async ({ page }) => {
    await page.goto('http://localhost:3000')
    await page.waitForLoadState('networkidle')
    
    // Wait for estate plans to load
    await page.waitForTimeout(3000)
    
    // Check for estate plans section
    const estatePlansSection = page.locator('text=Estate Plans')
    await expect(estatePlansSection).toBeVisible({ timeout: 10000 })
    
    // Check for search functionality
    const searchInput = page.locator('input[placeholder*="Search"]')
    const hasSearch = await searchInput.isVisible().catch(() => false)
    
    if (hasSearch) {
      await searchInput.fill('test')
      await page.waitForTimeout(1000)
    }
  })

  test('User Journey: Error Handling', async ({ page }) => {
    // Intercept API to simulate error
    await page.route('**/api/v1/estate-plans', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal server error' }),
      })
    })
    
    await page.goto('http://localhost:3000')
    await page.waitForTimeout(3000)
    
    // Should show error message
    const errorIndicators = [
      page.locator('text=/error|Error|failed|Failed/'),
      page.locator('[class*="toast"]'),
      page.locator('[class*="error"]'),
    ]
    
    let foundError = false
    for (const indicator of errorIndicators) {
      try {
        if (await indicator.isVisible({ timeout: 2000 })) {
          foundError = true
          break
        }
      } catch {}
    }
    
    // Error should be displayed
    expect(foundError).toBeTruthy()
  })

  test('User Journey: Loading States', async ({ page }) => {
    // Add delay to API response
    await page.route('**/api/v1/estate-plans', route => {
      setTimeout(() => route.continue(), 2000)
    })
    
    await page.goto('http://localhost:3000')
    
    // Should show loading state
    const loadingIndicators = [
      page.locator('[class*="skeleton"]'),
      page.locator('[class*="Skeleton"]'),
      page.locator('[class*="spinner"]'),
      page.locator('[class*="loading"]'),
      page.locator('text=Loading'),
    ]
    
    let foundLoading = false
    for (const indicator of loadingIndicators) {
      try {
        if (await indicator.isVisible({ timeout: 1000 })) {
          foundLoading = true
          break
        }
      } catch {}
    }
    
    // Loading state should appear
    expect(foundLoading).toBeTruthy()
  })
})

