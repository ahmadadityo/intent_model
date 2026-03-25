import json
import os
import pickle
import time

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

from flask import Flask, jsonify, request, send_from_directory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__, static_folder="static")

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return response

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options_handler(p):
    return jsonify({}), 200

DATASET_PATH          = "dataset.json"
MODEL_PATH            = "intent_model.pkl"
VECTORIZER_PATH       = "vectorizer.pkl"
DATASET_MODIFIED_PATH = "dataset_modified.txt"   # timestamp perubahan dataset
DB_CONFIG_PATH        = "db_config.json"
INTENT_QUERY_PATH     = "intent_query.json"


# ─── Helpers ─────────────────────────────────────────────────────

def load_dataset():
    if not os.path.exists(DATASET_PATH):
        return []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dataset(data):
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Catat waktu dataset diubah
    with open(DATASET_MODIFIED_PATH, "w") as f:
        f.write(str(time.time()))


def get_dataset_modified_time():
    """Kembalikan timestamp terakhir dataset diubah lewat API."""
    if os.path.exists(DATASET_MODIFIED_PATH):
        with open(DATASET_MODIFIED_PATH, "r") as f:
            try:
                return float(f.read().strip())
            except ValueError:
                pass
    # fallback: gunakan mtime file dataset.json
    if os.path.exists(DATASET_PATH):
        return os.path.getmtime(DATASET_PATH)
    return None


# ─── Dataset CRUD ────────────────────────────────────────────────

@app.route("/api/dataset", methods=["GET"])
def get_dataset():
    data = load_dataset()
    page       = int(request.args.get("page", 1))
    per_page   = int(request.args.get("per_page", 20))
    search     = request.args.get("search", "").lower()
    label_filter = request.args.get("label", "").lower()

    filtered = data
    if search:
        filtered = [
            d for d in filtered
            if search in d["texts"].lower() or search in d["label"].lower()
        ]
    if label_filter:
        filtered = [d for d in filtered if d["label"].lower() == label_filter]

    total    = len(filtered)
    start    = (page - 1) * per_page
    paginated = filtered[start:start + per_page]

    return jsonify({
        "data":        paginated,
        "total":       total,
        "page":        page,
        "per_page":    per_page,
        "total_pages": (total + per_page - 1) // per_page
    })


@app.route("/api/dataset/labels", methods=["GET"])
def get_labels():
    data   = load_dataset()
    labels = sorted(set(d["label"] for d in data))
    return jsonify(labels)


@app.route("/api/dataset/stats", methods=["GET"])
def get_stats():
    data         = load_dataset()
    label_counts = {}
    for d in data:
        label_counts[d["label"]] = label_counts.get(d["label"], 0) + 1
    return jsonify({
        "total":        len(data),
        "total_labels": len(label_counts),
        "label_counts": label_counts
    })


@app.route("/api/dataset", methods=["POST"])
def add_item():
    data  = load_dataset()
    body  = request.json
    texts = body.get("texts", "").strip()
    label = body.get("label", "").strip()

    if not texts or not label:
        return jsonify({"error": "texts dan label wajib diisi"}), 400

    next_nomor = max((d["nomor"] for d in data), default=0) + 1
    new_item   = {"nomor": next_nomor, "texts": texts, "label": label}
    data.append(new_item)
    save_dataset(data)
    return jsonify(new_item), 201


@app.route("/api/dataset/<int:nomor>", methods=["PUT"])
def update_item(nomor):
    data = load_dataset()
    body = request.json
    for item in data:
        if item["nomor"] == nomor:
            item["texts"] = body.get("texts", item["texts"]).strip()
            item["label"] = body.get("label", item["label"]).strip()
            save_dataset(data)
            return jsonify(item)
    return jsonify({"error": "Data tidak ditemukan"}), 404


@app.route("/api/dataset/<int:nomor>", methods=["DELETE"])
def delete_item(nomor):
    data     = load_dataset()
    new_data = [d for d in data if d["nomor"] != nomor]
    if len(new_data) == len(data):
        return jsonify({"error": "Data tidak ditemukan"}), 404
    save_dataset(new_data)
    return jsonify({"message": "Data berhasil dihapus"})


# ─── Label Management ────────────────────────────────────────────

@app.route("/api/labels", methods=["GET"])
def get_labels_detail():
    """Return all unique labels with their counts, sorted alphabetically."""
    data         = load_dataset()
    label_counts = {}
    for d in data:
        label_counts[d["label"]] = label_counts.get(d["label"], 0) + 1
    result = [
        {"label": label, "count": count}
        for label, count in sorted(label_counts.items())
    ]
    return jsonify(result)


