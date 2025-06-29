export function parseErrorResponse(error: any) {
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
