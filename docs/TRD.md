# Technical Requirements Document (TRD)

**Product:** CardioPredict — AI-Powered Cardiovascular Risk Assessment Platform  
**Version:** 2.0  
**Date:** May 2026  
**Status:** ✅ Implemented  

---

## 1. System Overview

CardioPredict is a monolithic full-stack web application structured as a Flask REST API backend serving a Vanilla JS / HTML5 frontend. The system trains three scikit-learn classification models, persists patient records to SQLite via SQLAlchemy ORM, generates styled PDF reports via ReportLab, and delivers ML visualizations as server-rendered base64 PNG images.

### Architecture Diagram

```
Browser (Vanilla JS)
        │
        │  HTTP (REST JSON)
        ▼
Flask REST API  (app.py  — port 5000)
        │
        ├── ML Engine         (backend/ml/)
        │       ├── pipeline.py    → Train LR, RF, SVM → .pkl + results.json
        │       └── predictor.py   → Load .pkl → infer → risk score + recommendations
        │
        ├── Database Layer    (backend/db/)
        │       └── database.py    → SQLAlchemy ORM → SQLite (cardiopredict.db)
        │
        ├── Report Engine     (backend/reports/)
        │       └── pdf_generator.py → ReportLab → PDF bytes → HTTP response
        │
        └── Data Layer        (backend/data/)
                ├── heart_generator.py  → Synthetic 1000-row dataset
                └── preprocessor.py     → StandardScaler + one-hot + train/test split
```

---

## 2. Technology Stack

| Layer | Technology | Version |
|---|---|---|
| **Runtime** | Python | 3.11+ |
| **Web Framework** | Flask | 3.0.3 |
| **CORS** | Flask-CORS | 4.0.1 |
| **ML Library** | scikit-learn | 1.4.2 |
| **Model Serialization** | joblib | 1.4.2 |
| **Data Processing** | pandas | 2.2.2 |
| **Numerical Computing** | NumPy | 1.26.4 |
| **Backend Visualization** | Matplotlib | 3.8.4 |
| **Backend Visualization** | Seaborn | 0.13.2 |
| **PDF Generation** | ReportLab | 4.2.0 |
| **ORM** | SQLAlchemy | 2.0.30 |
| **Database** | SQLite | (bundled) |
| **Image Processing** | Pillow | 10.3.0 |
| **Frontend** | Vanilla HTML5 / CSS3 / ES6+ JS | — |
| **Frontend Charts** | Chart.js | 4.4 (CDN) |
| **Typography** | Google Fonts (Orbitron + Inter) | (CDN) |

---

## 3. Directory Structure

```
Disease Prediction (Heart Disease)/
│
├── run.py                         # Entry point
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── docs/
│   ├── PRD.md                     # Product Requirements Document
│   └── TRD.md                     # Technical Requirements Document
│
├── backend/
│   ├── app.py                     # Flask app — 9 REST endpoints
│   ├── data/
│   │   ├── heart_generator.py     # Synthetic dataset generator
│   │   ├── preprocessor.py        # Feature engineering + StandardScaler
│   │   └── heart.csv              # Generated on first run (1000 rows)
│   ├── ml/
│   │   ├── pipeline.py            # Training pipeline + chart generation
│   │   ├── predictor.py           # Inference engine + risk logic
│   │   └── models/
│   │       ├── logistic_regression.pkl
│   │       ├── random_forest.pkl
│   │       ├── svm.pkl
│   │       └── results.json       # Metrics + base64 chart images
│   ├── db/
│   │   ├── database.py            # SQLAlchemy models + CRUD
│   │   └── cardiopredict.db       # SQLite database file
│   └── reports/
│       └── pdf_generator.py       # ReportLab PDF builder
│
└── frontend/
    ├── index.html                 # Landing page
    ├── dashboard.html             # Prediction UI
    ├── comparison.html            # Model metrics comparison
    ├── analytics.html             # Visualization charts
    ├── report.html                # Patient history
    ├── about.html                 # Info + Viva Q&A
    ├── css/
    │   ├── globals.css            # Design tokens + CSS reset
    │   ├── animations.css         # Keyframe animations
    │   ├── components.css         # Reusable UI components
    │   └── pages.css              # Page-specific styles
    └── js/
        ├── api.js                 # Flask API client (fetch wrappers)
        ├── nav.js                 # Navigation + toast utilities
        ├── dashboard.js           # Prediction form + gauge logic
        ├── comparison.js          # Chart.js model comparison charts
        ├── analytics.js           # Confusion matrix + distributions
        └── report.js              # Patient history table + PDF download
```

