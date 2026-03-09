"""
app.py — Malaria Detection Flask Web Application
=================================================
Loads a pre-trained CNN model and serves a web interface where users can
upload a blood smear image and receive an instant malaria prediction.

Usage:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os
import uuid
import numpy as np
from pathlib import Path
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf

# ─── App Configuration ────────────────────────────────────────────────────────
app = Flask(__name__)

BASE_DIR        = Path(__file__).resolve().parent
MODEL_PATH      = BASE_DIR / 'model' / 'malaria_model.h5'
LABELS_PATH     = BASE_DIR / 'model' / 'labels.txt'
UPLOAD_FOLDER   = BASE_DIR / 'static' / 'uploads'
ALLOWED_EXT     = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
IMG_SIZE        = (128, 128)
MAX_CONTENT_MB  = 10

app.config['UPLOAD_FOLDER']    = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_MB * 1024 * 1024

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ─── Load Model & Labels ──────────────────────────────────────────────────────
print('[INFO] Loading model...')
try:
    model = tf.keras.models.load_model(str(MODEL_PATH))
    print(f'[INFO] Model loaded from {MODEL_PATH}')
except Exception as e:
    print(f'[ERROR] Could not load model: {e}')
    print('[INFO]  Train the model first using notebooks/malaria_training.ipynb')
    model = None

try:
    with open(LABELS_PATH, 'r') as f:
        class_labels = [line.strip() for line in f.readlines()]
    print(f'[INFO] Labels: {class_labels}')
except FileNotFoundError:
    class_labels = ['Parasitized', 'Uninfected']
    print('[WARN] labels.txt not found — using defaults:', class_labels)


# ─── Helpers ─────────────────────────────────────────────────────────────────
def allowed_file(filename: str) -> bool:
    """Return True if the file extension is permitted."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def preprocess_image(img_path: str) -> np.ndarray:
    """
    Load an image, resize to IMG_SIZE, normalise to [0, 1],
    and expand dims to (1, H, W, 3) for model inference.
    """
    img = Image.open(img_path).convert('RGB')
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def predict(img_path: str) -> dict:
    """
    Run inference on img_path.
    Returns a dict with keys: label, confidence, raw_prob, color.
    """
    if model is None:
        return {
            'label':      'Model Not Loaded',
            'confidence': '0.00%',
            'raw_prob':   0.0,
            'color':      'gray',
            'error':      'Please train the model first.'
        }

    arr       = preprocess_image(img_path)
    raw_prob  = float(model.predict(arr, verbose=0)[0][0])

    # Model outputs P(class_index=1); class_indices depend on ImageDataGenerator
    # Kaggle dataset → 0: Parasitized, 1: Uninfected
    label_idx  = int(raw_prob > 0.5)
    label      = class_labels[label_idx] if label_idx < len(class_labels) else str(label_idx)
    confidence = raw_prob if label_idx == 1 else (1 - raw_prob)

    return {
        'label':      label,
        'confidence': f'{confidence:.2%}',
        'raw_prob':   raw_prob,
        'color':      'red' if label == 'Parasitized' else 'green',
        'icon':       '🦟' if label == 'Parasitized' else '✅'
    }


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def upload_and_predict():
    """Accept an uploaded image, run inference, return prediction."""

    # Validate request
    if 'file' not in request.files:
        return render_template('index.html', error='No file part in the request.')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected.')

    if not allowed_file(file.filename):
        return render_template(
            'index.html',
            error=f'Unsupported file type. Allowed: {", ".join(ALLOWED_EXT)}'
        )

    # Save file with a unique name to avoid collisions
    ext       = file.filename.rsplit('.', 1)[1].lower()
    unique_fn = f'{uuid.uuid4().hex}.{ext}'
    save_path = UPLOAD_FOLDER / unique_fn
    file.save(str(save_path))

    # Run prediction
    result = predict(str(save_path))

    return render_template(
        'index.html',
        prediction=result,
        image_path=f'uploads/{unique_fn}'
    )


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    JSON API endpoint for programmatic access.
    POST multipart/form-data with key 'file'.
    Returns JSON: { label, confidence, raw_prob }
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    ext       = file.filename.rsplit('.', 1)[1].lower()
    unique_fn = f'{uuid.uuid4().hex}.{ext}'
    save_path = UPLOAD_FOLDER / unique_fn
    file.save(str(save_path))

    result = predict(str(save_path))
    return jsonify(result)


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('\n' + '═' * 55)
    print('  🦟  Malaria Detection — Flask App')
    print('  Open: http://127.0.0.1:5000')
    print('═' * 55 + '\n')
    app.run(debug=True, host='0.0.0.0', port=5000)
