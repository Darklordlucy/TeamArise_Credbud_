"""
Credit Score Model - KNN Classifier
Trained model for predicting loan approval based on financial parameters
"""

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Dict, Tuple
import os
import joblib

class CreditScoreModel:
    def __init__(self, model_path: str = None, scaler_path: str = None):
        """
        Initialize Credit Score Model
        
        Args:
            model_path: Path to saved KNN model (.pkl)
            scaler_path: Path to saved StandardScaler (.pkl)
        """
        self.model_path = model_path or './app/ml/models/knn_model.pkl'
        self.scaler_path = scaler_path or './app/ml/models/scaler.pkl'
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained KNN model and scaler"""
        try:
            # Try to load existing model
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("✓ Loaded trained KNN model and scaler")
            else:
                print("⚠ Warning: Model files not found. Please train the model first.")
                print(f"Expected model at: {self.model_path}")
                print(f"Expected scaler at: {self.scaler_path}")
                # Create dummy model for development (will be replaced by trained model)
                self._create_dummy_model()
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for development/testing purposes"""
        print("Creating dummy model for development...")
        self.model = KNeighborsClassifier(n_neighbors=6, metric='minkowski', p=2)
        self.scaler = StandardScaler()
        
        # Train with dummy data (6 features)
        X_dummy = np.random.rand(100, 6)
        y_dummy = np.random.randint(0, 2, 100)
        
        X_dummy_scaled = self.scaler.fit_transform(X_dummy)
        self.model.fit(X_dummy_scaled, y_dummy)
    
    def predict(self, features: Dict) -> Tuple[float, float]:
        """
        Predict credit score and acceptance rate
        
        Args:
            features: Dictionary containing:
                - num_debts: Number of existing debts
                - total_debt_amount: Total debt amount
                - monthly_emis: Monthly EMI payments
                - total_assets: Total assets value
                - monthly_income: Monthly income
                - city_tier: City tier (tier_1, tier_2, tier_3)
        
        Returns:
            Tuple of (ml_score, acceptance_rate)
        """
        try:
            # Extract and prepare features in correct order
            # Order matches training data: [num_debts, total_debt_amount, monthly_emis, 
            #                               total_assets, monthly_income, city_tier_encoded]
            city_tier_mapping = {'tier_1': 1, 'tier_2': 2, 'tier_3': 3}
            
            X = np.array([[
                features['num_debts'],
                features['total_debt_amount'],
                features['monthly_emis'],
                features['total_assets'],
                features['monthly_income'],
                city_tier_mapping.get(features['city_tier'], 2)
            ]])
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Get prediction probability from KNN model
            proba = self.model.predict_proba(X_scaled)[0]
            
            # ML Score (0-100) - probability of approval class
            ml_score = proba[1] * 100  # Probability of class 1 (approved)
            
            # Calculate acceptance rate based on ML score + financial ratios
            acceptance_rate = self._calculate_acceptance_rate(features, ml_score)
            
            return round(ml_score, 2), round(acceptance_rate, 2)
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            # Return conservative estimates on error
            return 50.0, 50.0
    
    def _calculate_acceptance_rate(self, features: Dict, ml_score: float) -> float:
        """
        Calculate final acceptance rate by combining ML score with financial ratios
        
        Args:
            features: User's financial features
            ml_score: Base ML model score
        
        Returns:
            Final acceptance rate (10-95%)
        """
        # Start with ML score
        acceptance_rate = ml_score
        
        # Calculate financial health indicators
        monthly_income = max(features['monthly_income'], 1)  # Avoid division by zero
        annual_income = monthly_income * 12
        total_debt = max(features['total_debt_amount'], 0)
        
        # 1. Debt-to-Income Ratio (DTI)
        debt_to_income = total_debt / annual_income if annual_income > 0 else 1
        if debt_to_income > 0.5:  # High debt burden
            acceptance_rate -= 15
        elif debt_to_income > 0.3:  # Moderate debt burden
            acceptance_rate -= 8
        elif debt_to_income < 0.2:  # Low debt burden
            acceptance_rate += 5
        
        # 2. EMI-to-Income Ratio
        emi_to_income = features['monthly_emis'] / monthly_income if monthly_income > 0 else 1
        if emi_to_income > 0.5:  # Very high EMI burden
            acceptance_rate -= 20
        elif emi_to_income > 0.4:  # High EMI burden
            acceptance_rate -= 12
        elif emi_to_income < 0.25:  # Manageable EMI
            acceptance_rate += 5
        
        # 3. Asset-to-Debt Ratio
        if total_debt > 0:
            asset_ratio = features['total_assets'] / total_debt
            if asset_ratio > 2.0:  # Strong asset backing
                acceptance_rate += 15
            elif asset_ratio > 1.5:  # Good asset backing
                acceptance_rate += 10
            elif asset_ratio < 0.5:  # Weak asset backing
                acceptance_rate -= 10
        elif features['total_assets'] > 0:
            # No debt but has assets
            acceptance_rate += 10
        
        # 4. Number of existing debts penalty
        if features['num_debts'] > 5:
            acceptance_rate -= 12
        elif features['num_debts'] > 3:
            acceptance_rate -= 6
        elif features['num_debts'] == 0:
            acceptance_rate += 5
        
        # 5. City tier adjustment (cost of living)
        if features.get('city_tier') == 'tier_1':
            # Higher income needed in metro cities
            if monthly_income < 30000:
                acceptance_rate -= 5
        elif features.get('city_tier') == 'tier_3':
            # Lower cost of living
            acceptance_rate += 3
            
        # 6. Loan-to-Income (LTI) Ratio
        amount_requested = features.get('amount_requested', 0)
        if amount_requested > 0:
            lti_ratio = amount_requested / annual_income if annual_income > 0 else 10
            if lti_ratio > 5:  # Very high loan amount relative to income
                acceptance_rate -= 20
            elif lti_ratio > 3:  # High loan amount
                acceptance_rate -= 10
            elif lti_ratio < 1.5:  # Conservative loan amount
                acceptance_rate += 5
                
        # 7. Loan-to-Asset (LTA) Ratio
        total_assets = max(features.get('total_assets', 0), 0)
        if total_assets > 0 and amount_requested > 0:
            lta_ratio = amount_requested / total_assets
            if lta_ratio > 1.5:  # Loan exceed assets significantly
                acceptance_rate -= 15
            elif lta_ratio < 0.5:  # Strong collateral/asset backing
                acceptance_rate += 10
        
        # Ensure bounds [10, 95]
        acceptance_rate = max(10, min(95, acceptance_rate))
        
        return acceptance_rate
    
    def save_model(self, model_path: str = None, scaler_path: str = None):
        """
        Save trained model and scaler to disk
        
        Args:
            model_path: Path to save KNN model
            scaler_path: Path to save StandardScaler
        """
        model_path = model_path or self.model_path
        scaler_path = scaler_path or self.scaler_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"✓ Model saved to {model_path}")
            print(f"✓ Scaler saved to {scaler_path}")
        except Exception as e:
            print(f"✗ Error saving model: {str(e)}")
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_type': 'KNeighborsClassifier',
            'n_neighbors': self.model.n_neighbors if hasattr(self.model, 'n_neighbors') else None,
            'metric': self.model.metric if hasattr(self.model, 'metric') else None,
            'model_loaded': self.model is not None,
            'scaler_loaded': self.scaler is not None,
            'model_path': self.model_path,
            'scaler_path': self.scaler_path
        }


# Create global instance
credit_model = CreditScoreModel()
