import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:8000',
  },
  timeout: 60000, // increase timeout
});
