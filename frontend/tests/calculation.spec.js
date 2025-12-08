import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:8000';

test('BREAD calculations', async ({ request }) => {
  // 1. Register & login via API
  const registerRes = await request.post(`${baseURL}/auth/register`, {
    data: { email: 'testuser@example.com', password: 'testpass' }
  });
  expect(registerRes.ok()).toBeTruthy();

  const loginRes = await request.post(`${baseURL}/auth/login`, {
    data: { email: 'testuser@example.com', password: 'testpass' }
  });
  expect(loginRes.ok()).toBeTruthy();

  const loginData = await loginRes.json();
  const token = loginData.access_token;
  const headers = { 'Authorization': `Bearer ${token}` };

  // 2. Add calculation
  let res = await request.post(`${baseURL}/calculations`, {
    data: { operand1: 2, operand2: 3, operation: 'add' },
    headers
  });
  expect(res.ok()).toBeTruthy();
  const calc = await res.json();
  expect(calc.result).toBe(5);

  // 3. Browse calculations
  res = await request.get(`${baseURL}/calculations`, { headers });
  const list = await res.json();
  expect(list.length).toBeGreaterThan(0);

  // 4. Edit calculation
  res = await request.put(`${baseURL}/calculations/${calc.id}`, {
    data: { operand2: 4 },
    headers
  });
  const updated = await res.json();
  expect(updated.result).toBe(6);

  // 5. Delete calculation
  res = await request.delete(`${baseURL}/calculations/${calc.id}`, { headers });
  expect(res.ok()).toBeTruthy();
});
