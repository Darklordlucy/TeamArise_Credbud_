import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../common/Card';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { Check, X } from 'lucide-react';

const FinancialBehaviorScore = ({ behavior }) => {
    // If no behavior data, show message
    if (!behavior || !behavior.category_scores) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Financial Behavior Score</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-center text-gray-500 py-8">
                        Upload your transaction history to see your financial behavior score
                    </p>
                </CardContent>
            </Card>
        );
    }

    const score = behavior.total_score || 0;
    const maxScore = 8;
    const behaviorRating = behavior.behavior_rating || 'average';

    // Get rating text and color
    const getRatingInfo = (rating) => {
        switch (rating) {
            case 'good':
                return { text: 'Excellent', color: 'text-green-600' };
            case 'average':
                return { text: 'Average', color: 'text-yellow-600' };
            case 'bad':
                return { text: 'Needs Improvement', color: 'text-red-600' };
            default:
                return { text: 'Unknown', color: 'text-gray-600' };
        }
    };

    const ratingInfo = getRatingInfo(behaviorRating);

    // Prepare chart data
    const data = [
        { name: 'Score', value: score },
        { name: 'Remaining', value: maxScore - score },
    ];
    const COLORS = ['#10b981', '#e5e7eb'];

    // Prepare categories from backend data
    const categoryMapping = {
        'transport': 'Transport',
        'education': 'Education',
        'medical': 'Medical',
        'food_shopping': 'Food & Shopping',
        'groceries': 'Groceries',
        'emi': 'EMI',
        'entertainment': 'Entertainment',
        'others': 'Others'
    };

    const categories = Object.entries(behavior.category_scores || {}).map(([key, data]) => ({
        name: categoryMapping[key] || key,
        spent: data.percentage || 0,
        threshold: data.threshold || 0,
        point: data.point || 0,
        spending: data.spending || 0
    }));

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Financial Behavior Score</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Score Gauge */}
                <Card className="md:col-span-1">
                    <CardHeader>
                        <CardTitle className="text-center">Overall Score</CardTitle>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center min-h-[300px]">
                        <div className="w-48 h-48 relative">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={data}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        paddingAngle={5}
                                        dataKey="value"
                                        startAngle={180}
                                        endAngle={0}
                                    >
                                        {data.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center mt-4">
                                <div className="text-4xl font-bold text-gray-900">{score}/{maxScore}</div>
                                <div className={`text-sm font-medium ${ratingInfo.color}`}>{ratingInfo.text}</div>
                            </div>
                        </div>
                        <p className="text-center text-sm text-gray-500 mt-4">
                            {behaviorRating === 'good' && 'Your financial health is excellent!'}
                            {behaviorRating === 'average' && 'Your financial health is average.'}
                            {behaviorRating === 'bad' && 'Consider improving your spending habits.'}
                        </p>

                        {/* Additional Metrics */}
                        <div className="mt-4 w-full space-y-2 text-sm">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Cash Inflow:</span>
                                <span className="font-medium">{behavior.cash_inflow_pattern || 'N/A'}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Liquidity Days:</span>
                                <span className="font-medium">{behavior.liquidity_resilience_days || 0} days</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Transaction Depth:</span>
                                <span className="font-medium">{behavior.transaction_depth_days || 0} days</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Breakdown */}
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Category Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {categories.map((cat, idx) => (
                                <div key={idx} className="bg-gray-50 p-4 rounded-lg flex items-center justify-between">
                                    <div>
                                        <div className="font-semibold text-gray-900">{cat.name}</div>
                                        <div className="text-sm text-gray-500">
                                            Spent: {cat.spent.toFixed(1)}% / Max: {cat.threshold.toFixed(0)}%
                                        </div>
                                        <div className="text-xs text-gray-400 mt-1">
                                            ₹{cat.spending.toLocaleString()}
                                        </div>
                                    </div>
                                    <div className="flex items-center">
                                        {cat.point === 1 ? (
                                            <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                                                <Check className="h-4 w-4" />
                                            </div>
                                        ) : (
                                            <div className="h-8 w-8 rounded-full bg-red-100 flex items-center justify-center text-red-600">
                                                <X className="h-4 w-4" />
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default FinancialBehaviorScore;