@app.route("/api/labels/rename", methods=["PUT"])
def rename_label():
    """Rename all occurrences of old_label to new_label in the dataset."""
    body      = request.json
    old_label = body.get("old_label", "").strip()
    new_label = body.get("new_label", "").strip()

    if not old_label or not new_label:
        return jsonify({"error": "old_label dan new_label wajib diisi"}), 400
    if old_label == new_label:
        return jsonify({"error": "Label baru sama dengan label lama"}), 400

    data          = load_dataset()
    updated_count = 0
    for item in data:
        if item["label"] == old_label:
            item["label"] = new_label
            updated_count += 1

    if updated_count == 0:
        return jsonify({"error": f"Label '{old_label}' tidak ditemukan"}), 404

    save_dataset(data)
    return jsonify({
        "message":       f"Label '{old_label}' berhasil diubah menjadi '{new_label}'",
        "updated_count": updated_count,
        "old_label":     old_label,
        "new_label":     new_label
    })


@app.route("/api/labels/delete", methods=["DELETE"])
def delete_label():
    """Delete all dataset entries with the given label."""
    body  = request.json
    label = body.get("label", "").strip()

    if not label:
        return jsonify({"error": "label wajib diisi"}), 400

    data          = load_dataset()
    new_data      = [d for d in data if d["label"] != label]
    deleted_count = len(data) - len(new_data)

    if deleted_count == 0:
        return jsonify({"error": f"Label '{label}' tidak ditemukan"}), 404

    save_dataset(new_data)
    return jsonify({
        "message":       f"Label '{label}' dan {deleted_count} data berhasil dihapus",
        "deleted_count": deleted_count,
        "label":         label
    })


# ─── Model Training ──────────────────────────────────────────────

@app.route("/api/train", methods=["POST"])
def train_model():
    data = load_dataset()
    if len(data) < 2:
        return jsonify({"error": "Dataset terlalu sedikit untuk melatih model"}), 400

    texts  = [item["texts"] for item in data]
    labels = [item["label"]  for item in data]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000)
    model.fit(X, labels)

    pickle.dump(model,      open(MODEL_PATH,      "wb"))
    pickle.dump(vectorizer, open(VECTORIZER_PATH, "wb"))

    unique_labels = list(set(labels))
    return jsonify({
        "message":         "Model berhasil dilatih dan disimpan",
        "total_data":      len(data),
        "total_labels":    len(unique_labels),
        "labels":          sorted(unique_labels),
        "model_file":      MODEL_PATH,
        "vectorizer_file": VECTORIZER_PATH
    })


@app.route("/api/model/status", methods=["GET"])
def model_status():
    model_exists      = os.path.exists(MODEL_PATH)
    vectorizer_exists = os.path.exists(VECTORIZER_PATH)
    info = {"model_exists": model_exists, "vectorizer_exists": vectorizer_exists}

    if model_exists:
        model_mtime        = os.path.getmtime(MODEL_PATH)
        info["model_size"]     = os.path.getsize(MODEL_PATH)
        info["model_modified"] = model_mtime
    else:
        model_mtime = None

    if vectorizer_exists:
        info["vectorizer_size"] = os.path.getsize(VECTORIZER_PATH)

    # Cek apakah dataset lebih baru dari model → perlu training ulang
    dataset_mtime            = get_dataset_modified_time()
    info["dataset_modified"] = dataset_mtime

    if model_exists and dataset_mtime is not None and model_mtime is not None:
        info["needs_retrain"] = dataset_mtime > model_mtime
    else:
        info["needs_retrain"] = False

    return jsonify(info)


@app.route("/api/predict", methods=["POST"])
def predict():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        return jsonify({"error": "Model belum dilatih"}), 400
    body = request.json
    text = body.get("text", "").strip()
    if not text:
        return jsonify({"error": "text wajib diisi"}), 400

    model      = pickle.load(open(MODEL_PATH,      "rb"))
    vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))
    X          = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    proba      = model.predict_proba(X)[0]
    confidence = float(max(proba))
    return jsonify({"text": text, "intent": prediction, "confidence": round(confidence * 100, 2)})

# ─── Database Config Endpoints ───────────────────────────────────

@app.route("/api/db/config", methods=["GET"])
def get_db_config():
    config = load_db_config()
    # Jangan kirim password ke frontend secara penuh
    safe = config.copy()
    if safe.get("password"):
        safe["password"] = "••••••••"
    return jsonify(safe)


@app.route("/api/db/config", methods=["POST"])
def save_db_config_api():
    body = request.json
    required = ["host", "port", "username", "database"]
    for field in required:
        if field not in body or str(body[field]).strip() == "":
            return jsonify({"error": f"Field '{field}' wajib diisi"}), 400

    config = {
        "host":     body["host"].strip(),
        "port":     int(body["port"]),
        "username": body["username"].strip(),
        "password": body.get("password", ""),   # boleh kosong
        "database": body["database"].strip()
    }
    save_db_config(config)
    return jsonify({"message": "Konfigurasi database berhasil disimpan"})


