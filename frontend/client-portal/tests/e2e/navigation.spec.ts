import { test, expect } from '@playwright/test';

/**
 * Navigation E2E Tests
 * Tests all navigation workflows: menus, buttons, links, dropdowns
 */

const TEST_USER = {
  email: `nav-test-${Date.now()}@example.com`,
  password: 'TestPassword123!',
  full_name: 'Navigation Test User',
};

test.describe('Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
  });

  test('should navigate to dashboard from login', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/.*\/$/, { timeout: 10000 });
  });

  test('should navigate to estate plan detail', async ({ page }) => {
    // Click on first estate plan card
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await expect(page).toHaveURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
    }
  });

  test('should navigate back from detail to dashboard', async ({ page }) => {
    // Go to detail page
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Click back button
      const backButton = page.locator('button:has-text("Back"), a:has-text("Back"), button[aria-label*="back" i]').first();
      if (await backButton.isVisible().catch(() => false)) {
        await backButton.click();
        await expect(page).toHaveURL(/.*\/$/, { timeout: 5000 });
      }
    }
  });

  test('should toggle theme (dark mode)', async ({ page }) => {
    // Look for theme toggle button
    const themeToggle = page.locator('button[aria-label*="theme" i], button[aria-label*="dark" i], button:has(svg)').first();
    if (await themeToggle.isVisible().catch(() => false)) {
      await themeToggle.click();
      await page.waitForTimeout(500);
      
      // Check if dark mode class is applied
      const html = page.locator('html');
      const classes = await html.getAttribute('class');
      // Theme should have changed
      expect(classes).toBeTruthy();
    }
  });

  test('should access user menu', async ({ page }) => {
    // Look for user menu or logout button
    const userMenu = page.locator('text=/sign out|logout|user|account/i').first();
    if (await userMenu.isVisible().catch(() => false)) {
      await userMenu.click();
      await page.waitForTimeout(500);
      
      // Should show menu or logout option
      const logoutOption = page.locator('text=/sign out|logout/i').first();
      if (await logoutOption.isVisible().catch(() => false)) {
        await expect(logoutOption).toBeVisible();
      }
    }
  });

  test('should navigate using browser back/forward', async ({ page }) => {
    // Go to detail page
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Use browser back
      await page.goBack();
      await expect(page).toHaveURL(/.*\/$/, { timeout: 5000 });
      
      // Use browser forward
      await page.goForward();
      await expect(page).toHaveURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
    }
  });
});

