"""
CardioPredict — Inference Engine
Loads saved models and runs predictions on patient input.
"""
import os
import sys
import json
import numpy as np
import joblib

MODELS_DIR   = os.path.join(os.path.dirname(__file__), 'models')
RESULTS_JSON = os.path.join(MODELS_DIR, 'results.json')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.data.preprocessor import preprocess_input

MODEL_FILES = {
    'Logistic Regression': 'logistic_regression.pkl',
    'Random Forest':       'random_forest.pkl',
    'SVM':                 'svm.pkl',
}

RECOMMENDATIONS = {
    'low': [
        "Maintain your current healthy lifestyle — you're doing great!",
        "Schedule routine annual cardiovascular checkups.",
        "Continue regular moderate exercise (150+ min/week).",
        "Maintain a balanced diet rich in fruits and vegetables.",
        "Monitor blood pressure and cholesterol yearly.",
    ],
    'moderate': [
        "Consult your physician for a full cardiovascular evaluation.",
        "Reduce sodium intake to lower blood pressure.",
        "Adopt a Mediterranean-style diet (olive oil, fish, whole grains).",
        "Quit smoking immediately — it doubles cardiovascular risk.",
        "Increase aerobic activity gradually (start with 30 min walks).",
        "Consider stress-reduction techniques: yoga, meditation.",
        "Monitor fasting blood sugar every 6 months.",
    ],
    'high': [
        "⚠️ Schedule an urgent cardiology consultation.",
        "Request an ECG, echocardiogram, and stress test.",
        "Review all current medications with your doctor.",
        "Strict dietary control: eliminate processed foods and trans fats.",
        "Absolute cessation of smoking and alcohol.",
        "Daily blood pressure monitoring at home.",
        "Consider cardiac rehabilitation program enrollment.",
    ],
    'critical': [
        "🚨 Seek immediate medical evaluation — do not delay.",
        "Emergency cardiology consultation is strongly recommended.",
        "Do not perform strenuous physical activity until cleared.",
        "Continuous cardiac monitoring may be required.",
        "Discuss advanced interventions (angiography, stenting) with cardiologist.",
        "Have a family member or companion available at all times.",
    ],
}


def get_risk_band(risk_pct):
    if risk_pct < 30:
        return 'low',      'Low Risk',      '#00ff88'
    elif risk_pct < 60:
        return 'moderate', 'Moderate Risk', '#ffd60a'
    elif risk_pct < 80:
        return 'high',     'High Risk',     '#ff9500'
    else:
        return 'critical', 'Critical Risk', '#ff2d55'


def predict(patient_dict):
    """
    patient_dict keys: age, sex, cp, trestbps, chol, fbs, restecg,
                       thalach, exang, oldpeak, slope, ca, thal
    Returns: prediction dict
    """
    X = preprocess_input(patient_dict)

    per_model = {}
    rf_prob   = None

    for name, filename in MODEL_FILES.items():
        path = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model not found: {path}. Run pipeline.py first."
            )
        clf = joblib.load(path)
        prob = float(clf.predict_proba(X)[0][1])
        pred = int(clf.predict(X)[0])
        per_model[name] = {
            'probability': round(prob * 100, 1),
            'prediction':  pred,
            'label':       'Heart Disease Detected' if pred == 1 else 'No Heart Disease',
        }
        if name == 'Random Forest':
            rf_prob = prob

    risk_pct = round(rf_prob * 100, 1)
    band_key, band_label, band_color = get_risk_band(risk_pct)
    final_pred = 1 if rf_prob >= 0.5 else 0

    # Load best model from results
    best_model = 'Random Forest'
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON) as f:
            results = json.load(f)
        metrics = results.get('metrics', {})
        best_model = max(metrics, key=lambda k: metrics[k]['accuracy'])

    return {
        'prediction':     final_pred,
        'prediction_label': 'Heart Disease Detected' if final_pred == 1 else 'No Heart Disease',
        'risk_score':     risk_pct,
        'risk_band':      band_key,
        'risk_label':     band_label,
        'risk_color':     band_color,
        'per_model':      per_model,
        'best_model':     best_model,
        'recommendations': RECOMMENDATIONS[band_key],
    }


def get_results():
    """Return saved training metrics and chart images."""
    if not os.path.exists(RESULTS_JSON):
        return None
    with open(RESULTS_JSON) as f:
        return json.load(f)
