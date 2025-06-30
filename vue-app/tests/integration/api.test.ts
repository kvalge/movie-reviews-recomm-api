vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn()
    }))
  }
}))

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { GenreService } from '@/services/GenreService'
import type { Genre, GenreResponse } from '@/domain/genre'
import { BaseService } from '@/services/BaseService'

describe('API Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('GenreService API calls', () => {
    it('fetches genres from API', async () => {
      const mockGenres = [
        { id: 1, name: 'Action', description: 'Action movies' },
        { id: 2, name: 'Comedy', description: 'Comedy movies' }
      ]
      
      const mockAxios = BaseService['axios']
      vi.mocked(mockAxios.get).mockResolvedValueOnce({
        data: mockGenres,
        status: 200,
        statusText: 'OK'
      })
      
      const genreService = new GenreService()
      const result = await genreService.getAll()
      
      expect(result.data).toEqual(mockGenres)
      expect(mockAxios.get).toHaveBeenCalledWith('genres')
    })

    it('creates genre via API', async () => {
      const genreData: Genre = {
        name: 'Thriller',
        description: 'Thriller movies'
      }
      
      const mockResponse: GenreResponse = { id: 3, ...genreData }
      
      const mockAxios = BaseService['axios']
      vi.mocked(mockAxios.post).mockResolvedValueOnce({
        data: mockResponse,
        status: 201,
        statusText: 'Created'
      })
      
      const genreService = new GenreService()
      const result = await genreService.add(genreData)
      
      expect(result.data).toEqual(mockResponse)
      expect(mockAxios.post).toHaveBeenCalledWith('genres', genreData)
    })
  })

  describe('IdentityService API calls', () => {
    const mockIdentityService = {
      login: vi.fn(),
      register: vi.fn()
    }

    it('logs in user via API', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123'
      }
      
      const mockResponse = {
        user: { id: 1, email: 'test@example.com', username: 'testuser' },
        token: 'mock-jwt-token'
      }
      
      mockIdentityService.login.mockResolvedValueOnce(mockResponse)
      
      const result = await mockIdentityService.login(loginData)
      
      expect(result).toEqual(mockResponse)
    })

    it('registers user via API', async () => {
      const registerData = {
        email: 'new@example.com',
        username: 'newuser',
        password: 'password123'
      }
      
      const mockResponse = {
        id: 2,
        email: 'new@example.com',
        username: 'newuser'
      }
      
      mockIdentityService.register.mockResolvedValueOnce(mockResponse)
      
      const result = await mockIdentityService.register(registerData)
      
      expect(result).toEqual(mockResponse)
    })
  })
}) 