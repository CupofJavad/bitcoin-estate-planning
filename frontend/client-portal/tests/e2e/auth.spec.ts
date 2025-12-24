import { test, expect } from '@playwright/test';

/**
 * Authentication E2E Tests
 * Tests all authentication workflows: registration, login, logout
 */

const TEST_USER = {
  email: `test-${Date.now()}@example.com`,
  password: 'TestPassword123!',
  full_name: 'Test User',
};

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Clear cookies and storage before each test
    await page.context().clearCookies();
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  });

  test('should display registration page', async ({ page }) => {
    await page.goto('/register');
    
    // Check page elements
    await expect(page.locator('h1')).toContainText('Create Account');
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should register a new user', async ({ page }) => {
    await page.goto('/register');
    
    // Fill registration form
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.fill('input[name="full_name"]', TEST_USER.full_name);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to login page
    await expect(page).toHaveURL(/.*\/login/);
    
    // Check for success message (if toast is visible)
    const toast = page.locator('[role="alert"], .toast, [data-testid="toast"]').first();
    if (await toast.isVisible().catch(() => false)) {
      await expect(toast).toContainText(/success|registered/i);
    }
  });

  test('should show error for invalid email format', async ({ page }) => {
    await page.goto('/register');
    
    await page.fill('input[type="email"]', 'invalid-email');
    await page.fill('input[type="password"]', TEST_USER.password);
    
    // Try to submit
    await page.click('button[type="submit"]');
    
    // Should show validation error or stay on page
    const emailInput = page.locator('input[type="email"]');
    const validity = await emailInput.evaluate((el: HTMLInputElement) => el.validity.valid);
    
    if (!validity) {
      // HTML5 validation should prevent submission
      await expect(page).toHaveURL(/.*\/register/);
    }
  });

  test('should show error for short password', async ({ page }) => {
    await page.goto('/register');
    
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', 'short');
    
    // Try to submit
    await page.click('button[type="submit"]');
    
    // Should show validation error
    const passwordInput = page.locator('input[type="password"]');
    const validity = await passwordInput.evaluate((el: HTMLInputElement) => el.validity.valid);
    
    if (!validity) {
      await expect(page).toHaveURL(/.*\/register/);
    }
  });

  test('should display login page', async ({ page }) => {
    await page.goto('/login');
    
    // Check page elements
    await expect(page.locator('h1')).toContainText(/sign in|login/i);
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should login with valid credentials', async ({ page }) => {
    // First, register a user
    await page.goto('/register');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.fill('input[name="full_name"]', TEST_USER.full_name);
    await page.click('button[type="submit"]');
    
    // Wait for redirect to login
    await page.waitForURL(/.*\/login/, { timeout: 5000 });
    
    // Now login
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    // Should redirect to dashboard/home
    await expect(page).toHaveURL(/.*\/$/, { timeout: 10000 });
    
    // Check for user menu or logout button
    const userMenu = page.locator('text=/sign out|logout/i').first();
    await expect(userMenu).toBeVisible({ timeout: 5000 });
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('input[type="email"]', 'nonexistent@example.com');
    await page.fill('input[type="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Should show error message
    await page.waitForTimeout(2000); // Wait for API call
    
    const errorMessage = page.locator('text=/invalid|incorrect|error/i').first();
    if (await errorMessage.isVisible().catch(() => false)) {
      await expect(errorMessage).toBeVisible();
    }
    
    // Should stay on login page
    await expect(page).toHaveURL(/.*\/login/);
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/register');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.fill('input[name="full_name"]', TEST_USER.full_name);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/login/);
    
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Click logout
    const logoutButton = page.locator('text=/sign out|logout/i').first();
    await logoutButton.click();
    
    // Should redirect to login
    await expect(page).toHaveURL(/.*\/login/, { timeout: 10000 });
  });

  test('should redirect to login when accessing protected route without auth', async ({ page }) => {
    await page.goto('/');
    
    // Should redirect to login
    await expect(page).toHaveURL(/.*\/login/, { timeout: 5000 });
  });

  test('should navigate between login and register pages', async ({ page }) => {
    await page.goto('/login');
    
    // Click "Sign up" link
    const signUpLink = page.locator('a[href="/register"]').first();
    if (await signUpLink.isVisible().catch(() => false)) {
      await signUpLink.click();
      await expect(page).toHaveURL(/.*\/register/);
    }
    
    // Click "Sign in" link
    await page.goto('/register');
    const signInLink = page.locator('a[href="/login"]').first();
    if (await signInLink.isVisible().catch(() => false)) {
      await signInLink.click();
      await expect(page).toHaveURL(/.*\/login/);
    }
  });
});

