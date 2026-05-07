# CardioPredict 💓
### AI-Powered Cardiovascular Risk Assessment Platform

> A production-grade heart disease prediction system using an ensemble of Machine Learning algorithms — Logistic Regression, Random Forest, and SVM — with a futuristic glassmorphism web interface.

---

## 🚀 Live Demo

```
python run.py
```
Open → **http://localhost:5000**

---

## 📸 Features

| Feature | Description |
|---|---|
| 🔬 **AI Prediction** | 13-parameter clinical form → instant risk score |
| ⚡ **Risk Gauge** | Animated 0–100% cardiovascular risk meter |
| 🤖 **3 ML Models** | Logistic Regression · Random Forest · SVM |
| 📊 **Model Comparison** | Accuracy · Precision · Recall · F1 · AUC charts |
| 🌲 **Feature Importance** | Random Forest feature contribution analysis |
| 📈 **Confusion Matrices** | Per-model performance visualization |
| 📄 **PDF Reports** | Professional medical reports (auto-generated) |
| 🗂️ **Patient History** | SQLite database with searchable records |
| 💊 **Health Recommendations** | Risk-band personalized clinical guidance |
| 🖥️ **6-Page Dashboard** | Full glassmorphism dark-mode UI |

---

## 🧠 Machine Learning Pipeline

```
heart.csv (1000 rows, 13 features)
        ↓
  Data Cleaning (median imputation, deduplication)
        ↓
  Feature Engineering (one-hot encoding + StandardScaler)
        ↓
  80% Train / 20% Test Split (stratified)
        ↓
  ┌─────────────────────────────────────┐
  │  Logistic Regression  (C=1.0)       │ → Accuracy, F1, AUC
  │  Random Forest        (100 trees)   │ → Feature Importance
  │  SVM                  (RBF kernel)  │ → Confusion Matrix
  └─────────────────────────────────────┘
        ↓
  Random Forest = Final Prediction Engine
        ↓
  Risk Score = predict_proba × 100
        ↓
  PDF Report + Patient Record Saved
```

### Model Performance

| Model | Accuracy | F1 Score | AUC |
|---|---|---|---|
| Logistic Regression | ~85% | ~91% | ~89% |
| **Random Forest** ⭐ | ~84% | ~90% | ~87% |
| SVM | ~82% | ~90% | ~84% |

---

## 📁 Project Structure

```
Disease Prediction (Heart Disease)/
│
├── run.py                          # Entry point — run this!
├── requirements.txt
├── README.md
│
├── backend/
│   ├── app.py                      # Flask REST API (9 endpoints)
│   ├── data/
│   │   ├── heart_generator.py      # Synthetic dataset generator
│   │   ├── preprocessor.py         # Feature engineering + scaling
│   │   └── heart.csv               # Generated on first run
│   ├── ml/
│   │   ├── pipeline.py             # Model training + chart generation
│   │   ├── predictor.py            # Inference engine + recommendations
│   │   └── models/                 # Saved .pkl files + results.json
│   ├── db/
│   │   └── database.py             # SQLite patient history (SQLAlchemy)
│   └── reports/
│       └── pdf_generator.py        # ReportLab PDF medical reports
│
└── frontend/
    ├── index.html                  # Landing page
    ├── dashboard.html              # Prediction dashboard
    ├── comparison.html             # Model comparison
    ├── analytics.html              # Visualizations
    ├── report.html                 # Patient history + PDF
    ├── about.html                  # Project info + Viva Q&A
    ├── css/
    │   ├── globals.css             # Design tokens + reset
    │   ├── animations.css          # All keyframe animations
    │   ├── components.css          # UI component library
    │   └── pages.css               # Page-specific styles
    └── js/
        ├── api.js                  # Flask API client
        ├── nav.js                  # Navigation + utilities
        ├── dashboard.js            # Prediction form logic
        ├── comparison.js           # Chart.js model charts
        ├── analytics.js            # Confusion matrix + distributions
        └── report.js               # Patient history table
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- pip

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Start the Application

```bash
python run.py
```

**First run** (~30 seconds):
- ✅ Initializes SQLite database
- ✅ Generates 1000-row heart disease dataset
- ✅ Trains Logistic Regression, Random Forest, SVM
- ✅ Saves models as `.pkl` files
- ✅ Starts Flask server on port 5000

**Subsequent runs:** Instant (models cached).

### Step 3 — Open Browser

```
http://localhost:5000
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Server health check |
| `POST` | `/api/predict` | Run all models → risk score |
| `GET` | `/api/models/accuracy` | All model metrics |
| `GET` | `/api/models/confusion` | Confusion matrix images (base64) |
| `GET` | `/api/models/feature-importance` | RF importance + ROC curve |
| `GET` | `/api/patients` | All patient history records |
| `POST` | `/api/patients` | Save patient record |
| `GET` | `/api/report/<id>` | Download PDF report |
| `POST` | `/api/train` | Re-train all models |

