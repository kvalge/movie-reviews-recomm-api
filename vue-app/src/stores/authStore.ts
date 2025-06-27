import { defineStore } from 'pinia'
import type { UserResponse } from '../domain/auth'

interface AuthState {
  token: string | null
  user: UserResponse | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: localStorage.getItem('user')
      ? JSON.parse(localStorage.getItem('user')!)
      : null,
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
    isAuthenticated: (state) => !!state.token,
  },
})
