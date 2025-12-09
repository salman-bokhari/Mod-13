import { test, expect } from '@playwright/test';
const timestamp = Date.now();
const testUser = { email: `test${timestamp}@example.com`, password: 'Password123' };
const shortPassUser = { email: `short${timestamp}@example.com`, password: '123' };
const baseURL = process.env.BASE_URL || 'http://localhost:8000';

test('Register with short password shows error', async ({ page }) => {
  await page.goto(`${baseURL}/register.html`);
  await page.fill('input[name="email"]', shortPassUser.email);
  await page.fill('input[name="password"]', shortPassUser.password);
  await page.click('button[type="submit"]');
  await expect(page.locator('#error-message')).toHaveText(/error during registration/i, { timeout: 20000 });
});

test('Login with wrong password shows error', async ({ page }) => {
  await page.goto(`${baseURL}/login.html`);
  await page.fill('input[name="email"]', testUser.email);
  await page.fill('input[name="password"]', 'wrongpass');
  await page.click('button[type="submit"]');
  await expect(page.locator('#error-message')).toHaveText(/invalid credentials/i, { timeout: 20000 });
});
