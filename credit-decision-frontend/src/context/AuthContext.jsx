import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const verifyUser = async () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                try {
                    const response = await authService.verifyToken();
                    // response is { valid: true, user: { ... } }
                    setUser(response.user || response);
                } catch (error) {
                    console.error('Token verification failed:', error);
                    localStorage.removeItem('access_token');
                    setUser(null);
                }
            }
            setLoading(false);
        };

        verifyUser();
    }, []);

    const login = async (credentials) => {
        try {
            const response = await authService.login(credentials);
            const { access_token, user: userData } = response;
            localStorage.setItem('access_token', access_token);
            setUser(userData);
            return response;
        } catch (error) {
            throw error;
        }
    };

    const registerUser = async (userData) => {
        try {
            const response = await authService.register(userData);
            const { access_token, user: newUser } = response;
            localStorage.setItem('access_token', access_token);
            setUser(newUser);
            return response;
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, registerUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
