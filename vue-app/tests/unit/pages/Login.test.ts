import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Login from '@/pages/Login.vue'

describe('Login Page', () => {
  it('renders login form', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [createPinia()]
      }
    })
    
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('submits form with valid data', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [createPinia()]
      }
    })
    
    await wrapper.find('input[type="text"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('has reset button functionality', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [createPinia()]
      }
    })

    await wrapper.find('input[type="text"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')

    await wrapper.find('button[type="button"]').trigger('click')

    expect((wrapper.find('input[type="text"]').element as HTMLInputElement).value).toBe('')
    expect((wrapper.find('input[type="password"]').element as HTMLInputElement).value).toBe('')
  })
}) 