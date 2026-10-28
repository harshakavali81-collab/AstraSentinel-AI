import {defineConfig, devices} from '@playwright/test'

/** Run Chromium against the real, offline Docker Compose application. */
export default defineConfig({
  testDir: './e2e',
  timeout: 60000,
  expect: {timeout: 30000},
  workers: 1,
  retries: 0,
  reporter: [['list'], ['html', {open:'never',outputFolder:'artifacts/playwright-report'}]],
  outputDir: 'artifacts/test-results',
  use: {
    ...devices['Desktop Chrome'],
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
})
