/**
 * Authentication test helpers for Playwright E2E tests
 * Provides reusable functions for common auth operations
 */

import { Page } from '@playwright/test';

export interface TestUser {
  email: string;
  password: string;
  full_name: string;
}

/**
 * Generate a unique test user with timestamp-based email
 */
export function generateTestUser(prefix = 'test'): TestUser {
  const timestamp = Date.now();
  return {
    email: `${prefix}-${timestamp}@example.com`,
    password: 'TestPassword123!',
    full_name: `Test User ${timestamp}`,
  };
}

/**
 * Register a new user via the UI
 */
export async function registerUser(page: Page, user: TestUser): Promise<void> {
  await page.goto('/register');
  await page.fill('input[type="email"]', user.email);
  await page.fill('input[type="password"]', user.password);
  await page.fill('input[id="full_name"]', user.full_name);
  await page.click('button[type="submit"]');
  await page.waitForURL(/.*\/login/, { timeout: 10000 });
}

/**
 * Login a user via the UI
 */
export async function loginUser(page: Page, user: TestUser): Promise<void> {
  await page.goto('/login');
  await page.fill('input[type="email"]', user.email);
  await page.fill('input[type="password"]', user.password);
  await page.click('button[type="submit"]');
  await page.waitForURL(/.*\/$/, { timeout: 15000 });
  
  // Verify login was successful by checking for logout button
  const logoutButton = page.locator('text=/sign out|logout/i').first();
  await logoutButton.waitFor({ state: 'visible', timeout: 10000 });
}

/**
 * Register and login a user in one step
 */
export async function registerAndLogin(page: Page, user?: TestUser): Promise<TestUser> {
  const testUser = user || generateTestUser();
  await registerUser(page, testUser);
  await loginUser(page, testUser);
  return testUser;
}

/**
 * Logout the current user
 */
export async function logoutUser(page: Page): Promise<void> {
  const logoutButton = page.locator('text=/sign out|logout/i').first();
  if (await logoutButton.isVisible().catch(() => false)) {
    await logoutButton.click();
    await page.waitForURL(/.*\/login/, { timeout: 10000 });
  }
}

/**
 * Clear all authentication state (cookies, storage)
 */
export async function clearAuthState(page: Page): Promise<void> {
  await page.context().clearCookies();
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
}

/**
 * Check if user is currently logged in
 */
export async function isLoggedIn(page: Page): Promise<boolean> {
  const logoutButton = page.locator('text=/sign out|logout/i').first();
  return await logoutButton.isVisible().catch(() => false);
}

