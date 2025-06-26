import { BaseService } from './BaseService'

export interface UserResponse {
  id: number
  username: string
  email: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface ValidationError {
  loc: (string | number)[]
  msg: string
  type: string
}

export interface ServiceResponse<T = any> {
  data?: T
  status?: string
  statusText?: string
  errors?: string[]
  errorsByField?: Record<string, string[]>
}

export abstract class IdentityService extends BaseService {
    static async register(
        username: string,
        email: string,
        password: string,
    ): Promise<ServiceResponse<UserResponse>> {
        const url = 'users/register'
        try {
            const registerData: RegisterRequest = { username, email, password }
            const response = await this.axios.post<UserResponse>(url, registerData)

            if (response.status < 400) {
                return {
                    data: response.data,
                    status: response.status.toString(),
                    statusText: response.statusText,
                }
            }

            return {
                status: response.status.toString(),
                statusText: response.statusText,
                errors: [`${response.status} ${response.statusText}`],
            }
        } catch (error: any) {
            return this.handleRegistrationError(error)
        }
    }

    private static handleRegistrationError(error: any): ServiceResponse<UserResponse> {
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail
            
            if (Array.isArray(detail)) {
                return this.parseValidationErrors(detail, error.response)
            } else if (typeof detail === 'string') {
                return {
                    status: error.response.status.toString(),
                    statusText: error.response.statusText,
                    errors: [detail],
                }
            }
        }

        return {
            errors: [error.message || 'Registration failed'],
        }
    }

    private static parseValidationErrors(
        errors: ValidationError[], 
        response: any
    ): ServiceResponse<UserResponse> {
        const errorsByField: Record<string, string[]> = {}
        
        for (const err of errors) {
            const field = err.loc && err.loc.length > 1 ? err.loc[1] : '_general'
            if (!errorsByField[field]) errorsByField[field] = []
            errorsByField[field].push(err.msg || JSON.stringify(err))
        }
        
        return {
            status: response.status.toString(),
            statusText: response.statusText,
            errorsByField,
        }
    }
}