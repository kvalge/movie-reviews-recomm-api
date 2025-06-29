import {BaseService} from './BaseService'
import type {AuthResponse} from '../domain/auth'
import {parseErrorResponse} from "../../utils/errorHandler.ts";

export abstract class IdentityService extends BaseService {
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
            return parseErrorResponse(error);
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
            return parseErrorResponse(error);
        }
    }
}

