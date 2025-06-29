import { defineStore } from 'pinia'
import type { UserResponse } from '../domain/auth'

interface AuthState {
  token: string | null
  user: UserResponse | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: (() => {
      const userData = localStorage.getItem('user')
      try {
        return userData ? JSON.parse(userData) as UserResponse : null
      } catch (e) {
        console.error('Invalid user data in localStorage')
        return null
      }
    })(),
  }),

  actions: {
    setAuth(token: string, user: UserResponse) {
      this.token = token
      this.user = user
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },

  getters: {
    isAuthenticated: (state): boolean => !!state.token,
    isAdmin: (state): boolean => state.user?.username === 'admin',
  },
})
