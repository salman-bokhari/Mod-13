import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:8000';

test('Add, Browse, Edit, Delete calculation', async ({ page }) => {
  // 1️⃣ Login / get token
  const loginRes = await page.request.post(`${baseURL}/login`, {
    data: { email: 'testuser@example.com', password: 'testpass' }
  });
  expect(loginRes.ok()).toBeTruthy();
  const loginData = await loginRes.json();
  const token = loginData.access_token;
  const headers = { 'Authorization': `Bearer ${token}` };

  // 2️⃣ Add
  let res = await page.request.post(`${baseURL}/calculations`, { data: { operand1: 2, operand2: 3, operation: 'add' }, headers });
  expect(res.ok()).toBeTruthy();
  const calc = await res.json();
  expect(calc.result).toBe(5);

  // 3️⃣ Browse
  res = await page.request.get(`${baseURL}/calculations`, { headers });
  const list = await res.json();
  expect(list.length).toBeGreaterThan(0);

  // 4️⃣ Edit
  res = await page.request.put(`${baseURL}/calculations/${calc.id}`, { data: { operand2: 4 }, headers });
  const updated = await res.json();
  expect(updated.result).toBe(6);

  // 5️⃣ Delete
  res = await page.request.delete(`${baseURL}/calculations/${calc.id}`, { headers });
  expect(res.ok()).toBeTruthy();
});
