// Test setup file for Vitest
import { vi } from 'vitest'

// Mock environment variables for tests
vi.mock('import.meta.env', () => ({
  VITE_API_BASE_URL: 'http://localhost:5000/api',
  VITE_SUPABASE_URL: 'http://localhost:54321',
  VITE_SUPABASE_ANON_KEY: 'test-anon-key'
}))

// Global test utilities can be added here