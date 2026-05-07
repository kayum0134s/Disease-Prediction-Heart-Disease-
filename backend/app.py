"""
CardioPredict — Flask REST API
"""
import os
import sys
import json

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, ROOT_DIR)

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import io

from backend.ml.predictor import predict, get_results
from backend.db.database import init_db, save_patient, get_all_patients, get_patient_by_id
from backend.reports.pdf_generator import generate_pdf

app = Flask(__name__, static_folder=os.path.join(ROOT_DIR, 'frontend'))
CORS(app)

# ── Static file serving ────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# ── Health check ───────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'CardioPredict API v2.0'})

# ── Predict ────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True)
    patient_name = data.pop('name', 'Anonymous')
    try:
        result = predict(data)
        # Optionally auto-save
        pid = save_patient(patient_name, data, result)
        result['patient_id'] = pid
        return jsonify({'success': True, 'data': result})
    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ── Model metrics ──────────────────────────────────────────────
@app.route('/api/models/accuracy', methods=['GET'])
def api_accuracy():
    results = get_results()
    if not results:
        return jsonify({'success': False, 'error': 'Models not trained yet'}), 503
    return jsonify({'success': True, 'data': results['metrics']})

@app.route('/api/models/confusion', methods=['GET'])
def api_confusion():
    results = get_results()
    if not results:
        return jsonify({'success': False, 'error': 'Models not trained yet'}), 503
    return jsonify({'success': True, 'data': results['confusion_images']})

@app.route('/api/models/feature-importance', methods=['GET'])
def api_feature_importance():
    results = get_results()
    if not results:
        return jsonify({'success': False, 'error': 'Models not trained yet'}), 503
    return jsonify({'success': True, 'data': {
        'image': results['feature_importance_image'],
        'roc':   results['roc_curve_image'],
    }})

# ── Patient history ────────────────────────────────────────────
@app.route('/api/patients', methods=['GET'])
def api_patients_list():
    patients = get_all_patients()
    return jsonify({'success': True, 'data': patients, 'count': len(patients)})

@app.route('/api/patients', methods=['POST'])
def api_patients_save():
    data = request.get_json(force=True)
    name   = data.get('name', 'Anonymous')
    inputs = data.get('inputs', {})
    result = data.get('result', {})
    pid = save_patient(name, inputs, result)
    return jsonify({'success': True, 'patient_id': pid})

# ── PDF Report ────────────────────────────────────────────────
@app.route('/api/report/<int:patient_id>', methods=['GET'])
def api_report(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({'success': False, 'error': 'Patient not found'}), 404
    try:
        pdf_bytes = generate_pdf(patient)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'CardioPredict_Report_{patient_id:04d}.pdf'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ── Re-train ──────────────────────────────────────────────────
@app.route('/api/train', methods=['POST'])
def api_train():
    try:
        from backend.ml.pipeline import train_all
        from backend.data.heart_generator import generate_heart_dataset
        import os
        csv_path = os.path.join(ROOT_DIR, 'backend', 'data', 'heart.csv')
        if not os.path.exists(csv_path):
            df = generate_heart_dataset(1000)
            df.to_csv(csv_path, index=False)
        results = train_all(csv_path)
        return jsonify({'success': True, 'data': results['metrics']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
