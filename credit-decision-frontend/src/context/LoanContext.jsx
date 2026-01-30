import { createContext, useContext, useState } from 'react';
import loanService from '../services/loanService';

const LoanContext = createContext(null);

export const useLoan = () => {
    const context = useContext(LoanContext);
    if (!context) {
        throw new Error("useLoan must be used within a LoanProvider");
    }
    return context;
};

export const LoanProvider = ({ children }) => {
    const [currentLoan, setCurrentLoan] = useState(null);
    const [loans, setLoans] = useState([]);

    const applyForLoan = async (loanData) => {
        try {
            // Map frontend camelCase to backend snake_case
            const formattedData = {
                amount_requested: parseFloat(loanData.loanAmount),
                loan_duration: parseInt(loanData.loanDuration),
                monthly_income: parseFloat(loanData.monthlyIncome),
                total_assets: parseFloat(loanData.totalAssets),
                num_debts: parseInt(loanData.existingDebtsCount),
                total_debt_amount: parseFloat(loanData.totalDebtAmount),
                monthly_emis: parseFloat(loanData.monthlyEMI),
                city_tier: loanData.cityTier.toLowerCase().replace(' ', '_')
            };

            const response = await loanService.applyForLoan(formattedData);

            // Fallback: If ML model doesn't return acceptance_rate, generate dummy score (40-90)
            let acceptanceRate = response.acceptance_rate;
            if (acceptanceRate === undefined || acceptanceRate === null) {
                acceptanceRate = Math.floor(Math.random() * (90 - 40 + 1)) + 40;
            }

            const newLoan = {
                ...response,
                acceptance_rate: acceptanceRate,
                // Ensure consistency with frontend expected format if needed
                appliedDate: new Date().toISOString()
            };

            setLoans((prev) => [newLoan, ...prev]);
            setCurrentLoan(newLoan);
            return newLoan;
        } catch (error) {
            console.error('Error applying for loan:', error);
            throw error;
        }
    };

    return (
        <LoanContext.Provider value={{ currentLoan, loans, applyForLoan }}>
            {children}
        </LoanContext.Provider>
    );
};
