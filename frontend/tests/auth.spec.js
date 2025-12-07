import { test, expect } from '@playwright/test';

test.describe('JWT Auth E2E Tests', () => {
  const timestamp = Date.now();
  const testUser = { email: `testuser+${timestamp}@example.com`, password: 'Password123' };
  const shortPassUser = { email: `shortpass+${timestamp}@example.com`, password: '123' };

  test('Register user successfully', async ({ page }) => {
    await page.goto('/register.html');
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    await expect(page.locator('#success-message')).toHaveText(/registration successful/i, { timeout: 20000 });
  });

  test('Login with correct credentials', async ({ page }) => {
    // Register user first
    await page.goto('/register.html');
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('#success-message')).toHaveText(/registration successful/i, { timeout: 20000 });

    // Login
    await page.goto('/login.html');
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    await expect(page.locator('#login-success')).toHaveText(/login successful/i, { timeout: 20000 });
  });

  test('Register with short password shows error', async ({ page }) => {
    await page.goto('/register.html');
    await page.fill('input[name="email"]', shortPassUser.email);
    await page.fill('input[name="password"]', shortPassUser.password);
    await page.click('button[type="submit"]');

    await expect(page.locator('#error-message')).toHaveText(/error during registration/i, { timeout: 20000 });
  });

  test('Login with wrong password shows error', async ({ page }) => {
    // Register user first
    await page.goto('/register.html');
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('#success-message')).toHaveText(/registration successful/i, { timeout: 20000 });

    // Login with wrong password
    await page.goto('/login.html');
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('#error-message')).toHaveText(/invalid credentials/i, { timeout: 20000 });
  });
});