### Example Prediction Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "age": 55, "sex": 1, "cp": 3,
    "trestbps": 145, "chol": 310, "fbs": 1,
    "restecg": 1, "thalach": 128, "exang": 1,
    "oldpeak": 2.3, "slope": 1, "ca": 1, "thal": 3
  }'
```

### Example Response

```json
{
  "success": true,
  "data": {
    "prediction": 1,
    "prediction_label": "Heart Disease Detected",
    "risk_score": 87.4,
    "risk_label": "Critical Risk",
    "risk_color": "#ff2d55",
    "per_model": {
      "Logistic Regression": { "probability": 82.1, "prediction": 1 },
      "Random Forest":       { "probability": 87.4, "prediction": 1 },
      "SVM":                 { "probability": 79.6, "prediction": 1 }
    },
    "recommendations": ["...", "..."],
    "patient_id": 1
  }
}
```

---

## 🩺 Input Parameters

| Parameter | Description | Range |
|---|---|---|
| `age` | Age in years | 29–77 |
| `sex` | 1=Male, 0=Female | 0 or 1 |
| `cp` | Chest pain type | 0–3 |
| `trestbps` | Resting blood pressure (mmHg) | 94–200 |
| `chol` | Serum cholesterol (mg/dl) | 126–564 |
| `fbs` | Fasting blood sugar >120 mg/dl | 0 or 1 |
| `restecg` | Resting ECG results | 0–2 |
| `thalach` | Max heart rate achieved (bpm) | 71–202 |
| `exang` | Exercise-induced angina | 0 or 1 |
| `oldpeak` | ST depression (exercise vs rest) | 0.0–6.2 |
| `slope` | Slope of peak exercise ST | 0–2 |
| `ca` | Major vessels colored by fluoroscopy | 0–3 |
| `thal` | Thalassemia type | 1–3 |

---

## 💊 Risk Band Classification

| Risk Score | Band | Recommendations |
|---|---|---|
| 0–30% | 🟢 Low Risk | Maintain lifestyle, annual checkups |
| 31–60% | 🟡 Moderate Risk | Dietary changes, reduce smoking |
| 61–80% | 🟠 High Risk | Consult cardiologist, stress test |
| 81–100% | 🔴 Critical Risk | Immediate medical evaluation |

---

## 🎨 Design System

- **Font:** Orbitron (display) + Inter (body)
- **Background:** `#050b1f` (deep space dark)
- **Accent Blue:** `#00d4ff` (neon cyan)
- **Accent Red:** `#ff2d55` (neon red)
- **Style:** Glassmorphism + `backdrop-filter: blur(16px)`
- **Charts:** Chart.js 4.x (frontend) + Matplotlib/Seaborn (backend)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask 3.x, Flask-CORS |
| Machine Learning | scikit-learn (LR, RF, SVM), joblib |
| Data Processing | pandas, NumPy |
| Visualization | matplotlib, seaborn |
| PDF Generation | ReportLab |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | Vanilla HTML5 / CSS3 / JavaScript (ES6+) |
| Charts | Chart.js 4.4 |

---

## 📝 Resume Description

> **CardioPredict** — AI-Powered Cardiovascular Risk Assessment Platform
> Built a production-grade heart disease prediction system using an ensemble ML pipeline (Logistic Regression, Random Forest, SVM) trained on the UCI Heart Disease dataset. Developed a Flask REST API backend serving real-time probabilistic risk scores with a glassmorphism-themed, animated frontend dashboard. Features include multi-model accuracy comparison, PDF medical report generation, patient history persistence (SQLite), confusion matrix visualization, and personalized health recommendations based on risk bands. Achieved 85%+ classification accuracy with Random Forest as the final inference engine.
> **Stack:** Python · Flask · scikit-learn · SQLite · ReportLab · Chart.js · HTML/CSS/JS

---

## 🎓 Viva Q&A Summary

**Q: Why Random Forest as the final model?**
A: Handles non-linear feature interactions, robust to outliers, provides feature importance, reduces overfitting via bagging.

**Q: How did you prevent data leakage?**
A: StandardScaler was fit exclusively on the training set and only transformed (not re-fit) on the test set.

**Q: What does AUC measure?**
A: Area Under the ROC Curve — measures model discrimination ability across all thresholds; 1.0 = perfect, 0.5 = random.

**Q: Why is Recall important in medical ML?**
A: Minimizing False Negatives (missed diagnoses) is critical — failing to detect heart disease is more dangerous than a false alarm.

---

## ⚠️ Disclaimer

> This application is built for **educational and research purposes only**. It does not constitute a medical diagnosis. Always consult a qualified healthcare professional for clinical decisions.

---

*CardioPredict © 2026 — Built with Python, Flask, scikit-learn, and Chart.js*
