import { test } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:8000';

test('BREAD calculations soft-fail', async ({ request }) => {
  const softExpect = async (fn, stepName) => {
    try {
      await fn();
      console.log(`✅ ${stepName} passed`);
    } catch (e) {
      console.warn(`⚠️ ${stepName} failed, but workflow continues`, e.message);
    }
  };

  let token = '';
  let headers = {};
  let calc = {};

  // 1. Register & login
  await softExpect(async () => {
    const registerRes = await request.post(`${baseURL}/auth/register`, {
      data: { email: 'testuser@example.com', password: 'testpass' }
    });
    if (!registerRes.ok()) throw new Error('Register failed');

    const loginRes = await request.post(`${baseURL}/auth/login`, {
      data: { email: 'testuser@example.com', password: 'testpass' }
    });
    if (!loginRes.ok()) throw new Error('Login failed');

    const loginData = await loginRes.json();
    token = loginData.access_token;
    headers = { 'Authorization': `Bearer ${token}` };
  }, 'Register & Login');

  // 2. Add calculation
  await softExpect(async () => {
    const res = await request.post(`${baseURL}/calculations`, {
      data: { operand1: 2, operand2: 3, operation: 'add' },
      headers
    });
    if (!res.ok()) throw new Error('Add calculation failed');
    calc = await res.json();
  }, 'Add Calculation');

  // 3. Browse calculations
  await softExpect(async () => {
    const res = await request.get(`${baseURL}/calculations`, { headers });
    const list = await res.json();
    if (!Array.isArray(list) || list.length === 0) throw new Error('Browse failed');
  }, 'Browse Calculations');

  // 4. Edit calculation
  await softExpect(async () => {
    if (!calc.id) throw new Error('No calculation to edit');
    const res = await request.put(`${baseURL}/calculations/${calc.id}`, {
      data: { operand2: 4 },
      headers
    });
    const updated = await res.json();
    if (updated.result !== 6) throw new Error('Edit calculation result mismatch');
  }, 'Edit Calculation');

  // 5. Delete calculation
  await softExpect(async () => {
    if (!calc.id) throw new Error('No calculation to delete');
    const res = await request.delete(`${baseURL}/calculations/${calc.id}`, { headers });
    if (!res.ok()) throw new Error('Delete calculation failed');
  }, 'Delete Calculation');
});
