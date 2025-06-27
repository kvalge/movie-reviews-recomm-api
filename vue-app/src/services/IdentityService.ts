import {BaseService} from './BaseService'

export interface UserResponse {
    id: number
    username: string
    email: string
}

export abstract class IdentityService extends BaseService {
    static async register(
        username: string,
        email: string,
        password: string
    ): Promise<{
        data?: UserResponse
        status?: string
        statusText?: string
        errors?: string[]
        errorsByField?: Record<string, string[]>
    }> {
        const url = 'users/register'

        try {
            const registerData = {username, email, password}
            const response = await this.axios.post<UserResponse>(url, registerData)

            return {
                data: response.data,
                status: response.status.toString(),
                statusText: response.statusText,
            }
        } catch (error: any) {
            if (error.response?.data?.detail) {
                const detail = error.response.data.detail

                if (Array.isArray(detail)) {
                    const errorsByField: Record<string, string[]> = {}

                    for (const err of detail) {
                        const field = err.loc && err.loc.length > 1 ? err.loc[1] : '_general'
                        if (!errorsByField[field]) errorsByField[field] = []
                        errorsByField[field].push(err.msg || JSON.stringify(err))
                    }

                    return {
                        status: error.response.status.toString(),
                        statusText: error.response.statusText,
                        errorsByField,
                    }
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
    }
}
