import {BaseService} from './BaseService'

export abstract class IdentityService extends BaseService {
    static async register(
        username: string,
        email: string,
        password: string,
    ): Promise<{
        data?: { jwt: string; refreshToken: string }
        status?: string
        statusText?: string
        errors?: string[]
    }> {
        const url = 'register'
        try {
            const loginData = {
                username,
                email,
                password,
            }

            const response = await this.axios.post<{ jwt: string; refreshToken: string }>(url, loginData)

            console.log('login response', response)

            if (response.status <= 300) {
                console.log('response.data', response.data)
                return {data: response.data}
            }

            return {
                errors: [(response.status.toString() + ' ' + response.statusText).trim()],
            }
        } catch (error) {
            console.log('error: ', (error as Error).message)
            return {
                errors: [JSON.stringify(error)],
            }
        }
    }
}
