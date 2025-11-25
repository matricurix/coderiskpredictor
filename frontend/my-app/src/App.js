import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import './App.css';

function App() {
  const [code, setCode] = useState(`def calculate_total(a, b, c, d, e, f, g, h):
    result = 0
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    result = a + b + c + d + e + f + g + h
    return result

class UserManager:
    def __init__(self):
        self.users = []
        
    def create_user(self, name, email, password, age, country, city, zipcode, phone):
        pass
    
    def update_user(self): pass
    def delete_user(self): pass
    def validate_user(self): pass
    def send_email(self): pass
    def log_activity(self): pass
    def calculate_metrics(self): pass
    def generate_report(self): pass
    def export_data(self): pass
    def import_data(self): pass
    def sync_database(self): pass
    def backup_data(self): pass

def process_data(data):
    x = 500
    temp = data * x
    if temp > 500:
        return temp * 2
    else:
        return temp / 2`);

  const [smells, setSmells] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [mlPrediction, setMlPrediction] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  const analyzeCode = async () => {
    setAnalyzing(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          language: 'python'
        })
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setSmells(data.smells);
      setMetrics(data.metrics);
      setMlPrediction(data.ml_prediction);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return 'severity-info';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🔵';
      default: return '✅';
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🔍 ML-Based Code Smell Detector</h1>
          <p>AI-Powered Code Quality Analysis Tool</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-container">
        {/* Left Panel - Editor */}
        <div className="editor-panel">
          <div className="panel-header">
            <h2>📝 Python Code Editor</h2>
            <button 
              onClick={analyzeCode}
              disabled={analyzing}
              className="analyze-button"
            >
              {analyzing ? '⏳ Analyzing...' : '⚡ Analyze Code'}
            </button>
          </div>
          <div className="editor-container">
            <Editor
              height="500px"
              defaultLanguage="python"
              value={code}
              onChange={setCode}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
              }}
            />
          </div>
        </div>

        {/* Right Panel - Results */}
        <div className="results-panel">
          <div className="panel-header">
            <h2>🎯 Analysis Results</h2>
            {smells.length > 0 && (
              <span className="smell-count">{smells.length} Issues Found</span>
            )}
          </div>

          {error && (
            <div className="error-message">
              ❌ Error: {error}
            </div>
          )}

          {/* ML Prediction */}
          {mlPrediction && (
            <div className="ml-prediction">
              <h3>🤖 ML Model Prediction</h3>
              <div className="prediction-content">
                <div className="prediction-status">
                  {mlPrediction.has_smell ? (
                    <>
                      <span className="status-badge smell">Code Smell Detected</span>
                      <span className="confidence">
                        Confidence: {(mlPrediction.confidence * 100).toFixed(1)}%
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="status-badge clean">Clean Code</span>
                      <span className="confidence">
                        Confidence: {(mlPrediction.confidence * 100).toFixed(1)}%
                      </span>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Detected Smells */}
          <div className="smells-container">
            {smells.length === 0 && !analyzing && (
              <div className="no-smells">
                <div className="no-smells-icon">✨</div>
                <p>No code smells detected!</p>
                <small>Click "Analyze Code" to scan your code</small>
              </div>
            )}

            {smells.map((smell, idx) => (
              <div key={idx} className={`smell-card ${getSeverityColor(smell.severity)}`}>
                <div className="smell-header">
                  <span className="smell-icon">{getSeverityIcon(smell.severity)}</span>
                  <div className="smell-title">
                    <h4>{smell.smell_type}</h4>
                    <span className="smell-meta">
                      Line {smell.line_number} • {smell.detector}
                    </span>
                  </div>
                </div>
                <p className="smell-description">{smell.description}</p>
                <div className="smell-suggestion">
                  <strong>💡 Suggestion:</strong> {smell.suggestion}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Metrics Dashboard */}
      {metrics && (
        <div className="metrics-section">
          <h2>📊 Code Metrics</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">{metrics.lines}</div>
              <div className="metric-label">Lines of Code</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{metrics.functions}</div>
              <div className="metric-label">Functions</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{metrics.classes}</div>
              <div className="metric-label">Classes</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{metrics.complexity}</div>
              <div className="metric-label">Complexity</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{metrics.avg_method_length}</div>
              <div className="metric-label">Avg Method Length</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{metrics.max_nesting_depth}</div>
              <div className="metric-label">Max Nesting</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;