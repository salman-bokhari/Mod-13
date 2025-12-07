import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:8000';

test('Add, Browse, Edit, Delete calculation', async ({ page }) => {
  const headers = { 'Content-Type': 'application/json' };

  // 1. Register test user (idempotent)
  await page.request.post(`${baseURL}/register`, {
    data: JSON.stringify({ email: 'testuser@example.com', password: 'testpass' }),
    headers
  }).catch(() => {}); // Ignore error if user already exists

  // 2. Login to get JWT token
  const loginRes = await page.request.post(`${baseURL}/login`, {
    data: JSON.stringify({ email: 'testuser@example.com', password: 'testpass' }),
    headers
  });
  expect(loginRes.ok()).toBeTruthy();
  const loginData = await loginRes.json();
  const token = loginData.access_token;
  const authHeaders = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };

  // Add calculation
  let res = await page.request.post(`${baseURL}/calculations`, {
    data: JSON.stringify({ operand1: 2, operand2: 3, operation: 'add' }),
    headers: authHeaders
  });
  expect(res.ok()).toBeTruthy();
  const calc = await res.json();
  expect(calc.result).toBe(5);

  // Browse calculations
  res = await page.request.get(`${baseURL}/calculations`, { headers: authHeaders });
  const list = await res.json();
  expect(list.length).toBeGreaterThan(0);

  // Edit calculation
  res = await page.request.put(`${baseURL}/calculations/${calc.id}`, {
    data: JSON.stringify({ operand2: 4 }),
    headers: authHeaders
  });
  const updated = await res.json();
  expect(updated.result).toBe(6);

  // Delete calculation
  res = await page.request.delete(`${baseURL}/calculations/${calc.id}`, { headers: authHeaders });
  expect(res.ok()).toBeTruthy();
});
