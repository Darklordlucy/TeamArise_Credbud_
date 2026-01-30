import api from './api';

const transactionService = {
    // Upload transaction file
    uploadTransactions: async (file, monthlyIncome) => {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('monthly_income', monthlyIncome);

            const response = await api.post('/api/transactions/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    },

    // Get financial behavior analysis
    getFinancialBehavior: async (userId) => {
        try {
            const response = await api.get(`/api/transactions/analyze/${userId}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
};

export default transactionService;
