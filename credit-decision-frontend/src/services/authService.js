import api from './api';

const authService = {
    register: async (userData) => {
        try {
            const response = await api.post('/api/auth/register', userData);
            return response.data;
        } catch (error) {
            // Extract error message from axios error response
            if (error.response?.data) {
                throw error.response.data;
            }
            throw error;
        }
    },

    login: async (credentials) => {
        try {
            const response = await api.post('/api/auth/login', credentials);
            return response.data;
        } catch (error) {
            // Extract error message from axios error response
            if (error.response?.data) {
                throw error.response.data;
            }
            throw error;
        }
    },

    verifyToken: async () => {
        try {
            const response = await api.get('/api/auth/verify');
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

export default authService;
