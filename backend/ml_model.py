import joblib
import pandas as pd
from utils import extract_features

class MLDetector:
    """ML-based code smell detection"""
    
    def __init__(self):
        """Load trained model and scaler"""
        try:
            self.model = joblib.load('ml_model.pkl')
            self.scaler = joblib.load('scaler.pkl')
            print("✅ ML model loaded successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not load ML model: {e}")
            self.model = None
            self.scaler = None
    
    def predict(self, code):
        """Predict if code has smells using ML model"""
        if self.model is None:
            return {
                'has_smell': False,
                'confidence': 0.0,
                'features': None
            }
        
        try:
            # Extract features
            features = extract_features(code)
            if features is None:
                return {
                    'has_smell': False,
                    'confidence': 0.0,
                    'features': None,
                    'error': 'Failed to extract features'
                }
            
            # Convert to DataFrame
            feature_df = pd.DataFrame([features])
            
            # Scale features
            features_scaled = self.scaler.transform(feature_df)
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            
            # Get prediction probability
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = probabilities[prediction]
            
            return {
                'has_smell': bool(prediction),
                'confidence': float(confidence),
                'features': features,
                'probabilities': {
                    'clean': float(probabilities[0]),
                    'smell': float(probabilities[1])
                }
            }
            
        except Exception as e:
            print(f"Error in ML prediction: {e}")
            return {
                'has_smell': False,
                'confidence': 0.0,
                'features': None,
                'error': str(e)
            }
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        if self.model is None:
            return None
        
        try:
            feature_names = [
                'num_lines', 'num_functions', 'num_classes', 'num_loops',
                'num_ifs', 'num_returns', 'max_params', 'avg_params',
                'max_depth', 'complexity', 'num_comments', 'avg_line_length',
                'empty_lines', 'indentation_levels', 'code_density'
            ]
            
            importances = self.model.feature_importances_
            
            return {
                name: float(importance)
                for name, importance in zip(feature_names, importances)
            }
        except:
            return None