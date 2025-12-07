import { test, expect } from '@playwright/test';

test.describe('JWT Auth E2E Tests', () => {
  const timestamp = Date.now();
  const testUser = { email: `testuser+${timestamp}@example.com`, password: 'Password123' };
  const shortPassUser = { email: `shortpass+${timestamp}@example.com`, password: '123' };

  const baseURL = '/'; // relative paths work with Playwright baseURL

  test('Register user successfully', async ({ page }) => {
    await page.goto(`${baseURL}register.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    // Wait for backend response to update DOM
    await page.waitForResponse(r => r.url().endsWith('/register') && r.status() === 201);
    await expect(page.locator('#success-message')).toHaveText(/registration successful/i, { timeout: 20000 });
  });

  test('Login with correct credentials', async ({ page }) => {
    await page.goto(`${baseURL}register.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForResponse(r => r.url().endsWith('/register') && r.status() === 201);

    await page.goto(`${baseURL}login.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForResponse(r => r.url().endsWith('/login') && r.status() === 200);

    await expect(page.locator('#login-success')).toHaveText(/login successful/i, { timeout: 20000 });
  });

  test('Register with short password shows error', async ({ page }) => {
    await page.goto(`${baseURL}register.html`);
    await page.fill('input[name="email"]', shortPassUser.email);
    await page.fill('input[name="password"]', shortPassUser.password);
    await page.click('button[type="submit"]');
    await page.waitForResponse(r => r.url().endsWith('/register') && r.status() === 400);

    await expect(page.locator('#error-message')).toHaveText(/error during registration/i, { timeout: 20000 });
  });

  test('Login with wrong password shows error', async ({ page }) => {
    await page.goto(`${baseURL}register.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForResponse(r => r.url().endsWith('/register') && r.status() === 201);

    await page.goto(`${baseURL}login.html`);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');
    await page.waitForResponse(r => r.url().endsWith('/login') && r.status() === 401);

    await expect(page.locator('#error-message')).toHaveText(/invalid credentials/i, { timeout: 20000 });
  });
});
