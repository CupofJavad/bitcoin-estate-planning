/**
 * Authentication helpers for E2E tests
 */

import { Page } from '@playwright/test'

export async function loginAsDemoUser(page: Page) {
  // Navigate to login page
  await page.goto('/login')
  await page.waitForLoadState('networkidle')
  
  // Wait for login form to be visible
  await page.waitForSelector('input[type="email"]', { timeout: 5000 })
  
  // Fill login form
  await page.fill('input[type="email"]', 'demo@example.com')
  await page.fill('input[type="password"]', 'demo123')
  
  // Submit form
  await page.click('button[type="submit"]')
  
  // Wait for either redirect to dashboard or stay on login (if auth fails)
  try {
    await page.waitForURL('/', { timeout: 10000 })
  } catch {
    // If still on login, check for error message
    const errorVisible = await page.locator('text=/error|invalid|failed/i').isVisible({ timeout: 2000 }).catch(() => false)
    if (errorVisible) {
      console.log('Login failed - error message visible')
    }
  }
  await page.waitForLoadState('networkidle')
}

export async function ensureAuthenticated(page: Page) {
  // Check if we're on login page
  const currentUrl = page.url()
  if (currentUrl.includes('/login')) {
    await loginAsDemoUser(page)
  } else {
    // Check if we're already authenticated by looking for user menu
    const userMenu = page.locator('text=/sign out|logout|demo@example.com/i')
    const isVisible = await userMenu.isVisible({ timeout: 2000 }).catch(() => false)
    if (!isVisible) {
      await loginAsDemoUser(page)
    }
  }
}
