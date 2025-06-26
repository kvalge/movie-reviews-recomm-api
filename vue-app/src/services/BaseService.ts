import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios'

export abstract class BaseService {
  protected static axios: AxiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
      common: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    },
    timeout: 10000
  })

  static {
    this.axios.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    this.axios.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  protected static handleHttpError(error: AxiosError): string {
    if (error.response) {
      const status = error.response.status
      const statusText = error.response.statusText
      
      switch (status) {
        case 400:
          return 'Bad request - please check your input'
        case 401:
          return 'Unauthorized - please log in again'
        case 403:
          return 'Forbidden - you don\'t have permission'
        case 404:
          return 'Resource not found'
        case 422:
          return 'Validation error - please check your input'
        case 500:
          return 'Server error - please try again later'
        default:
          return `${status} ${statusText}`
      }
    } else if (error.request) {
      return 'Network error - please check your connection'
    } else {
      return error.message || 'An unexpected error occurred'
    }
  }
}
