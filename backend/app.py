from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import List, Dict
from detector import RuleBasedDetector
from ml_model import MLDetector
from utils import extract_features

app = FastAPI(title="Code Smell Detector API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model and detectors on startup
ml_detector = MLDetector()
rule_detector = RuleBasedDetector()

# Pydantic models for request/response
class CodeInput(BaseModel):
    code: str
    language: str = "python"

class SmellResult(BaseModel):
    smell_type: str
    severity: str
    line_number: int
    description: str
    suggestion: str
    detector: str  # "rule-based" or "ml"

class AnalysisResponse(BaseModel):
    smells: List[SmellResult]
    metrics: Dict
    ml_prediction: Dict

@app.get("/")
async def root():
    return {
        "message": "Code Smell Detector API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/health"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ml_model_loaded": ml_detector.model is not None
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(input: CodeInput):
    """Main endpoint to analyze code for smells"""
    try:
        if not input.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        # Run rule-based detection
        rule_smells = rule_detector.detect_all(input.code)
        
        # Run ML-based detection
        ml_result = ml_detector.predict(input.code)
        
        # Combine results
        all_smells = []
        
        # Add rule-based smells
        for smell in rule_smells:
            all_smells.append(SmellResult(
                smell_type=smell['type'],
                severity=smell['severity'],
                line_number=smell['line'],
                description=smell['description'],
                suggestion=smell['suggestion'],
                detector="rule-based"
            ))
        
        # Add ML prediction as a smell if detected
        if ml_result['has_smell']:
            all_smells.append(SmellResult(
                smell_type="ML Detected Smell",
                severity="medium",
                line_number=1,
                description=f"ML model detected potential code smell with {ml_result['confidence']:.1%} confidence",
                suggestion="Review the code structure and consider refactoring based on rule-based suggestions",
                detector="ml"
            ))
        
        # Calculate metrics
        metrics = calculate_code_metrics(input.code)
        
        # Remove duplicates by (type, line)
        unique_smells = {}
        for smell in all_smells:
            key = (smell.smell_type, smell.line_number)
            if key not in unique_smells:
                unique_smells[key] = smell
        
        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        sorted_smells = sorted(
            unique_smells.values(),
            key=lambda x: severity_order.get(x.severity, 3)
        )
        
        return AnalysisResponse(
            smells=sorted_smells,
            metrics=metrics,
            ml_prediction=ml_result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_code_metrics(code: str) -> Dict:
    """Calculate various code metrics"""
    features = extract_features(code)
    
    if features is None:
        return {
            "lines": 0,
            "functions": 0,
            "classes": 0,
            "complexity": 0,
            "avg_method_length": 0,
            "comment_ratio": 0
        }
    
    lines = code.split('\n')
    num_lines = len([l for l in lines if l.strip()])
    
    comment_ratio = (features['num_comments'] / max(num_lines, 1)) * 100
    avg_method_length = num_lines / max(features['num_functions'], 1)
    
    return {
        "lines": num_lines,
        "functions": features['num_functions'],
        "classes": features['num_classes'],
        "complexity": features['complexity'],
        "avg_method_length": round(avg_method_length, 1),
        "comment_ratio": round(comment_ratio, 1),
        "max_nesting_depth": features['max_depth'],
        "max_parameters": features['max_params']
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Code Smell Detector API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)