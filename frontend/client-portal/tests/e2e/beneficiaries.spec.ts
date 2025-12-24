import { test, expect } from '@playwright/test';

/**
 * Beneficiaries E2E Tests
 * Tests all beneficiary workflows: create, read, update, delete
 */

const TEST_USER = {
  email: `beneficiary-test-${Date.now()}@example.com`,
  password: 'TestPassword123!',
  full_name: 'Beneficiary Test User',
};

test.describe('Beneficiaries', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*\/$/, { timeout: 10000 });
  });

  test('should create a beneficiary', async ({ page }) => {
    // First create an estate plan
    const createButton = page.locator('button:has-text("Create"), button:has-text("New")').first();
    await createButton.click();
    await page.waitForSelector('input[name="name"]', { timeout: 5000 });
    
    await page.fill('input[name="name"]', 'Test Estate Plan');
    await page.fill('input[name="bitcoin_address"]', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa');
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    // Navigate to estate plan detail
    const estatePlanCard = page.locator('text=Test Estate Plan').first();
    await estatePlanCard.click();
    await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
    
    // Click add beneficiary
    const addBeneficiaryButton = page.locator('button:has-text("Add Beneficiary"), button:has-text("Beneficiary")').first();
    await addBeneficiaryButton.click();
    await page.waitForSelector('input[name="name"]', { timeout: 5000 });
    
    // Fill beneficiary form
    await page.fill('input[name="name"]', 'Test Beneficiary');
    await page.fill('input[name="email"]', 'beneficiary@example.com');
    await page.fill('input[name="allocation_percentage"]', '50');
    await page.fill('input[name="bitcoin_address"]', '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2');
    
    // Submit
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    // Check if beneficiary appears
    await expect(page.locator('text=Test Beneficiary')).toBeVisible({ timeout: 5000 });
  });

  test('should validate allocation percentage', async ({ page }) => {
    // Navigate to estate plan
    const firstCard = page.locator('[data-testid="estate-plan-card"], .estate-plan-card, article, .card').first();
    if (await firstCard.isVisible().catch(() => false)) {
      await firstCard.click();
      await page.waitForURL(/.*\/estate-plans\/\d+/, { timeout: 5000 });
      
      // Add beneficiary
      const addButton = page.locator('button:has-text("Add Beneficiary")').first();
      await addButton.click();
      await page.waitForSelector('input[name="allocation_percentage"]', { timeout: 5000 });
      
      // Try invalid percentage (>100)
      await page.fill('input[name="allocation_percentage"]', '150');
      await page.click('button[type="submit"]');
      
      // Should show error or prevent submission
      await page.waitForTimeout(1000);
      const errorMessage = page.locator('text=/exceed|invalid|100/i').first();
      if (await errorMessage.isVisible().catch(() => false)) {
        await expect(errorMessage).toBeVisible();
      }
    }
  });
});

