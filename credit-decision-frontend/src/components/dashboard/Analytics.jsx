import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../common/Card';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const Analytics = ({ behavior }) => {
    // Check if behavior data exists
    const hasData = behavior && behavior.category_scores;

    // Prepare category data for PieChart
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

    const categoryData = hasData
        ? Object.entries(behavior.category_scores).map(([key, data]) => ({
            name: categoryMapping[key] || key,
            value: data.spending || 0
        })).filter(item => item.value > 0)
        : [];

    const COLORS = [
        '#2563eb', '#10b981', '#f59e0b', '#ef4444',
        '#8b5cf6', '#ec4899', '#06b6d4', '#4b5563'
    ];

    if (!hasData) {
        return (
            <div className="space-y-6">
                <div className="mb-8">
                    <h1 className="text-2xl font-bold text-gray-900">Financial Analytics</h1>
                    <p className="text-gray-600 mt-2">Insights into your spending habits and financial stability.</p>
                </div>
                <Card>
                    <CardContent className="h-[300px] flex items-center justify-center">
                        <p className="text-gray-500">Upload your transaction history to see analytics.</p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-gray-900">Financial Analytics</h1>
                <p className="text-gray-600 mt-2">Insights into your spending habits and financial stability.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Metrics Summary */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle>Spending Summary</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="p-4 bg-blue-50 rounded-xl">
                                <p className="text-sm text-blue-600 font-medium">Liquidity Resilience</p>
                                <p className="text-2xl font-bold text-blue-900">{behavior.liquidity_resilience_days} Days</p>
                                <p className="text-xs text-blue-500 mt-1">Survive without income</p>
                            </div>
                            <div className="p-4 bg-green-50 rounded-xl">
                                <p className="text-sm text-green-600 font-medium">Cash Flow Pattern</p>
                                <p className="text-2xl font-bold text-green-900 capitalize">{behavior.cash_inflow_pattern}</p>
                                <p className="text-xs text-green-500 mt-1">Stability indicator</p>
                            </div>
                            <div className="p-4 bg-purple-50 rounded-xl">
                                <p className="text-sm text-purple-600 font-medium">History Depth</p>
                                <p className="text-2xl font-bold text-purple-900">{behavior.transaction_depth_days} Days</p>
                                <p className="text-xs text-purple-500 mt-1">Analysis coverage</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Categories Chart */}
                <Card>
                    <CardHeader>
                        <CardTitle>Expense Distribution (₹)</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[400px]">
                        {categoryData.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={categoryData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={true}
                                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                        outerRadius={120}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {categoryData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        formatter={(value) => `₹${value.toLocaleString()}`}
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="h-full flex items-center justify-center text-gray-500">
                                No spending data to display.
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Score vs Targets */}
                <Card>
                    <CardHeader>
                        <CardTitle>Category Targets</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {Object.entries(behavior.category_scores).map(([key, data], idx) => (
                                <div key={key} className="space-y-1">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-700 font-medium">{categoryMapping[key] || key}</span>
                                        <span className={data.point === 1 ? 'text-green-600' : 'text-red-600'}>
                                            {data.percentage.toFixed(1)}% / {data.threshold}%
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                                        <div
                                            className={`h-full rounded-full transition-all duration-1000 ${data.point === 1 ? 'bg-green-500' : 'bg-red-500'}`}
                                            style={{ width: `${Math.min(data.percentage / data.threshold * 100, 100)}%` }}
                                        ></div>
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

export default Analytics;
