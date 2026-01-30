"""
Train KNN Credit Score Model
This script trains the KNN classifier and saves the model and scaler
Run this script once to generate the model files before starting the backend
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Configuration
DATA_PATH = 'D:/TeamArise(windsirf)/credit-decision-backend/data/data.csv'  # Path to your training data
MODEL_SAVE_PATH = 'D:/TeamArise(windsirf)/credit-decision-backend/app/ml/models/knn_model.pkl'
SCALER_SAVE_PATH = 'D:/TeamArise(windsirf)/credit-decision-backend/app/ml/models/scaler.pkl'
LABEL_ENCODER_SAVE_PATH = 'D:/TeamArise(windsirf)/credit-decision-backend/app/ml/models/label_encoder.pkl'

def train_model():
    """Train the KNN credit score model"""
    
    print("="*60)
    print("TRAINING KNN CREDIT SCORE MODEL")
    print("="*60)
    
    # 1. Load Dataset
    print("\n1. Loading dataset...")
    try:
        dataset = pd.read_csv(DATA_PATH)
        print(f"   ✓ Dataset loaded: {dataset.shape[0]} rows, {dataset.shape[1]} columns")
        print(f"\n   Dataset Info:")
        dataset.info()
    except FileNotFoundError:
        print(f"   ✗ Error: Dataset not found at {DATA_PATH}")
        print(f"   Please ensure data.csv is in the ./data/ directory")
        return
    
    # 2. Prepare Features and Target
    print("\n2. Preparing features and target...")
    X = dataset.iloc[:, :-1].values  # All columns except last
    y = dataset.iloc[:, -1].values   # Last column (target)
    
    print(f"   Features shape: {X.shape}")
    print(f"   Target shape: {y.shape}")
    
    # 3. Encode Target Variable
    print("\n3. Encoding target variable...")
    # Ensure y is string to avoid issues with boolean interpretation
    y = y.astype(str)
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    print(f"   Classes: {le.classes_}")
    print(f"   Encoded values: {np.unique(y_encoded)}")
    
    # 4. Split Dataset
    print("\n4. Splitting dataset (80% train, 20% test)...")
    # Identify stratify parameter might cause issues if classes are too small
    stratify_param = y_encoded if len(np.unique(y_encoded)) > 1 and np.min(np.bincount(y_encoded)) > 1 else None
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=stratify_param
    )
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Test set: {X_test.shape[0]} samples")
    
    # 5. Feature Scaling
    print("\n5. Scaling features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   ✓ Features scaled")
    
    # 6. Train KNN Classifier
    print("\n6. Training KNN Classifier...")
    classifier = KNeighborsClassifier(
        n_neighbors=6,
        metric='minkowski',
        p=2
    )
    classifier.fit(X_train_scaled, y_train)
    print("   ✓ Model trained")
    
    # 7. Evaluate Model
    print("\n7. Evaluating model...")
    y_pred = classifier.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n   Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\n   Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\n   Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # 8. Save Model and Scaler
    print("\n8. Saving model and scaler...")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    try:
        # Save KNN model
        with open(MODEL_SAVE_PATH, 'wb') as f:
            pickle.dump(classifier, f)
        print(f"   ✓ Model saved to: {MODEL_SAVE_PATH}")
        
        # Save scaler
        with open(SCALER_SAVE_PATH, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"   ✓ Scaler saved to: {SCALER_SAVE_PATH}")
        
        # Save label encoder (optional, for reference)
        with open(LABEL_ENCODER_SAVE_PATH, 'wb') as f:
            pickle.dump(le, f)
        print(f"   ✓ Label encoder saved to: {LABEL_ENCODER_SAVE_PATH}")
        
    except Exception as e:
        print(f"   ✗ Error saving files: {str(e)}")
        return
    
    # 9. Test Saved Model
    print("\n9. Testing saved model...")
    try:
        with open(MODEL_SAVE_PATH, 'rb') as f:
            loaded_model = pickle.load(f)
        with open(SCALER_SAVE_PATH, 'rb') as f:
            loaded_scaler = pickle.load(f)
        
        # Make a test prediction
        test_sample = X_test_scaled[0:1]
        prediction = loaded_model.predict(test_sample)
        probability = loaded_model.predict_proba(test_sample)
        
        print(f"   ✓ Model loaded successfully")
        print(f"   Test prediction: {le.classes_[prediction[0]]}")
        print(f"   Prediction probability: {probability[0]}")
        
    except Exception as e:
        print(f"   ✗ Error testing saved model: {str(e)}")
        return
    
    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Copy the trained model files to your backend:")
    print(f"   - {MODEL_SAVE_PATH}")
    print(f"   - {SCALER_SAVE_PATH}")
    print("2. Start your FastAPI backend")
    print("3. The model will be automatically loaded")
    print("\n" + "="*60)


def test_prediction():
    """Test the model with sample data"""
    print("\n" + "="*60)
    print("TESTING MODEL WITH SAMPLE DATA")
    print("="*60)
    
    try:
        # Load model and scaler
        with open(MODEL_SAVE_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_SAVE_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        # Sample loan application data
        # [num_debts, total_debt_amount, monthly_emis, total_assets, monthly_income, city_tier]
        sample_data = np.array([
            [2, 50000, 5000, 200000, 50000, 1],  # Good candidate
            [5, 150000, 15000, 100000, 30000, 2],  # Risky candidate
            [0, 0, 0, 300000, 80000, 1]  # Excellent candidate
        ])
        
        # Scale data
        sample_scaled = scaler.transform(sample_data)
        
        # Predict
        predictions = model.predict(sample_scaled)
        probabilities = model.predict_proba(sample_scaled)
        
        print("\nSample Predictions:")
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            print(f"\nCandidate {i+1}:")
            print(f"  Input: {sample_data[i]}")
            print(f"  Prediction: {'Approved' if pred == 1 else 'Rejected'}")
            print(f"  Confidence: {prob[pred]*100:.2f}%")
            print(f"  Probabilities: [Rejected: {prob[0]*100:.1f}%, Approved: {prob[1]*100:.1f}%]")
        
    except Exception as e:
        print(f"Error testing predictions: {str(e)}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Train the model
    train_model()
    
    # Test with sample data
    test_prediction()
