"""
CardioPredict - Entry Point
Generates dataset, trains models, initializes DB, starts Flask server.
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

def bootstrap():
    from backend.db.database import init_db
    from backend.data.heart_generator import generate_heart_dataset

    print("=" * 55)
    print("  CardioPredict - AI Healthcare Platform")
    print("  Version 2.0  |  Starting up...")
    print("=" * 55)

    # 1. Init database
    init_db()
    print("[OK] Database initialized")

    # 2. Generate dataset if missing
    csv_path = os.path.join(ROOT_DIR, 'backend', 'data', 'heart.csv')
    if not os.path.exists(csv_path):
        df = generate_heart_dataset(1000)
        df.to_csv(csv_path, index=False)
        print(f"[OK] Dataset generated: {csv_path}")
    else:
        print(f"[OK] Dataset found: {csv_path}")

    # 3. Train models if missing
    models_dir  = os.path.join(ROOT_DIR, 'backend', 'ml', 'models')
    results_json = os.path.join(models_dir, 'results.json')
    if not os.path.exists(results_json):
        print("[...] Training ML models (first run - may take ~30s)...")
        from backend.ml.pipeline import train_all
        train_all(csv_path)
        print("[OK] Models trained and saved")
    else:
        print("[OK] Models already trained")

    print("=" * 55)
    print("  Server: http://localhost:5000")
    print("=" * 55)


if __name__ == '__main__':
    bootstrap()
    from backend.app import app
    app.run(debug=False, host='0.0.0.0', port=5000)
