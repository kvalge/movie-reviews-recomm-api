import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/authStore'

const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
})

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('has initial state', () => {
    const store = useAuthStore()
    
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBe(null)
    expect(store.token).toBe(undefined)
  })

  it('can set authentication', () => {
    const store = useAuthStore()
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      username: 'testuser'
    }
    const mockToken = 'mock-jwt-token'
    
    store.setAuth(mockToken, mockUser)
    
    expect(store.isAuthenticated).toBe(true)
    expect(store.user).toEqual(mockUser)
    expect(store.token).toBe(mockToken)
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', mockToken)
    expect(localStorageMock.setItem).toHaveBeenCalledWith('user', JSON.stringify(mockUser))
  })

  it('can logout user', () => {
    const store = useAuthStore()

    store.setAuth('mock-token', { id: 1, email: 'test@example.com', username: 'testuser' })
    
    store.logout()
    
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBe(null)
    expect(store.token).toBe(null)
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('token')
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('user')
  })

  it('has isAdmin getter', () => {
    const store = useAuthStore()

    expect(store.isAdmin).toBe(false)

    store.setAuth('mock-token', { id: 1, email: 'admin@example.com', username: 'admin' })
    expect(store.isAdmin).toBe(true)
  })
}) 