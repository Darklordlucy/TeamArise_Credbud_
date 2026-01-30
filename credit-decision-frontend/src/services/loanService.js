import api from './api';

const loanService = {
    // Submit loan application
    applyForLoan: async (loanData) => {
        try {
            const response = await api.post('/api/loans/apply', loanData);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    },

    // Get user's loans
    getUserLoans: async (userId) => {
        try {
            const response = await api.get(`/api/loans/user/${userId}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    },

    // Get loan details
    getLoanById: async (loanId) => {
        try {
            const response = await api.get(`/api/loans/${loanId}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
};

export default loanService;