---

## 4. REST API Specification

**Base URL:** `http://localhost:5000`  
**Content-Type:** `application/json`

### 4.1 Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/health` | Server health check | None |
| POST | `/api/predict` | Run all 3 models, return risk result | None |
| GET | `/api/models/accuracy` | Return all model accuracy metrics | None |
| GET | `/api/models/confusion` | Return per-model confusion matrix images (base64) | None |
| GET | `/api/models/feature-importance` | Return RF feature importance + ROC curve (base64) | None |
| GET | `/api/patients` | List all patient history records | None |
| POST | `/api/patients` | Save a patient record manually | None |
| GET | `/api/report/<int:patient_id>` | Download PDF for patient | None |
| POST | `/api/train` | Re-train all models | None |

### 4.2 POST /api/predict — Request Schema

```json
{
  "name": "string (optional, default: Anonymous)",
  "age": "integer",
  "sex": "integer (0 or 1)",
  "cp": "integer (0–3)",
  "trestbps": "integer",
  "chol": "integer",
  "fbs": "integer (0 or 1)",
  "restecg": "integer (0–2)",
  "thalach": "integer",
  "exang": "integer (0 or 1)",
  "oldpeak": "float",
  "slope": "integer (0–2)",
  "ca": "integer (0–3)",
  "thal": "integer (1–3)"
}
```

### 4.3 POST /api/predict — Response Schema

```json
{
  "success": true,
  "data": {
    "prediction": 1,
    "prediction_label": "Heart Disease Detected",
    "risk_score": 87.4,
    "risk_band": "critical",
    "risk_label": "Critical Risk",
    "risk_color": "#ff2d55",
    "per_model": {
      "Logistic Regression": { "probability": 82.1, "prediction": 1, "label": "Heart Disease Detected" },
      "Random Forest":       { "probability": 87.4, "prediction": 1, "label": "Heart Disease Detected" },
      "SVM":                 { "probability": 79.6, "prediction": 1, "label": "Heart Disease Detected" }
    },
    "best_model": "Logistic Regression",
    "recommendations": ["...", "..."],
    "patient_id": 42
  }
}
```

### 4.4 Error Response Schema

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

HTTP status codes: `200 OK`, `404 Not Found`, `500 Internal Server Error`, `503 Service Unavailable` (models not trained).

---

## 5. Machine Learning Pipeline

### 5.1 Dataset

| Property | Value |
|---|---|
| Source | Synthetic UCI Heart Disease-style data |
| Generator | `backend/data/heart_generator.py` |
| Size | 1,000 rows |
| Features | 13 clinical features |
| Target | Binary (`0` = No Disease, `1` = Disease) |
| Class balance | ~55% positive, ~45% negative |

### 5.2 Preprocessing (`preprocessor.py`)

1. **Cleaning:** Median imputation for missing values, duplicate removal
2. **Encoding:** One-hot encoding for categorical features (`cp`, `restecg`, `slope`, `thal`)
3. **Scaling:** `StandardScaler` — fit **only** on training set, applied to test set (no leakage)
4. **Split:** 80% train / 20% test, stratified by target label (`random_state=42`)

### 5.3 Model Configurations

| Model | Algorithm | Key Hyperparameters |
|---|---|---|
| Logistic Regression | `sklearn.linear_model.LogisticRegression` | `C=1.0`, `max_iter=1000`, `random_state=42` |
| Random Forest | `sklearn.ensemble.RandomForestClassifier` | `n_estimators=100`, `random_state=42` |
| SVM | `sklearn.svm.SVC` | `kernel='rbf'`, `probability=True`, `random_state=42` |

### 5.4 Evaluation Metrics

- **Accuracy** — Overall correct classification rate
- **Precision** — Positive predictive value (TP / (TP + FP))
- **Recall** — Sensitivity (TP / (TP + FN)) — most critical for medical ML
- **F1 Score** — Harmonic mean of precision and recall
- **AUC-ROC** — Area under Receiver Operating Characteristic curve

### 5.5 Model Performance (Approximate)

| Model | Accuracy | F1 | AUC |
|---|---|---|---|
| Logistic Regression | ~85% | ~91% | ~89% |
| **Random Forest ⭐** | ~84% | ~90% | ~87% |
| SVM | ~82% | ~90% | ~84% |

### 5.6 Inference Engine (`predictor.py`)

