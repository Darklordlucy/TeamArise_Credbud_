import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from '../components/dashboard/DashboardLayout';
import RecentLoans from '../components/dashboard/RecentLoans';
import TransactionUpload from '../components/dashboard/TransactionUpload';
import FinancialBehaviorScore from '../components/dashboard/FinancialBehaviorScore';
import Analytics from '../components/dashboard/Analytics';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/common/Card';
import { TrendingUp, UserCheck, AlertTriangle, DollarSign } from 'lucide-react';
import { formatCurrency } from '../utils/helpers';
import transactionService from '../services/transactionService';
import loanService from '../services/loanService';

// Dashboard Overview Widget
const Overview = ({ behavior }) => {
    const { user } = useAuth();
    const [loans, setLoans] = React.useState([]);

    React.useEffect(() => {
        const fetchLoans = async () => {
            if (user?.id) {
                try {
                    const data = await loanService.getUserLoans(user.id);
                    setLoans(data);
                } catch (err) {
                    console.error('Failed to fetch loans:', err);
                }
            }
        };
        fetchLoans();
    }, [user?.id]);

    const activeLoansCount = loans.filter(l => l.status === 'processing' || l.status === 'approved').length;
    const totalLoanAmount = loans.reduce((sum, l) => sum + (l.amount_requested || 0), 0);
    const score = behavior?.total_score || 0;
    const rating = behavior?.behavior_rating || 'N/A';

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Welcome back, {user?.name || user?.full_name || 'User'}!</h1>
                    <p className="text-gray-500">Here's what's happening with your loan applications.</p>
                </div>
                <div className="text-sm text-gray-500 bg-white px-4 py-2 rounded-lg border border-gray-100 shadow-sm">
                    Last login: {new Date().toLocaleDateString()}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white border-none">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-blue-100 uppercase tracking-wider">Financial Score</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">{score}/8</div>
                        <div className="mt-2 text-blue-100 text-sm">
                            Rating: <span className="capitalize font-semibold">{rating}</span>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
                        <CardTitle className="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Applications</CardTitle>
                        <DollarSign className="h-4 w-4 text-gray-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{loans.length}</div>
                        <div className="mt-1 text-sm text-gray-500">Total Requested: {formatCurrency(totalLoanAmount)}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium text-gray-500 uppercase tracking-wider">Active Loans</CardTitle>
                        <UserCheck className="h-4 w-4 text-gray-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{activeLoansCount}</div>
                        <div className="mt-1 text-sm text-gray-500">Approved or Processing</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
                        <CardTitle className="text-sm font-medium text-gray-500 uppercase tracking-wider">Stability</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-gray-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-yellow-600">
                            {behavior?.has_stable_inflow ? 'Stable' : 'Unstable'}
                        </div>
                        <div className="mt-1 text-sm text-gray-500">Based on cash inflow</div>
                    </CardContent>
                </Card>
            </div>

            <RecentLoans loans={loans} />
        </div>
    );
};

const Dashboard = () => {
    const { user, loading: authLoading } = useAuth();
    const [behavior, setBehavior] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    const fetchFinancialBehavior = React.useCallback(async () => {
        if (!user?.id) return;
        try {
            const data = await transactionService.getFinancialBehavior(user.id);
            setBehavior(data);
        } catch (error) {
            console.error('Failed to fetch financial behavior:', error);
        } finally {
            setLoading(false);
        }
    }, [user?.id]);

    React.useEffect(() => {
        if (user) {
            fetchFinancialBehavior();
        } else if (!authLoading) {
            setLoading(false);
        }
    }, [user, authLoading, fetchFinancialBehavior]);

    if (authLoading || loading) return <div>Loading...</div>;
    if (!user) return <Navigate to="/login" replace />;

    return (
        <Routes>
            <Route element={<DashboardLayout />}>
                <Route index element={<Overview behavior={behavior} />} />
                <Route path="recent" element={<RecentLoans />} />
                <Route path="upload" element={<TransactionUpload onUploadSuccess={fetchFinancialBehavior} />} />
                <Route path="behavior" element={<FinancialBehaviorScore behavior={behavior} />} />
                <Route path="analytics" element={<Analytics behavior={behavior} />} />
                {/* Fallback */}
                <Route path="*" element={<Overview behavior={behavior} />} />
            </Route>
        </Routes>
    );
};

export default Dashboard;
