import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../common/Card';
import { Button } from '../common/Button';
import { Upload, File, AlertCircle } from 'lucide-react';
import { toast } from 'react-hot-toast';
import transactionService from '../../services/transactionService';

const TransactionUpload = ({ onUploadSuccess }) => {
    const [files, setFiles] = useState([]);
    const [monthlyIncome, setMonthlyIncome] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const onDrop = useCallback(acceptedFiles => {
        // We only support one file at a time for analysis
        setFiles(acceptedFiles);
        if (acceptedFiles.length > 0) {
            toast.success(`File "${acceptedFiles[0].name}" added`);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'text/csv': ['.csv'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx', '.xls']
        },
        maxFiles: 1
    });

    const handleUpload = async () => {
        if (files.length === 0) {
            toast.error("Please select a file first");
            return;
        }
        if (!monthlyIncome || isNaN(monthlyIncome)) {
            toast.error("Please enter a valid monthly income");
            return;
        }

        setIsLoading(true);
        const uploadPromise = transactionService.uploadTransactions(files[0], monthlyIncome);

        toast.promise(uploadPromise, {
            loading: 'Uploading and analyzing your transactions...',
            success: (data) => {
                setFiles([]);
                setMonthlyIncome('');
                if (onUploadSuccess) onUploadSuccess();
                return 'Transactions analyzed successfully!';
            },
            error: (err) => {
                console.error('Upload error:', err);
                return err.detail || 'Upload failed. Please try again.';
            },
        });

        try {
            await uploadPromise;
        } catch (err) {
            // Error handled by toast.promise
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-500">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-gray-900">Upload Transactions</h1>
                <p className="text-gray-600 mt-2">Upload your bank statement (CSV/Excel) to receive your real-time behavior score.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>File Upload</CardTitle>
                        <CardDescription>Supported formats: .csv, .xlsx, .xls</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div
                            {...getRootProps()}
                            className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
                                ${isDragActive ? "border-primary bg-primary/5" : "border-gray-200 hover:border-primary hover:bg-gray-50"}`}
                        >
                            <input {...getInputProps()} />
                            <div className="mx-auto h-12 w-12 text-gray-400 mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                                <Upload className="h-6 w-6" />
                            </div>
                            {isDragActive ? (
                                <p className="text-primary font-medium">Drop the CSV file here...</p>
                            ) : (
                                <div className="space-y-1">
                                    <p className="text-gray-700 font-medium">Click to upload or drag and drop</p>
                                    <p className="text-sm text-gray-500">Limit: 1 file, Max 10MB</p>
                                </div>
                            )}
                        </div>

                        {files.length > 0 && (
                            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100 flex items-center justify-between">
                                <div className="flex items-center space-x-3">
                                    <File className="h-5 w-5 text-blue-600" />
                                    <div>
                                        <div className="text-sm font-medium text-blue-900">{files[0].name}</div>
                                        <div className="text-xs text-blue-700">{(files[0].size / 1024).toFixed(1)} KB</div>
                                    </div>
                                </div>
                                <button
                                    onClick={() => setFiles([])}
                                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                                >
                                    Change file
                                </button>
                            </div>
                        )}
                    </CardContent>
                </Card>

                <Card className="md:col-span-1">
                    <CardHeader>
                        <CardTitle>Details</CardTitle>
                        <CardDescription>Required for scoring</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Monthly Income (₹)
                            </label>
                            <input
                                type="number"
                                value={monthlyIncome}
                                onChange={(e) => setMonthlyIncome(e.target.value)}
                                placeholder="e.g. 50000"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                                required
                            />
                        </div>
                        <Button
                            className="w-full"
                            onClick={handleUpload}
                            disabled={isLoading || files.length === 0 || !monthlyIncome}
                            isLoading={isLoading}
                        >
                            Analyze Now
                        </Button>
                    </CardContent>
                </Card>
            </div>

            <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-4 flex items-start space-x-3">
                <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-yellow-800">
                    <p className="font-semibold mb-1">Security Note:</p>
                    <p>Your data is processed securely and used only to generate your financial behavior score. We do not share your raw transaction data with third parties.</p>
                </div>
            </div>
        </div>
    );
};

export default TransactionUpload;
