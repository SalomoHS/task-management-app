// Test setup file for Vitest
import { vi } from 'vitest'

// Mock environment variables for tests
vi.mock('import.meta.env', () => ({
  VITE_API_BASE_URL: 'http://localhost:5000'
}))

// Global test utilities can be added here