1. Load `StandardScaler` + saved `.pkl` model files via `joblib`
2. Preprocess input dict through `preprocess_input()`
3. Call `predict_proba()` on all 3 models
4. **Final prediction = Random Forest** (`predict_proba[:, 1]`)
5. Risk score = `rf_prob × 100`
6. Risk band assigned via thresholds: `< 30 → low`, `< 60 → moderate`, `< 80 → high`, `≥ 80 → critical`
7. `best_model` selected dynamically by max accuracy from `results.json`

### 5.7 Artifact Storage

| Artifact | Path | Format |
|---|---|---|
| Trained models | `backend/ml/models/*.pkl` | joblib binary |
| Metrics + Charts | `backend/ml/models/results.json` | JSON with base64 PNGs |
| Patient DB | `backend/db/cardiopredict.db` | SQLite binary |

---

## 6. Database Schema

**Engine:** SQLite via SQLAlchemy 2.x ORM  
**File:** `backend/db/cardiopredict.db`

### `patients` Table

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `name` | VARCHAR(100) | Patient name |
| `age` | INTEGER | Age in years |
| `sex` | VARCHAR(10) | `'0'` or `'1'` |
| `inputs_json` | TEXT | JSON-serialized raw input dict |
| `prediction` | INTEGER | `0` or `1` |
| `risk_score` | FLOAT | 0.0–100.0 |
| `risk_label` | VARCHAR(30) | e.g., `'Critical Risk'` |
| `rf_prob` | FLOAT | Random Forest probability |
| `lr_prob` | FLOAT | Logistic Regression probability |
| `svm_prob` | FLOAT | SVM probability |
| `recommendations` | TEXT | JSON-serialized list |
| `timestamp` | DATETIME | UTC timestamp (auto) |

### CRUD Operations

| Function | Description |
|---|---|
| `init_db()` | Create tables via `Base.metadata.create_all()` |
| `save_patient(name, inputs, result)` | Insert new patient record, return `id` |
| `get_all_patients()` | Return all records ordered by timestamp DESC |
| `get_patient_by_id(pid)` | Return single record by primary key |

---

## 7. PDF Report Engine

**Library:** ReportLab 4.2.0  
**Output:** A4 PDF (bytes), served as HTTP attachment

### Report Sections

| Section | Content |
|---|---|
| Header | Logo-style title, subtitle, horizontal rule |
| Report Meta | Patient ID, name, report date, assessed-by |
| Diagnosis Result | Final prediction, risk score %, risk category |
| ML Model Comparison | Table: LR / RF / SVM probability + prediction |
| Patient Medical Parameters | Two-column table of all 13 input values (labeled) |
| Health Recommendations | Numbered list from risk-band recommendations |
| Disclaimer | Legal / educational disclaimer paragraph |

### Color Palette (ReportLab)

| Token | Hex | Usage |
|---|---|---|
| `C_DARK` | `#050b1f` | Background |
| `C_NEON_BLUE` | `#00d4ff` | Headers, labels |
| `C_PANEL` | `#0d1b3e` | Table rows |
| `C_TEXT` | `#ccd6f6` | Body text |
| `C_LOW` | `#00ff88` | Low risk color |
| `C_MOD` | `#ffd60a` | Moderate risk color |
| `C_HIGH` | `#ff9500` | High risk color |
| `C_CRIT` | `#ff2d55` | Critical risk color |

---

## 8. Frontend Architecture

**Pattern:** Multi-page application (MPA), no framework, no build step  
**Styling:** Vanilla CSS with CSS custom properties (design tokens)  
**Interactivity:** ES6+ Vanilla JavaScript modules (non-module pattern)

### Design System (CSS Custom Properties in `globals.css`)

| Token Category | Examples |
|---|---|
| Colors | `--neon-blue`, `--neon-red`, `--bg-base`, `--bg-raised` |
| Typography | `--font-display` (Orbitron), `--font-body` (Inter) |
| Spacing | `--sp-xs` through `--sp-3xl` |
| Borders | `--border-dim`, `--border-glow` |
| Effects | `--glass-bg`, `--glass-border`, `--glow-blue` |

### JavaScript Modules

| File | Responsibilities |
|---|---|
| `api.js` | Typed fetch wrappers: `predict()`, `getModels()`, `getPatients()`, `downloadReport()` |
| `nav.js` | Active nav link detection, health status polling, toast notifications |
| `dashboard.js` | Form submission, animated risk gauge (canvas), per-model result cards render |
| `comparison.js` | Fetch model metrics → Chart.js grouped bar charts |
| `analytics.js` | Fetch base64 images → render confusion matrices, ROC, feature importance |
| `report.js` | Fetch patient list → HTML table, search filter, PDF download trigger |

