"""
CardioPredict — Data Preprocessor
Loads heart.csv, cleans, encodes, scales, and returns train/test splits.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

DATA_DIR = os.path.dirname(__file__)
CSV_PATH  = os.path.join(DATA_DIR, 'heart.csv')
SCALER_PATH = os.path.join(DATA_DIR, '..', 'ml', 'models', 'scaler.pkl')

CONTINUOUS_FEATURES = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
CATEGORICAL_FEATURES = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
TARGET = 'target'


def load_and_clean(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    # Median imputation for numeric nulls
    for col in df.columns:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)
    # Binarize target if multi-class (UCI raw sometimes has 0-4)
    df[TARGET] = (df[TARGET] > 0).astype(int)
    return df


def get_feature_matrix(df):
    """One-hot encode categoricals + scale continuous."""
    X = df.drop(columns=[TARGET])
    y = df[TARGET].values

    # One-hot encode
    X = pd.get_dummies(X, columns=[c for c in CATEGORICAL_FEATURES if c in X.columns])
    return X, y


def get_splits(csv_path=CSV_PATH, test_size=0.2, random_state=42):
    df = load_and_clean(csv_path)
    X, y = get_feature_matrix(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Fit scaler on training data only
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # Save scaler
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
    joblib.dump((scaler, list(X.columns)), SCALER_PATH)

    return X_train_sc, X_test_sc, y_train, y_test, list(X.columns), scaler


def preprocess_input(patient_dict, feature_names=None):
    """Transform a single patient input dict into a scaled numpy array."""
    scaler, saved_features = joblib.load(SCALER_PATH)

    # Build raw DataFrame row
    row = {
        'age':      int(patient_dict.get('age', 50)),
        'sex':      int(patient_dict.get('sex', 1)),
        'cp':       int(patient_dict.get('cp', 0)),
        'trestbps': int(patient_dict.get('trestbps', 120)),
        'chol':     int(patient_dict.get('chol', 200)),
        'fbs':      int(patient_dict.get('fbs', 0)),
        'restecg':  int(patient_dict.get('restecg', 0)),
        'thalach':  int(patient_dict.get('thalach', 150)),
        'exang':    int(patient_dict.get('exang', 0)),
        'oldpeak':  float(patient_dict.get('oldpeak', 0.0)),
        'slope':    int(patient_dict.get('slope', 0)),
        'ca':       int(patient_dict.get('ca', 0)),
        'thal':     int(patient_dict.get('thal', 1)),
    }

    df_row = pd.DataFrame([row])
    df_row = pd.get_dummies(df_row, columns=[c for c in CATEGORICAL_FEATURES if c in df_row.columns])

    # Align to training feature columns
    for col in saved_features:
        if col not in df_row.columns:
            df_row[col] = 0
    df_row = df_row[saved_features]

    return scaler.transform(df_row)
