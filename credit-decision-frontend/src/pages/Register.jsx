import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';
import Input from '../components/common/Input';
import Select from '../components/common/Select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/common/Card';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-hot-toast';

const Register = () => {
    const { registerUser } = useAuth();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);

    const { register, handleSubmit, formState: { errors } } = useForm({
        defaultValues: {
            full_name: '',
            email: '',
            phone: '',
            city_tier: 'tier_1',
            password: ''
        }
    });

    const onSubmit = async (data) => {
        setIsLoading(true);
        try {
            await registerUser(data);
            toast.success("Account created successfully!");
            navigate('/dashboard');
        } catch (error) {
            console.error('Registration error:', error);
            const errorMessage = error.detail || error.message || "Registration failed. Please try again.";
            toast.error(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const cityTierOptions = [
        { value: 'tier_1', label: 'Tier 1 (Metro)' },
        { value: 'tier_2', label: 'Tier 2 (Urban)' },
        { value: 'tier_3', label: 'Tier 3 (Semi-Urban/Rural)' }
    ];

    return (
        <div className="flex min-h-[80vh] items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
            <Card className="w-full max-w-md shadow-xl border-t-4 border-t-primary">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl text-center">Create an account</CardTitle>
                    <CardDescription className="text-center">
                        Enter your information to get started with CredBud
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                        <Input
                            label="Full Name"
                            placeholder="John Doe"
                            error={errors.full_name?.message}
                            {...register('full_name', { required: 'Full Name is required' })}
                        />
                        <Input
                            label="Email"
                            type="email"
                            placeholder="name@example.com"
                            error={errors.email?.message}
                            {...register('email', {
                                required: 'Email is required',
                                pattern: {
                                    value: /^\S+@\S+$/i,
                                    message: 'Invalid email address'
                                }
                            })}
                        />
                        <Input
                            label="Phone Number"
                            placeholder="10-digit mobile number"
                            error={errors.phone?.message}
                            {...register('phone', {
                                required: 'Phone Number is required',
                                pattern: { value: /^[0-9]{10}$/, message: 'Must be 10 digits' }
                            })}
                        />
                        <Select
                            label="City Tier"
                            options={cityTierOptions}
                            error={errors.city_tier?.message}
                            {...register('city_tier', { required: 'City Tier is required' })}
                        />
                        <Input
                            label="Password"
                            type="password"
                            placeholder="••••••••"
                            error={errors.password?.message}
                            {...register('password', {
                                required: 'Password is required',
                                minLength: { value: 8, message: 'Password must be at least 8 characters' }
                            })}
                        />
                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            isLoading={isLoading}
                        >
                            Create Account
                        </Button>
                    </form>
                    <div className="mt-6 text-center text-sm text-gray-500">
                        Already have an account?{' '}
                        <Link to="/login" className="font-semibold text-primary hover:underline decoration-2 underline-offset-4">
                            Sign in
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default Register;