### Visualization Strategy

- **Backend charts** (confusion matrix, ROC, feature importance): Generated server-side with Matplotlib/Seaborn, encoded as base64 PNG strings, stored in `results.json`, sent via JSON API, rendered client-side as `<img src="data:image/png;base64,...">`.
- **Frontend charts** (accuracy comparison): Rendered client-side using Chart.js 4.x with dark-theme configuration.
- **Risk gauge**: Custom HTML5 Canvas animation (`dashboard.js`) — arc fill + percentage counter animation.
- **ECG animation**: HTML5 Canvas sine-wave composite rendering loop (`index.html` inline script).

---

## 9. Startup Sequence (`run.py`)

```
1. sys.path setup (ROOT_DIR prepended)
2. import app, init_db, train_all, generate_heart_dataset
3. init_db()                        → Create SQLite tables
4. Check for heart.csv
     └── Missing → generate_heart_dataset(1000) → heart.csv
5. Check for models/*.pkl
     └── Missing → train_all(csv_path) → .pkl + results.json
6. app.run(debug=True, host='0.0.0.0', port=5000)
```

First-run duration: ~20–40 seconds (dataset generation + training).  
Subsequent runs: ~2–3 seconds (models cached).

---

## 10. API Client (`frontend/js/api.js`)

All frontend-to-backend communication goes through `api.js`:

```javascript
const API_BASE = 'http://localhost:5000';

async function predict(payload)           // POST /api/predict
async function getModelAccuracy()         // GET  /api/models/accuracy
async function getConfusionMatrices()     // GET  /api/models/confusion
async function getFeatureImportance()     // GET  /api/models/feature-importance
async function getPatients()              // GET  /api/patients
async function downloadReport(patientId) // GET  /api/report/<id>
```

---

## 11. Data Flow: Prediction Request

```
User fills form (dashboard.html)
        │
        ▼
dashboard.js → api.predict(formData)
        │
        ▼ POST /api/predict
        │
app.py → predict(data)           [ml/predictor.py]
        ├── preprocess_input()   [data/preprocessor.py]
        ├── Load 3 .pkl models   [joblib]
        ├── predict_proba × 3
        ├── Compute risk_score, risk_band, best_model
        └── RECOMMENDATIONS[band_key]
        │
        ▼ save_patient()         [db/database.py]
        │   INSERT INTO patients
        │
        ▼ JSON response → dashboard.js
        ├── Animate risk gauge
        ├── Render per-model cards
        └── Show recommendations list
```

---

## 12. Security Considerations

| Consideration | Implementation |
|---|---|
| CORS | `Flask-CORS` applied globally; accepts all origins (educational scope) |
| SQL Injection | Prevented via SQLAlchemy ORM parameterized queries |
| Input Validation | Type coercion via `int()` / `float()` in `preprocess_input()`; errors returned as 500 |
| File Access | PDF served via `send_file(io.BytesIO(...))` — no filesystem path exposure |
| Model Files | Served only via inference; no direct `.pkl` download endpoint |
| Auth | None required (educational/local deployment scope) |

---

## 13. Environment & Installation

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
pip install -r requirements.txt
python run.py
```

### Environment Variables

None required. All configuration is hardcoded for local development.

### Port

Default: `5000`. Modifiable in `run.py` or `app.py`.

---

## 14. Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Synthetic dataset | Metrics are on simulated data, not real UCI dataset | Acceptable for educational demo |
| No authentication | Any local user can access all records | Out of scope; local deployment only |
| SQLite concurrency | Not suitable for multi-user production | Upgrade to PostgreSQL for production |
| Models not versioned | Re-training overwrites existing `.pkl` | Acceptable for single-version portfolio app |
| No input sanitization on strings | Patient name not sanitized for SQL | ORM parameterization prevents injection |

---

## 15. Testing Checklist

| Test | Expected Result |
|---|---|
| `GET /api/health` | `{"status": "ok"}` |
| `POST /api/predict` with valid JSON | Returns risk score, band, recommendations |
| `POST /api/predict` with missing model `.pkl` | Returns `503` with error |
| `GET /api/models/accuracy` before training | Returns `503` |
| `GET /api/patients` | Returns array of saved records |
| `GET /api/report/1` | Downloads PDF binary |
| `POST /api/train` | Re-trains and returns updated metrics |
| All 6 HTML pages | Load without JS console errors |
| Chart.js comparison page | Bar charts render with correct values |

---

*CardioPredict TRD © 2026*
