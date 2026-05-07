"""
CardioPredict — Synthetic Heart Disease Dataset Generator
Generates a realistic 1000-row dataset matching UCI Heart Disease schema.
"""
import numpy as np
import pandas as pd
import os

def generate_heart_dataset(n_samples=1000, seed=42):
    np.random.seed(seed)
    n = n_samples

    # Age: 29–77
    age = np.random.randint(29, 78, n)

    # Sex: 0=female, 1=male (ratio ~68% male in UCI)
    sex = np.random.choice([0, 1], n, p=[0.32, 0.68])

    # Chest pain type: 0=typical angina, 1=atypical angina, 2=non-anginal, 3=asymptomatic
    cp = np.random.choice([0, 1, 2, 3], n, p=[0.08, 0.16, 0.28, 0.48])

    # Resting blood pressure: 94–200 mmHg
    trestbps = np.random.normal(130, 18, n).clip(94, 200).astype(int)

    # Cholesterol: 126–564 mg/dl
    chol = np.random.normal(245, 52, n).clip(126, 564).astype(int)

    # Fasting blood sugar > 120: 0 or 1
    fbs = np.random.choice([0, 1], n, p=[0.85, 0.15])

    # Resting ECG: 0=normal, 1=ST-T abnormality, 2=LV hypertrophy
    restecg = np.random.choice([0, 1, 2], n, p=[0.50, 0.48, 0.02])

    # Max heart rate: 71–202 bpm
    thalach = np.random.normal(150, 23, n).clip(71, 202).astype(int)

    # Exercise-induced angina
    exang = np.random.choice([0, 1], n, p=[0.67, 0.33])

    # ST depression: 0–6.2
    oldpeak = np.round(np.random.exponential(1.0, n).clip(0, 6.2), 1)

    # Slope of peak exercise ST: 0=upsloping, 1=flat, 2=downsloping
    slope = np.random.choice([0, 1, 2], n, p=[0.21, 0.14, 0.65])

    # Number of major vessels: 0–3
    ca = np.random.choice([0, 1, 2, 3], n, p=[0.58, 0.22, 0.13, 0.07])

    # Thal: 1=normal, 2=fixed defect, 3=reversible defect
    thal = np.random.choice([1, 2, 3], n, p=[0.55, 0.07, 0.38])

    # Build risk score to generate realistic target
    risk = (
        0.03 * (age - 29) +
        0.15 * (cp == 3) * 2 +
        0.10 * exang +
        0.12 * (oldpeak > 2.0) +
        0.10 * (slope == 1) +
        0.15 * (ca > 0) +
        0.12 * (thal == 3) +
        0.08 * (trestbps > 140) +
        0.06 * (chol > 240) +
        0.05 * fbs -
        0.10 * ((thalach - 71) / (202 - 71))
    )
    prob = 1 / (1 + np.exp(-5 * (risk - 0.5)))
    target = (np.random.rand(n) < prob).astype(int)

    df = pd.DataFrame({
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
        'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalach': thalach,
        'exang': exang, 'oldpeak': oldpeak, 'slope': slope, 'ca': ca,
        'thal': thal, 'target': target
    })
    return df


if __name__ == '__main__':
    out_dir = os.path.dirname(__file__)
    df = generate_heart_dataset(1000)
    path = os.path.join(out_dir, 'heart.csv')
    df.to_csv(path, index=False)
    print(f"[OK] Dataset saved to {path}  shape={df.shape}  target_ratio={df['target'].mean():.2f}")
