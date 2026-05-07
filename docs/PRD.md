# Product Requirements Document (PRD)

**Product:** CardioPredict — AI-Powered Cardiovascular Risk Assessment Platform  
**Version:** 2.0  
**Date:** May 2026  
**Status:** ✅ Completed  

---

## 1. Executive Summary

CardioPredict is a full-stack, AI-powered cardiovascular risk assessment platform. It accepts 13 standard clinical parameters and uses an ensemble of three machine learning models (Logistic Regression, Random Forest, SVM) to produce a probabilistic heart disease risk score, risk band classification, personalized health recommendations, and a downloadable PDF medical report — all through a glassmorphism-themed web interface.

---

## 2. Problem Statement

Cardiovascular disease (CVD) is the leading cause of death globally. Early risk detection through clinical data analysis can guide timely intervention, but specialist consultations may not be immediately accessible. There is a need for an intelligent, accessible tool that:

- Converts standard clinical readings into an actionable risk score
- Compares multiple ML model predictions transparently
- Persists patient history for longitudinal tracking
- Communicates results clearly to non-specialist users

CardioPredict addresses this as an AI-health demonstration application for academic/portfolio contexts.

---

## 3. Goals & Objectives

| Goal | Success Metric |
|---|---|
| Accurate multi-model risk prediction | ≥ 82% accuracy across all 3 models |
| Actionable, personalized guidance | Risk-band-mapped recommendations (4 tiers) |
| Persist all predictions | SQLite DB with full patient CRUD |
| Generate professional reports | ReportLab PDF with all key clinical data |
| Model transparency & analytics | Confusion matrices, ROC curves, feature importance |
| World-class frontend experience | Glassmorphism UI with micro-animations |

---

## 4. Target Users

| Persona | Use Case |
|---|---|
| Healthcare Students | Learn how clinical data maps to ML predictions |
| ML/Data Science Students | Explore multi-model comparison and evaluation |
| Portfolio Reviewers | Evaluate full-stack AI application quality |
| Project Examiners | Assess understanding of ML pipeline and system design |

> ⚠️ **Not intended for** clinical diagnosis or real patient management.

---

## 5. Features & User Stories

### F1 — AI Cardiovascular Risk Prediction
- Enter 13 clinical parameters → instant risk score (0–100%)
- See predictions from three ML models side-by-side
- Animated risk gauge with color-coded risk band (Low / Moderate / High / Critical)

### F2 — Model Analytics Dashboard
- View Accuracy, Precision, Recall, F1, AUC for each trained model
- View per-model confusion matrices
- View ROC curve comparison chart for all three models

### F3 — Feature Importance Analysis
- Bar chart of top-12 most important clinical features (Random Forest)
- Understand which parameters drive the prediction most

### F4 — Patient History Management
- All predictions auto-saved to database
- Searchable, sortable table of all previous patient records
- Download PDF report for any patient at any time

### F5 — PDF Medical Report Generation
- Downloadable professional medical report per patient
- Includes: patient identity, diagnosis, risk score, model comparison, clinical parameters, recommendations

### F6 — Personalized Health Recommendations
- Risk-band–mapped curated guidance list
- From lifestyle tips (Low Risk) to urgent medical referrals (Critical Risk)

### F7 — Model Re-Training (Admin)
- Trigger re-training via `POST /api/train`
- Auto-generates synthetic dataset if `heart.csv` is absent

---

## 6. Frontend Pages

| Page | File | Description |
|---|---|---|
| Home | `index.html` | Hero, animated ECG canvas, stats bar, feature grid, pipeline visual |
| Dashboard | `dashboard.html` | 13-param form, risk gauge, per-model cards, recommendations |
| Model Comparison | `comparison.html` | Chart.js bar charts: Accuracy, F1, AUC |
| Analytics | `analytics.html` | Confusion matrices, feature importance, ROC curve, distributions |
| Reports | `report.html` | Patient history table, search, filter, PDF download |
| About | `about.html` | Project info, tech stack, ML methodology, Viva Q&A |

---

## 7. Input Parameters

| Parameter | Description | Range |
|---|---|---|
| `age` | Age in years | 29–77 |
| `sex` | 1 = Male, 0 = Female | 0 or 1 |
| `cp` | Chest pain type | 0–3 |
| `trestbps` | Resting BP (mmHg) | 94–200 |
| `chol` | Serum cholesterol (mg/dl) | 126–564 |
| `fbs` | Fasting blood sugar > 120 mg/dl | 0 or 1 |
| `restecg` | Resting ECG results | 0–2 |
| `thalach` | Max heart rate (bpm) | 71–202 |
| `exang` | Exercise-induced angina | 0 or 1 |
| `oldpeak` | ST depression (exercise vs rest) | 0.0–6.2 |
| `slope` | Slope of peak exercise ST | 0–2 |
| `ca` | Major vessels by fluoroscopy | 0–3 |
| `thal` | Thalassemia type | 1–3 |

---

## 8. Risk Band Classification

| Risk Score | Band | Color | Action |
|---|---|---|---|
| 0–29% | 🟢 Low Risk | `#00ff88` | Annual checkups, maintain lifestyle |
| 30–59% | 🟡 Moderate Risk | `#ffd60a` | Dietary changes, physician consult |
| 60–79% | 🟠 High Risk | `#ff9500` | Cardiologist consult, stress test |
| 80–100% | 🔴 Critical Risk | `#ff2d55` | Immediate emergency evaluation |

---

## 9. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Prediction response ≤ 2 seconds |
| Availability | Runs locally via `python run.py`; no cloud dependency |
| Scalability | SQLite for educational use; upgradeable to PostgreSQL |
| Usability | All pages mobile-responsive; consistent glassmorphism UI |
| Security | CORS enabled; no auth required for educational scope |
| Accuracy | Minimum 82% classification accuracy on 20% held-out test set |
| Portability | Cross-platform via Python 3.11+ |
| Reliability | Models cached as `.pkl` files; prediction works without re-training |

---

## 10. Constraints & Assumptions

- Dataset: 1,000-row synthetic UCI-style heart disease dataset, auto-generated on first run
- No real patient data is processed (educational/synthetic only)
- Runs on `localhost:5000`; no cloud deployment required
- Chart.js 4.x loaded via CDN; no frontend build step required
- No login or role management required
- PDF generation is server-side using ReportLab (pure Python)

---

## 11. Out of Scope

- Real-time ECG device integration
- HIPAA / clinical data compliance
- Cloud hosting / CI/CD pipeline
- Multi-user authentication and RBAC
- Mobile native application
- EHR system integration

---

## 12. Success Criteria

| Criterion | Definition of Done |
|---|---|
| Prediction endpoint works | `POST /api/predict` returns risk score, band, per-model results, recommendations |
| All 3 models trained | `.pkl` files present in `backend/ml/models/` |
| Patient history persisted | Records appear in `report.html` after prediction |
| PDF report downloads | `/api/report/<id>` returns valid PDF |
| Frontend renders | All 6 pages load without console errors |
| Analytics charts display | Confusion matrices, ROC, feature importance render via base64 |

---

## 13. Disclaimer

> CardioPredict is developed strictly for **educational and research purposes only**. It does not constitute a clinical diagnostic tool. All outputs must be reviewed by a qualified healthcare professional before any medical decision is made.

---

*CardioPredict PRD © 2026*
