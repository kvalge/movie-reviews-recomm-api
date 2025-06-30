import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { setActivePinia, createPinia } from 'pinia'
import Header from '@/components/layout/Header.vue'
import { useAuthStore } from '@/stores/authStore'

// Mock vue-router
import { vi } from 'vitest'
vi.mock('vue-router', () => ({
  RouterLink: {
    name: 'RouterLink',
    props: ['to'],
    template: '<a :href="to"><slot /></a>'
  },
  useRouter: () => ({
    push: vi.fn()
  })
}))

describe('Header Component', () => {
  beforeEach(() => {
    const pinia = createPinia()
    setActivePinia(pinia)

    localStorage.clear()
  })

  afterEach(() => {
    localStorage.clear()
  })

  it('renders navigation links', () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('Movies')
  })

  it('shows login/register links when not authenticated', () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: {
              token: null,
              user: null
            }
          }
        })]
      }
    })
    
    expect(wrapper.text()).toContain('Login')
    expect(wrapper.text()).toContain('Register')
    expect(wrapper.text()).not.toContain('Logout')
  })

  it('shows logout link when authenticated', () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: {
              token: 'test-token',
              user: { id: 2, username: 'testuser', email: 'test@example.com' }
            }
          }
        })]
      }
    })

    expect(wrapper.text()).toContain('Logout')
    expect(wrapper.text()).not.toContain('Login')
    expect(wrapper.text()).not.toContain('Register')
  })

  it('shows admin links when user is admin', () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: {
              token: 'test-token',
              user: { id: 1, username: 'admin', email: 'admin@example.com' }
            }
          }
        })]
      }
    })

    expect(wrapper.text()).toContain('Add Review')
    expect(wrapper.text()).toContain('Manage Movie Data')
  })

  it('handles logout action', async () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: {
              token: 'test-token',
              user: { id: 2, username: 'testuser', email: 'test@example.com' }
            }
          }
        })]
      }
    })

    const authStore = useAuthStore()
    const logoutLink = wrapper.find('a[href="#"]')
    await logoutLink.trigger('click')

    expect(authStore.logout).toHaveBeenCalled()
  })
}) 