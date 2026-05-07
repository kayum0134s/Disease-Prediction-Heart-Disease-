"""
CardioPredict — ML Training Pipeline
Trains Logistic Regression, Random Forest, and SVM.
Saves models and returns accuracy metrics + visualization base64 images.
"""
import os
import sys
import io
import base64
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

# Paths
PIPELINE_DIR = os.path.dirname(__file__)
MODELS_DIR   = os.path.join(PIPELINE_DIR, 'models')
DATA_DIR     = os.path.join(PIPELINE_DIR, '..', 'data')

sys.path.insert(0, os.path.join(PIPELINE_DIR, '..', '..'))
from backend.data.preprocessor import get_splits

# Seaborn style
sns.set_theme(style='dark', palette='muted')
DARK_BG   = '#050b1f'
NEON_BLUE = '#00d4ff'
NEON_RED  = '#ff2d55'
NEON_PURP = '#bf5af2'


def _b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                facecolor=DARK_BG, edgecolor='none', dpi=120)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64


def _confusion_matrix_b64(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4.5, 3.8), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                linewidths=0.5, linecolor='#0d1b3e',
                ax=ax, annot_kws={'size': 14, 'color': 'white'})
    ax.set_xlabel('Predicted', color=NEON_BLUE, fontsize=10)
    ax.set_ylabel('Actual', color=NEON_BLUE, fontsize=10)
    ax.set_title(title, color='white', fontsize=11, pad=10)
    ax.tick_params(colors='#8892b0')
    return _b64(fig)


def _feature_importance_b64(importances, feature_names):
    indices = np.argsort(importances)[-12:]
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    bars = ax.barh(range(len(indices)),
                   importances[indices],
                   color=NEON_BLUE, alpha=0.85)
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices], color='#ccd6f6', fontsize=9)
    ax.set_xlabel('Importance', color=NEON_BLUE, fontsize=10)
    ax.set_title('Feature Importance — Random Forest', color='white', fontsize=12, pad=10)
    ax.tick_params(axis='x', colors='#8892b0')
    ax.spines[:].set_visible(False)
    for bar in bars:
        bar.set_edgecolor('none')
    return _b64(fig)


def _roc_curve_b64(models_roc):
    """models_roc: list of (name, fpr, tpr, auc, color)"""
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.plot([0, 1], [0, 1], '--', color='#444', linewidth=1)
    for name, fpr, tpr, auc_val, color in models_roc:
        ax.plot(fpr, tpr, color=color, linewidth=2,
                label=f'{name} (AUC={auc_val:.3f})')
    ax.set_xlabel('False Positive Rate', color=NEON_BLUE, fontsize=10)
    ax.set_ylabel('True Positive Rate', color=NEON_BLUE, fontsize=10)
    ax.set_title('ROC Curve Comparison', color='white', fontsize=12, pad=10)
    ax.tick_params(colors='#8892b0')
    ax.spines[:].set_color('#1a2a4a')
    legend = ax.legend(facecolor='#0d1b3e', edgecolor=NEON_BLUE,
                       labelcolor='white', fontsize=9)
    return _b64(fig)


def train_all(csv_path=None):
    """Train LR, RF, SVM. Return metrics dict + chart b64 images."""
    if csv_path is None:
        csv_path = os.path.join(DATA_DIR, 'heart.csv')

    X_train, X_test, y_train, y_test, feature_names, _ = get_splits(csv_path)
    os.makedirs(MODELS_DIR, exist_ok=True)

    model_defs = [
        ('Logistic Regression', LogisticRegression(max_iter=1000, C=1.0, random_state=42)),
        ('Random Forest',       RandomForestClassifier(n_estimators=100, random_state=42)),
        ('SVM',                 SVC(kernel='rbf', probability=True, random_state=42)),
    ]

    results = {}
    roc_data = []
    colors = [NEON_BLUE, '#00ff88', NEON_RED]
    confusion_images = {}

    for (name, clf), color in zip(model_defs, colors):
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]

        acc  = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec  = recall_score(y_test, y_pred, zero_division=0)
        f1   = f1_score(y_test, y_pred, zero_division=0)
        auc  = roc_auc_score(y_test, y_prob)

        results[name] = {
            'accuracy':  round(acc * 100, 2),
            'precision': round(prec * 100, 2),
            'recall':    round(rec * 100, 2),
            'f1':        round(f1 * 100, 2),
            'auc':       round(auc * 100, 2),
        }

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_data.append((name, fpr, tpr, auc, color))

        confusion_images[name] = _confusion_matrix_b64(y_test, y_pred, f'Confusion Matrix — {name}')

        # Save model
        safe_name = name.lower().replace(' ', '_')
        joblib.dump(clf, os.path.join(MODELS_DIR, f'{safe_name}.pkl'))

    # Feature importance (RF)
    rf_clf = [clf for name, clf in model_defs if name == 'Random Forest'][0]
    fi_img = _feature_importance_b64(rf_clf.feature_importances_, feature_names)

    # ROC curve
    roc_img = _roc_curve_b64(roc_data)

    # Save results to JSON for fast retrieval
    output = {
        'metrics': results,
        'confusion_images': confusion_images,
        'feature_importance_image': fi_img,
        'roc_curve_image': roc_img,
        'feature_names': feature_names,
    }
    with open(os.path.join(MODELS_DIR, 'results.json'), 'w') as f:
        json.dump(output, f)

    print("[CardioPredict] Training complete:")
    for name, m in results.items():
        print(f"  {name:22s} Acc={m['accuracy']}%  F1={m['f1']}%  AUC={m['auc']}%")

    return output


if __name__ == '__main__':
    # Generate dataset if missing
    csv_path = os.path.join(DATA_DIR, 'heart.csv')
    if not os.path.exists(csv_path):
        from backend.data.heart_generator import generate_heart_dataset
        df = generate_heart_dataset(1000)
        df.to_csv(csv_path, index=False)
        print(f"[CardioPredict] Dataset generated: {csv_path}")
    train_all(csv_path)
