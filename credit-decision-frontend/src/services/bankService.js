import api from './api';

const bankService = {
    // Get all banks
    getAllBanks: async () => {
        try {
            const response = await api.get('/api/banks/');
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    },

    // Get top banks
    getTopBanks: async (limit = 10) => {
        try {
            const response = await api.get(`/api/banks/top?limit=${limit}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    },

    // Get trusted banks
    getTrustedBanks: async (limit = 10) => {
        try {
            const response = await api.get(`/api/banks/trusted?limit=${limit}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
};

export default bankService;
