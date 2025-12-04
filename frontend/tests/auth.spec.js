import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:8000';

test.describe('JWT Auth E2E Tests', () => {
  const testUser = { email: 'testuser@example.com', password: 'Password123' };

  test('Register user successfully', async ({ page }) => {
    await page.goto(`${BASE_URL}/register.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    await expect(page.locator('#success-message')).toHaveText(/registration successful/i, { timeout: 20000 });
  });

  test('Login with correct credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    await expect(page.locator('#login-success')).toHaveText(/login successful/i, { timeout: 20000 });
  });

  test('Register with short password shows error', async ({ page }) => {
    await page.goto(`${BASE_URL}/register.html`);
    await page.fill('input[name="email"]', 'shortpass@example.com');
    await page.fill('input[name="password"]', '123');
    await page.click('button[type="submit"]');

    await expect(page.locator('#error-message')).toHaveText(/error during registration/i, { timeout: 20000 });
  });

  test('Login with wrong password shows error', async ({ page }) => {
    await page.goto(`${BASE_URL}/login.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('#error-message')).toHaveText(/invalid credentials/i, { timeout: 20000 });
  });
});
