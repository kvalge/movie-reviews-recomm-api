import { BaseService } from './BaseService';
import { parseErrorResponse } from '../../utils/errorHandler';

export abstract class BaseEntityService<TInput, TOutput> extends BaseService {
  protected abstract resourceUrl: string;

  async getAll(): Promise<{
    data?: TOutput[];
    status?: string;
    statusText?: string;
    errors?: string[];
  }> {
    try {
      const response = await BaseService.axios.get<TOutput[]>(this.resourceUrl);
      return {
        data: response.data,
        status: response.status.toString(),
        statusText: response.statusText,
      };
    } catch (error: any) {
      return parseErrorResponse(error);
    }
  }

  async getById(id: number): Promise<{
    data?: TOutput;
    status?: string;
    statusText?: string;
    errors?: string[];
  }> {
    try {
      const response = await BaseService.axios.get<TOutput>(`${this.resourceUrl}/${id}`);
      return {
        data: response.data,
        status: response.status.toString(),
        statusText: response.statusText,
      };
    } catch (error: any) {
      return parseErrorResponse(error);
    }
  }

  async add(entity: TInput): Promise<{
    data?: TOutput;
    status?: string;
    statusText?: string;
    errors?: string[];
    errorsByField?: Record<string, string[]>;
  }> {
    try {
      const response = await BaseService.axios.post<TOutput>(this.resourceUrl, entity);
      return {
        data: response.data,
        status: response.status.toString(),
        statusText: response.statusText,
      };
    } catch (error: any) {
      return parseErrorResponse(error);
    }
  }

  async update(id: number, entity: Partial<TInput>): Promise<{
    data?: TOutput;
    status?: string;
    statusText?: string;
    errors?: string[];
    errorsByField?: Record<string, string[]>;
  }> {
    try {
      const response = await BaseService.axios.put<TOutput>(`${this.resourceUrl}/${id}`, entity);
      return {
        data: response.data,
        status: response.status.toString(),
        statusText: response.statusText,
      };
    } catch (error: any) {
      return parseErrorResponse(error);
    }
  }

  async delete(id: number): Promise<{
    status?: string;
    statusText?: string;
    errors?: string[];
    errorsByField?: Record<string, string[]>;
  }> {
    try {
      const response = await BaseService.axios.delete(`${this.resourceUrl}/${id}`);
      return {
        status: response.status.toString(),
        statusText: response.statusText,
      };
    } catch (error: any) {
      return parseErrorResponse(error);
    }
  }
}
