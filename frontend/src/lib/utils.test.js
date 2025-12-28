import { describe, it, expect } from 'vitest'
import { cn } from './utils'

describe('utils', () => {
  it('cn merges class names correctly', () => {
    expect(cn('c1', 'c2')).toBe('c1 c2')
    expect(cn('px-2 py-1', 'p-4')).toBe('p-4') // tailwind-merge behavior
  })
})
