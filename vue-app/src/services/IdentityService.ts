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
        password: string,
    ): Promise<{
        data?: UserResponse
        status?: string
        statusText?: string
        errors?: string[]
    }> {
        const url = 'users/register'
        try {
            const registerData = {
                username,
                email,
                password,
            }

            const response = await this.axios.post<UserResponse>(url, registerData)

            console.log('register response', response)

            if (response.status <= 300) {
                console.log('response.data', response.data)
                return {data: response.data}
            }

            return {
                errors: [(response.status.toString() + ' ' + response.statusText).trim()],
            }
        } catch (error: any) {
            console.log('error: ', error.message)
            if (error.response?.data?.detail) {
                return {
                    errors: [error.response.data.detail],
                }
            }
            return {
                errors: [error.message || 'Registration failed'],
            }
        }
    }
}
