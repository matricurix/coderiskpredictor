import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from utils import extract_features

def prepare_dataset(csv_path):
    """Load and prepare dataset"""
    df = pd.read_csv(csv_path)
    
    # Extract features for each code sample
    features_list = []
    labels = []
    
    print("Extracting features from code samples...")
    for idx, row in df.iterrows():
        features = extract_features(row['code'])
        if features:
            features_list.append(features)
            labels.append(row['has_smell'])
        
        if idx % 50 == 0:
            print(f"Processed {idx}/{len(df)} samples")
    
    # Convert to DataFrame
    X = pd.DataFrame(features_list)
    y = np.array(labels)
    
    print(f"\nDataset shape: {X.shape}")
    print(f"Positive samples (has smell): {sum(y)}")
    print(f"Negative samples (clean code): {len(y) - sum(y)}")
    
    return X, y

def train_model(X, y):
    """Train ML model"""
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("\nTraining Random Forest model...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_acc = rf_model.score(X_train_scaled, y_train)
    test_acc = rf_model.score(X_test_scaled, y_test)
    
    print(f"Training Accuracy: {train_acc:.4f}")
    print(f"Testing Accuracy: {test_acc:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Important Features:")
    print(feature_importance.head())
    
    # Save model and scaler
    joblib.dump(rf_model, 'ml_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("\nModel saved as 'ml_model.pkl'")
    
    return rf_model, scaler

if __name__ == "__main__":
    # Load and prepare data
    X, y = prepare_dataset('data/code_samples.csv')
    
    # Train model
    model, scaler = train_model(X, y)
    
    print("\n✅ Model training complete!")