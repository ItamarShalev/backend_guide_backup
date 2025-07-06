const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (this.token && !config.headers.Authorization) {
      config.headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // If response is not JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      // Handle empty responses (like DELETE requests)
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return {};
      }
    } catch (error) {
      console.error('API request failed:', error);
      
      // Handle network errors
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
        throw new Error('Cannot connect to server. Please check if the backend is running on http://127.0.0.1:8000');
      }
      
      throw error;
    }
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  // Auth endpoints
  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await this.request('/auth/login', {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it for FormData
    });

    this.setToken(response.access_token);
    return response;
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Todo endpoints
  async getTodos(completed = null) {
    const params = completed !== null ? `?completed=${completed}` : '';
    return this.request(`/todos/${params}`);
  }

  async createTodo(todoData) {
    return this.request('/todos/', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async updateTodo(todoId, todoData) {
    return this.request(`/todos/${todoId}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  }

  async deleteTodo(todoId) {
    return this.request(`/todos/${todoId}`, {
      method: 'DELETE',
    });
  }

  async uploadAttachment(todoId, file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.request(`/todos/${todoId}/attachment`, {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type for FormData
    });
  }
}

export default new ApiService();
