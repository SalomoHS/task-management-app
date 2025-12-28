import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import LoginForm from './LoginForm.vue'

// Mock vue-router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

describe('LoginForm.vue', () => {
  it('renders login form', () => {
    setActivePinia(createPinia())
    const wrapper = mount(LoginForm)
    expect(wrapper.find('h2').text()).toBe('Login')
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login')
  })
})