@app.route("/api/db/test", methods=["POST"])
def test_db_connection():
    if not MYSQL_AVAILABLE:
        return jsonify({
            "success": False,
            "error": "Library mysql-connector-python belum terinstal. Jalankan: pip install mysql-connector-python"
        }), 400

    body = request.json

    # Bisa pakai config dari body (test sebelum simpan) atau dari file
    if body and body.get("host"):
        config = body
    else:
        config = load_db_config()

    if not config:
        return jsonify({"success": False, "error": "Konfigurasi database belum disimpan"}), 400

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=int(config.get("port", 3306)),
            user=config["username"],
            password=config.get("password", ""),
            database=config["database"],
            connection_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            "success": True,
            "message": f"Koneksi berhasil! MySQL versi {version}",
            "host":    config["host"],
            "database": config["database"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200


# ─── Intent Query Endpoints ───────────────────────────────────────

@app.route("/api/intent-queries", methods=["GET"])
def get_intent_queries():
    queries = load_intent_queries()
    # Gabungkan dengan daftar label dari dataset supaya semua label terlihat
    data    = load_dataset()
    labels  = sorted(set(d["label"] for d in data))
    result  = []
    for label in labels:
        result.append({
            "label": label,
            "query": queries.get(label, "")
        })
    # Tambahkan entry dari intent_query.json yang labelnya sudah tidak ada di dataset
    for label, query in queries.items():
        if label not in set(labels):
            result.append({"label": label, "query": query, "orphan": True})
    return jsonify(result)


@app.route("/api/intent-queries/<path:label>", methods=["PUT"])
def save_intent_query(label):
    body  = request.json
    query = body.get("query", "").strip()
    queries = load_intent_queries()

    if query:
        # ── Validasi: hanya izinkan perintah SELECT ──────────────
        DANGEROUS_KEYWORDS = [
            "drop", "delete", "truncate", "alter",
            "insert", "update", "create", "grant", "revoke"
        ]
        query_lower = query.lower()
        if not query_lower.lstrip().startswith("select"):
            return jsonify({"error": "Hanya perintah SELECT yang diizinkan"}), 400
        if any(kw in query_lower for kw in DANGEROUS_KEYWORDS):
            return jsonify({"error": "Query mengandung perintah berbahaya yang tidak diizinkan"}), 400
        # ─────────────────────────────────────────────────────────

        queries[label] = query
    else:
        queries.pop(label, None)   # hapus jika query dikosongkan

    save_intent_queries(queries)
    return jsonify({
        "message": f"Query untuk label '{label}' berhasil disimpan",
        "label":   label,
        "query":   query
    })

MAX_QUERY_ROWS = 500   # tambahkan di bagian konstanta atas file, dekat DATASET_PATH dll.

@app.route("/api/intent-queries/<path:label>/execute", methods=["POST"])
def execute_intent_query(label):
    """Jalankan query SQL yang tersimpan untuk label tertentu."""
    if not MYSQL_AVAILABLE:
        return jsonify({"success": False, "error": "Library mysql-connector-python belum terinstal."}), 400

    queries = load_intent_queries()
    query   = queries.get(label, "").strip()

    if not query:
        return jsonify({"success": False, "error": f"Tidak ada query untuk label '{label}'"}), 404

    config = load_db_config()
    if not config or not config.get("host"):
        return jsonify({"success": False, "error": "Konfigurasi database belum disimpan."}), 400

    # Ambil params opsional dari body (untuk placeholder ?)
    body       = request.json or {}
    raw_params = body.get("params", [])

    # ── Validasi params: harus list of scalar values ─────────────
    if not isinstance(raw_params, list):
        return jsonify({"success": False, "error": "params harus berupa array"}), 400
    ALLOWED_TYPES = (str, int, float, type(None))
    if not all(isinstance(p, ALLOWED_TYPES) for p in raw_params):
        return jsonify({"success": False, "error": "Setiap elemen params harus berupa string, angka, atau null"}), 400
    params = raw_params
    # ─────────────────────────────────────────────────────────────

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=int(config.get("port", 3306)),
            user=config["username"],
            password=config.get("password", ""),
            database=config["database"],
            connection_timeout=5
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)

        # ── Batasi jumlah baris yang dikembalikan ─────────────────
        rows      = cursor.fetchmany(MAX_QUERY_ROWS)
        truncated = len(rows) == MAX_QUERY_ROWS
        # ─────────────────────────────────────────────────────────

        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        cursor.close()
        conn.close()
        return jsonify({
            "success":   True,
            "label":     label,
            "query":     query,
            "columns":   columns,
            "rows":      rows,
            "total":     len(rows),
            "truncated": truncated          # beri tahu frontend jika data dipotong
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200


@app.route("/api/intent-queries/<path:label>", methods=["DELETE"])
def delete_intent_query(label):
    queries = load_intent_queries()
    if label not in queries:
        return jsonify({"error": f"Query untuk label '{label}' tidak ditemukan"}), 404
    del queries[label]
    save_intent_queries(queries)
    return jsonify({"message": f"Query untuk label '{label}' berhasil dihapus"})


# ─── Serve Frontend ──────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ─── DB Config & Intent Query Helpers ────────────────────────────

def load_db_config():
    if not os.path.exists(DB_CONFIG_PATH):
        return {}
    with open(DB_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db_config(config):
    with open(DB_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_intent_queries():
    if not os.path.exists(INTENT_QUERY_PATH):
        return {}
    with open(INTENT_QUERY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_intent_queries(queries):
    with open(INTENT_QUERY_PATH, "w", encoding="utf-8") as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    app.run(debug=True, port=5000)