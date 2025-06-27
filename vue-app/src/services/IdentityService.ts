import {BaseService} from './BaseService'
import type {AuthResponse} from '../domain/auth'


export abstract class IdentityService extends BaseService {
    private static parseErrorResponse(error: any) {
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (Array.isArray(detail)) {
                const errorsByField: Record<string, string[]> = {};
                for (const err of detail) {
                    const field = err.loc && err.loc.length > 1 ? err.loc[1] : '_general';
                    if (!errorsByField[field]) errorsByField[field] = [];
                    errorsByField[field].push(err.msg || JSON.stringify(err));
                }
                return {
                    status: error.response.status.toString(),
                    statusText: error.response.statusText,
                    errorsByField,
                };
            } else if (typeof detail === 'string') {
                return {
                    status: error.response.status.toString(),
                    statusText: error.response.statusText,
                    errors: [detail],
                };
            }
        }
        if (error.code === 'ERR_NETWORK') {
            return {
                errors: ['Network error. Please check your connection.'],
            };
        }
        return {
            status: error.response?.status?.toString() || 'unknown',
            statusText: error.response?.statusText || 'unknown',
            errors: [error.message || 'Request failed'],
        };
    }

    static async register(
        username: string,
        email: string,
        password: string
    ): Promise<{
        data?: AuthResponse;
        status?: string;
        statusText?: string;
        errors?: string[];
        errorsByField?: Record<string, string[]>;
    }> {
        const url = 'users/register';

        try {
            const registerData = {username, email, password};
            const response = await this.axios.post<AuthResponse>(url, registerData);

            return {
                data: response.data,
                status: response.status.toString(),
                statusText: response.statusText,
            };
        } catch (error: any) {
            return this.parseErrorResponse(error);
        }
    }

    static async login(
        identifier: string,
        password: string
    ): Promise<{
        data?: AuthResponse;
        status?: string;
        statusText?: string;
        errors?: string[];
        errorsByField?: Record<string, string[]>;
    }> {
        const url = 'users/login';
        try {
            const loginData = {identifier, password};
            const response = await this.axios.post<AuthResponse>(url, loginData);
            return {
                data: response.data,
                status: response.status.toString(),
                statusText: response.statusText,
            };
        } catch (error: any) {
            return this.parseErrorResponse(error);
        }
    }
}

