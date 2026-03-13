"""
Intent Prediction API — for n8n integration
============================================
Endpoint:
  POST /predict
  GET  /health
  GET  /model/info

Usage from n8n (HTTP Request node):
  Method : POST
  URL    : http://<host>:5001/predict
  Body   : JSON  →  { "text": "dimana lokasi Kawah Putih?" }
  Output : JSON  →  { "text": "...", "intent": "info_lokasi_wisata", "confidence": 97.34, "status": "ok" }

Run:
  python intent_api.py
  python intent_api.py --host 0.0.0.0 --port 5001
"""

import argparse
import os
import pickle
from datetime import datetime

from flask import Flask, jsonify, request

# ─── Config ──────────────────────────────────────────────────────
MODEL_PATH      = "intent_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"
API_KEY         = os.environ.get("INTENT_API_KEY", "")   # optional; set env var to enable auth

# ─── App ─────────────────────────────────────────────────────────
app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/predict", methods=["OPTIONS"])
def options_predict():
    return jsonify({}), 200


# ─── Auth helper ─────────────────────────────────────────────────
def check_auth():
    """Return error response if API_KEY is set and request doesn't match."""
    if not API_KEY:
        return None   # auth disabled
    key = request.headers.get("X-API-Key", "")
    if key != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized — invalid or missing X-API-Key header"}), 401
    return None


# ─── Model loader ────────────────────────────────────────────────
def load_model():
    """Load model & vectorizer from disk. Raises FileNotFoundError if not found."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"Vectorizer file not found: {VECTORIZER_PATH}")
    model      = pickle.load(open(MODEL_PATH,      "rb"))
    vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))
    return model, vectorizer


# ─── Endpoints ───────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """
    Health-check endpoint — useful for n8n IF node / monitoring.
    Returns model availability status.
    """
    model_ok = os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)
    return jsonify({
        "status":       "ok" if model_ok else "degraded",
        "model_ready":  model_ok,
        "timestamp":    datetime.utcnow().isoformat() + "Z"
    }), 200 if model_ok else 503


@app.route("/model/info", methods=["GET"])
def model_info():
    """
    Returns metadata about the loaded model.
    """
    auth_err = check_auth()
    if auth_err:
        return auth_err

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        return jsonify({"status": "error", "message": "Model belum dilatih"}), 503

    try:
        model, vectorizer = load_model()
        classes     = list(model.classes_)
        model_size  = os.path.getsize(MODEL_PATH)
        vec_size    = os.path.getsize(VECTORIZER_PATH)
        model_mtime = datetime.utcfromtimestamp(os.path.getmtime(MODEL_PATH)).isoformat() + "Z"

        return jsonify({
            "status":          "ok",
            "total_classes":   len(classes),
            "classes":         sorted(classes),
            "model_size_kb":   round(model_size  / 1024, 2),
            "vec_size_kb":     round(vec_size    / 1024, 2),
            "model_trained_at": model_mtime
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Main prediction endpoint.

    Request body (JSON):
      {
        "text": "string yang ingin diprediksi"   ← required
      }

    Response (JSON):
      {
        "status":     "ok",
        "text":       "string yang ingin diprediksi",
        "intent":     "nama_label_intent",
        "confidence": 97.34,          ← persentase (0–100)
        "all_scores": {               ← skor semua kelas (opsional, selalu disertakan)
          "info_lokasi_wisata": 97.34,
          "info_tiket_wisata":   2.66
        }
      }

    Error response:
      {
        "status":  "error",
        "message": "penjelasan error"
      }
    """
    auth_err = check_auth()
    if auth_err:
        return auth_err

    # ── Validate body ────────────────────────────────────────────
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type harus application/json"}), 400

    body = request.get_json(silent=True) or {}
    text = str(body.get("text", "")).strip()

    if not text:
        return jsonify({"status": "error", "message": "Field 'text' wajib diisi dan tidak boleh kosong"}), 400

    # ── Load & predict ───────────────────────────────────────────
    try:
        model, vectorizer = load_model()
    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": str(e)}), 503

    try:
        X          = vectorizer.transform([text])
        intent     = model.predict(X)[0]
        proba      = model.predict_proba(X)[0]
        confidence = float(max(proba))

        all_scores = {
            label: round(float(score) * 100, 2)
            for label, score in zip(model.classes_, proba)
        }

        return jsonify({
            "status":     "ok",
            "text":       text,
            "intent":     intent,
            "confidence": round(confidence * 100, 2),
            "all_scores": all_scores
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Prediction error: {str(e)}"}), 500


# ─── Batch predict (bonus — useful for n8n loop/split nodes) ─────

@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    """
    Batch prediction — predict multiple texts in one request.

    Request body (JSON):
      {
        "texts": ["teks 1", "teks 2", "teks 3"]
      }

    Response:
      {
        "status": "ok",
        "count":  3,
        "results": [
          { "text": "teks 1", "intent": "...", "confidence": 95.0 },
          ...
        ]
      }
    """
    auth_err = check_auth()
    if auth_err:
        return auth_err

    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type harus application/json"}), 400

    body  = request.get_json(silent=True) or {}
    texts = body.get("texts", [])

    if not isinstance(texts, list) or not texts:
        return jsonify({"status": "error", "message": "Field 'texts' harus berupa array string tidak kosong"}), 400

    if len(texts) > 100:
        return jsonify({"status": "error", "message": "Maksimal 100 teks per request"}), 400

    try:
        model, vectorizer = load_model()
    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": str(e)}), 503

    results = []
    for raw in texts:
        text = str(raw).strip()
        if not text:
            results.append({"text": text, "intent": None, "confidence": 0, "error": "empty text"})
            continue
        try:
            X          = vectorizer.transform([text])
            intent     = model.predict(X)[0]
            proba      = model.predict_proba(X)[0]
            confidence = round(float(max(proba)) * 100, 2)
            results.append({"text": text, "intent": intent, "confidence": confidence})
        except Exception as e:
            results.append({"text": text, "intent": None, "confidence": 0, "error": str(e)})

    return jsonify({"status": "ok", "count": len(results), "results": results})


# ─── Main ────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intent Prediction API for n8n")
    parser.add_argument("--host",  default="0.0.0.0",  help="Host (default: 0.0.0.0)")
    parser.add_argument("--port",  default=5001, type=int, help="Port (default: 5001)")
    parser.add_argument("--debug", action="store_true",   help="Enable debug mode")
    args = parser.parse_args()

    print("=" * 55)
    print("  Intent Prediction API — n8n Ready")
    print("=" * 55)
    print(f"  Host  : {args.host}")
    print(f"  Port  : {args.port}")
    print(f"  Auth  : {'Enabled (X-API-Key)' if API_KEY else 'Disabled'}")
    print(f"  Model : {'✓ Found' if os.path.exists(MODEL_PATH) else '✗ Not found — train first!'}")
    print("=" * 55)
    print("  Endpoints:")
    print("    POST /predict         — single text prediction")
    print("    POST /predict/batch   — batch prediction (max 100)")
    print("    GET  /health          — health check")
    print("    GET  /model/info      — model metadata")
    print("=" * 55)

    app.run(host=args.host, port=args.port, debug=args.debug)