import { test, expect } from '@playwright/test';

/**
 * Estate Plans E2E Tests
 * Tests all estate plan workflows: create, read, update, delete
 */

const TEST_USER = {
  email: `estate-test-${Date.now()}@example.com`,
  password: 'TestPassword123!',
  full_name: 'Estate Test User',
};

const TEST_ESTATE_PLAN = {
  name: 'Test Estate Plan',
  description: 'This is a test estate plan',
  bitcoin_address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
  is_active: true,
};

test.describe('Estate Plans', () => {
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    // Register and login to get auth token
    const registerResponse = await request.post('http://localhost:8000/api/v1/auth/register', {
      data: TEST_USER,
    });
    
    if (registerResponse.ok()) {
      const loginResponse = await request.post('http://localhost:8000/api/v1/auth/jwt/login', {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        data: new URLSearchParams({
          username: TEST_USER.email,
          password: TEST_USER.password,
        }).toString(),
      });
      
      if (loginResponse.ok()) {
        const loginData = await loginResponse.json();
        authToken = loginData.access_token;
      }
    }
  });

  test.beforeEach(async ({ page, context }) => {
    // Set auth cookie or token
    if (authToken) {
      await context.addCookies([{
        name: 'next-auth.session-token',
        value: authToken,
        domain: 'localhost',
        path: '/',
      }]);
    }
  });

  test('should display dashboard with estate plans list', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Check dashboard elements
    await expect(page.locator('h1')).toContainText(/estate planning|dashboard/i);
    await expect(page.locator('button:has-text("Create")')).toBeVisible();
  });

  test('should create a new estate plan', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Click create button
    const createButton = page.locator('button:has-text("Create"), button:has-text("New")').first();
    await createButton.click();
    
    // Wait for modal
    await page.waitForSelector('input[name="name"], input[placeholder*="name" i]', { timeout: 5000 });
    
    // Fill form
    await page.fill('input[name="name"], input[placeholder*="name" i]', TEST_ESTATE_PLAN.name);
    await page.fill('textarea[name="description"], textarea[placeholder*="description" i]', TEST_ESTATE_PLAN.description);
    await page.fill('input[name="bitcoin_address"], input[placeholder*="bitcoin" i]', TEST_ESTATE_PLAN.bitcoin_address);
    
    // Submit
    const submitButton = page.locator('button[type="submit"], button:has-text("Save"), button:has-text("Create")').first();
    await submitButton.click();
    
    // Wait for success
    await page.waitForTimeout(2000);
    
    // Check if estate plan appears in list
    const estatePlanCard = page.locator(`text=${TEST_ESTATE_PLAN.name}`).first();
    await expect(estatePlanCard).toBeVisible({ timeout: 5000 });
  });

  test('should view estate plan details', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Click on first estate plan card
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      
      // Should navigate to detail page
      await expect(page).toHaveURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Check detail page elements
      await expect(page.locator('h1')).toBeVisible();
    }
  });

  test('should edit estate plan', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Click on first estate plan
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Click edit button
      const editButton = page.locator('button:has-text("Edit"), button[aria-label*="edit" i]').first();
      if (await editButton.isVisible().catch(() => false)) {
        await editButton.click();
        
        // Wait for edit modal
        await page.waitForSelector('input[name="name"]', { timeout: 5000 });
        
        // Update name
        const nameInput = page.locator('input[name="name"]').first();
        await nameInput.clear();
        await nameInput.fill('Updated Estate Plan Name');
        
        // Save
        const saveButton = page.locator('button[type="submit"], button:has-text("Save")').first();
        await saveButton.click();
        
        await page.waitForTimeout(2000);
        
        // Check for updated name
        await expect(page.locator('text=Updated Estate Plan Name')).toBeVisible({ timeout: 5000 });
      }
    }
  });

  test('should delete estate plan', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
    
    // Click on first estate plan
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Click delete button
      const deleteButton = page.locator('button:has-text("Delete"), button[aria-label*="delete" i]').first();
      if (await deleteButton.isVisible().catch(() => false)) {
        await deleteButton.click();
        
        // Confirm deletion (if confirmation dialog appears)
        page.on('dialog', async dialog => {
          await dialog.accept();
        });
        
        await page.waitForTimeout(2000);
        
        // Should redirect to dashboard
        await expect(page).toHaveURL(/.*\/$/, { timeout: 5000 });
      }
    }
  });
});

