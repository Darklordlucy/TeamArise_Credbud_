import React, { useState } from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import BankFilters from '../components/banks/BankFilters';
import BankCard from '../components/banks/BankCard';
import Modal from '../components/common/Modal';
import { Button } from '../components/common/Button';
import { CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

const BankStats = () => {
    const [filters, setFilters] = useState({ search: '', minAmount: '', maxRate: '' });
    const [selectedBank, setSelectedBank] = useState(null);

    // Mock Data
    const banks = [
        { id: 1, name: "HDFC Bank", interestRate: 10.5, processingFee: 2, tenure: "1-5 Years", maxAmount: 500000, rating: 4.8, reviews: 1250, approvalTime: "24 Hours" },
        { id: 2, name: "ICICI Bank", interestRate: 11.0, processingFee: 1.5, tenure: "1-4 Years", maxAmount: 400000, rating: 4.6, reviews: 980, approvalTime: "48 Hours" },
        { id: 3, name: "Axis Bank", interestRate: 12.5, processingFee: 1, tenure: "2-5 Years", maxAmount: 300000, rating: 4.5, reviews: 670, approvalTime: "36 Hours" },
        { id: 4, name: "Kotak Bank", interestRate: 13.0, processingFee: 0.5, tenure: "1-3 Years", maxAmount: 200000, rating: 4.2, reviews: 450, approvalTime: "12 Hours" },
        { id: 5, name: "SBI Bank", interestRate: 9.8, processingFee: 1.25, tenure: "1-7 Years", maxAmount: 1000000, rating: 4.9, reviews: 2100, approvalTime: "72 Hours" },
        { id: 6, name: "Bajaj Finserv", interestRate: 14.0, processingFee: 2.5, tenure: "1-2 Years", maxAmount: 150000, rating: 4.0, reviews: 320, approvalTime: "6 Hours" },
    ];

    const filteredBanks = banks.filter(bank => {
        if (filters.search && !bank.name.toLowerCase().includes(filters.search.toLowerCase())) return false;
        if (filters.maxRate && bank.interestRate > Number(filters.maxRate)) return false;
        if (filters.minAmount && bank.maxAmount < Number(filters.minAmount)) return false;
        return true;
    });

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex-grow container mx-auto px-4 py-8 md:px-6">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Banks Statistics</h1>
                    <p className="text-gray-600 mt-2">Compare interest rates and approval times to find your best match.</p>
                </div>

                <BankFilters filters={filters} setFilters={setFilters} />

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredBanks.map(bank => (
                        <BankCard key={bank.id} bank={bank} onDetails={setSelectedBank} />
                    ))}
                </div>

                {filteredBanks.length === 0 && (
                    <div className="text-center py-20 text-gray-500">
                        No banks found matching your filters.
                    </div>
                )}
            </main>
            <Footer />

            <Modal
                isOpen={!!selectedBank}
                onClose={() => setSelectedBank(null)}
                title={selectedBank?.name}
            >
                {selectedBank && (
                    <div className="space-y-6">
                        <div className="p-4 bg-blue-50 rounded-lg text-sm text-blue-800 flex items-start">
                            <CheckCircle2 className="h-5 w-5 mr-3 flex-shrink-0 mt-0.5" />
                            <div>
                                <strong>Recommended for you!</strong> Based on your profile, you have a high chance of approval with {selectedBank.name}.
                            </div>
                        </div>

                        <div className="space-y-4">
                            <h4 className="font-semibold text-gray-900">Key Features</h4>
                            <ul className="list-disc pl-5 space-y-1 text-gray-600">
                                <li>Instant approval within {selectedBank.approvalTime}</li>
                                <li>Minimal documentation required (Aadhar + Pan)</li>
                                <li>Flexible repayment options up to {selectedBank.tenure}</li>
                            </ul>
                        </div>

                        <div className="space-y-4">
                            <h4 className="font-semibold text-gray-900">Fees & Charges</h4>
                            <div className="grid grid-cols-2 gap-4 text-sm">
                                <div className="text-gray-500">Processing Fee</div>
                                <div className="font-medium">{selectedBank.processingFee}%</div>
                                <div className="text-gray-500">Pre-closure Charges</div>
                                <div className="font-medium">2% (After 6 months)</div>
                            </div>
                        </div>

                        <div className="flex gap-4 pt-4">
                            <Button variant="outline" className="flex-1" onClick={() => setSelectedBank(null)}>Close</Button>
                            <Link to="/apply" className="flex-1">
                                <Button className="w-full">Apply Now</Button>
                            </Link>
                        </div>
                    </div>
                )}
            </Modal>
        </div>
    );
};

export default BankStats;
