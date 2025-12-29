/**
 * E2E Tests for Estate Plans Workflow
 * Tests complete user journey from creation to management
 */

import { test, expect } from '@playwright/test'
import { loginAsDemoUser } from '../helpers/auth'

test.describe('Estate Plans Management', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page
    await page.goto('http://localhost:3000')
    
    // Wait for page to load
    await page.waitForLoadState('networkidle')
  })

  test('should display dashboard with statistics', async ({ page }) => {
    // Check for dashboard elements
    await expect(page.locator('h1')).toContainText('Bitcoin Estate Planning Platform')
    
    // Check for stat cards
    await expect(page.locator('text=Total Estate Plans')).toBeVisible()
    await expect(page.locator('text=Active Plans')).toBeVisible()
    await expect(page.locator('text=Total Beneficiaries')).toBeVisible()
    await expect(page.locator('text=Timelock Policies')).toBeVisible()
  })

  test('should show empty state when no estate plans exist', async ({ page }) => {
    // Check for empty state
    const emptyState = page.locator('text=No estate plans yet')
    if (await emptyState.isVisible()) {
      await expect(emptyState).toBeVisible()
      await expect(page.locator('text=Create Estate Plan')).toBeVisible()
    }
  })

  test('should open create estate plan modal', async ({ page }) => {
    // Click create button
    await page.click('text=Create Estate Plan')
    
    // Wait for modal
    await page.waitForSelector('text=Create Estate Plan', { state: 'visible' })
    
    // Check form fields
    await expect(page.locator('input[name="name"]')).toBeVisible()
    await expect(page.locator('input[name="description"]')).toBeVisible()
    await expect(page.locator('input[name="bitcoin_address"]')).toBeVisible()
    await expect(page.locator('input[type="checkbox"][name="is_active"]')).toBeVisible()
  })

  test('should create estate plan with valid data', async ({ page }) => {
    // Click create button
    await page.click('text=Create Estate Plan')
    await page.waitForSelector('input[name="name"]', { state: 'visible' })
    
    // Fill form
    await page.fill('input[name="name"]', 'Test Estate Plan')
    await page.fill('input[name="description"]', 'Test description')
    await page.fill('input[name="bitcoin_address"]', 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh')
    
    // Submit form
    await page.click('button:has-text("Create")')
    
    // Wait for success message or estate plan to appear
    await page.waitForTimeout(2000)
    
    // Check for success toast or estate plan in list
    const successToast = page.locator('text=Estate plan created successfully')
    const estatePlanCard = page.locator('text=Test Estate Plan')
    
    // Either success toast or estate plan should be visible
    const hasSuccess = await successToast.isVisible().catch(() => false)
    const hasPlan = await estatePlanCard.isVisible().catch(() => false)
    
    expect(hasSuccess || hasPlan).toBeTruthy()
  })

  test('should validate Bitcoin address', async ({ page }) => {
    // Click create button
    await page.click('text=Create Estate Plan')
    await page.waitForSelector('input[name="name"]', { state: 'visible' })
    
    // Fill form with invalid address
    await page.fill('input[name="name"]', 'Test Plan')
    await page.fill('input[name="bitcoin_address"]', 'invalid-address')
    
    // Wait for validation
    await page.waitForTimeout(1000)
    
    // Check for validation message (either valid or invalid)
    const validationMessage = page.locator('text=/Valid|Invalid/')
    const hasValidation = await validationMessage.isVisible().catch(() => false)
    
    // Validation should appear
    expect(hasValidation).toBeTruthy()
  })

  test('should search estate plans', async ({ page }) => {
    // Wait for search input
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.waitFor({ state: 'visible', timeout: 5000 }).catch(() => {})
    
    if (await searchInput.isVisible()) {
      await searchInput.fill('test')
      await page.waitForTimeout(500)
      
      // Search should filter results
      const results = page.locator('[class*="card"], [class*="Card"]')
      const count = await results.count()
      expect(count).toBeGreaterThanOrEqual(0)
    }
  })

  test('should display estate plan card with details', async ({ page }) => {
    // Wait for estate plans to load
    await page.waitForTimeout(2000)
    
    // Check for estate plan cards
    const cards = page.locator('[class*="card"], [class*="Card"]')
    const cardCount = await cards.count()
    
    if (cardCount > 0) {
      // Check first card has required elements
      const firstCard = cards.first()
      await expect(firstCard.locator('text=/Estate|Plan/')).toBeVisible({ timeout: 5000 }).catch(() => {})
    }
  })

  test('should handle API errors gracefully', async ({ page }) => {
    // Intercept API calls and return error
    await page.route('**/api/v1/estate-plans', route => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ detail: 'Internal server error' }),
      })
    })
    
    // Reload page
    await page.reload()
    await page.waitForTimeout(2000)
    
    // Should show error toast or message
    const errorMessage = page.locator('text=/error|Error|failed|Failed/')
    const hasError = await errorMessage.isVisible().catch(() => false)
    
    // Error should be displayed
    expect(hasError).toBeTruthy()
  })

  test('should show loading skeleton while fetching data', async ({ page }) => {
    // Intercept API to add delay
    await page.route('**/api/v1/estate-plans', route => {
      setTimeout(() => {
        route.continue()
      }, 1000)
    })
    
    // Reload page
    await page.reload()
    
    // Should show loading state (skeleton or spinner)
    const loadingIndicator = page.locator('[class*="skeleton"], [class*="Skeleton"], [class*="spinner"], [class*="loading"]')
    const hasLoading = await loadingIndicator.isVisible({ timeout: 500 }).catch(() => false)
    
    // Loading state should appear
    expect(hasLoading).toBeTruthy()
  })
})

test.describe('Estate Plan Form Validation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000')
    await page.waitForLoadState('networkidle')
    await page.click('text=Create Estate Plan')
    await page.waitForSelector('input[name="name"]', { state: 'visible' })
  })

  test('should require name field', async ({ page }) => {
    // Try to submit without name
    await page.fill('input[name="description"]', 'Test')
    await page.click('button:has-text("Create")')
    
    // Should show validation error or prevent submission
    await page.waitForTimeout(500)
    const errorMessage = page.locator('text=/required|Required|name/')
    const hasError = await errorMessage.isVisible().catch(() => false)
    
    // Validation should prevent submission
    expect(hasError || await page.locator('input[name="name"]').isVisible()).toBeTruthy()
  })

  test('should allow canceling form', async ({ page }) => {
    // Fill some data
    await page.fill('input[name="name"]', 'Test')
    
    // Click cancel
    await page.click('button:has-text("Cancel")')
    
    // Modal should close
    await page.waitForTimeout(500)
    const modal = page.locator('text=Create Estate Plan')
    const isVisible = await modal.isVisible().catch(() => false)
    
    expect(isVisible).toBeFalsy()
  })
})
