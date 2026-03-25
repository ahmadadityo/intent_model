# 🧠 Intent Dataset Manager

Sistem manajemen dataset dan pelatihan model machine learning untuk klasifikasi intent berbasis teks. Dibangun dengan **Python (Flask)** sebagai back-end dan **HTML + TailwindCSS + Vanilla JavaScript** sebagai front-end.

---

## 📌 Fitur Utama

| Fitur | Deskripsi |
|---|---|
| 📋 **Kelola Dataset** | Lihat, tambah, ubah, dan hapus data intent dari file `dataset.json` |
| 🏷️ **Kelola Label** | Kelola data label dari file `dataset.json` |
| ⚡ **Latih Model** | Buat model intent (`.pkl`) menggunakan TF-IDF + Logistic Regression |
| 🔮 **Uji Prediksi** | Tes model secara langsung dari antarmuka web |
| 📊 **Statistik** | Distribusi label dan ringkasan dataset |
| 🗄️ **Database** | Distribusi label dan ringkasan dataset |

---

## 🗂️ Struktur Proyek

```
intent-manager/
│
├── app.py                  # Back-end Flask (API server + UI)
├── intent_api.py           # API khusus n8n / integrasi eksternal
├── dataset.json            # Dataset intent (teks + label)
├── db_config.json          # Dataset konfigurasi database
├── intent_query.json       # Dataset konfigurasi query berdasarkan label
├── requirements.txt        # Dependensi Python
├── intent_model.pkl        # Model (dibuat setelah training)
├── vectorizer.pkl          # Vectorizer (dibuat setelah training)
│
└── static/
    └── index.html          # Front-end (HTML + TailwindCSS + JS)
```

---

## ⚙️ Instalasi

### 1. Prasyarat

Pastikan sudah terinstal:
- Python 3.8 atau lebih baru
- pip (package manager Python)

### 2. Clone / Unduh Proyek

```bash
git clone https://github.com/ahmadadityo/intent_model.git
cd intent_model
```

Atau ekstrak file ZIP ke folder pilihan Anda.

### 3. Buat Virtual Environment (Disarankan)

```bash
python -m venv venv
```

Aktifkan virtual environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Instal Dependensi

```bash
pip install -r requirements.txt
```

Dependensi yang diinstal:
- `flask` — Web framework untuk API back-end
- `flask-cors` — Menangani Cross-Origin Resource Sharing
- `scikit-learn` — Library machine learning (TF-IDF & Logistic Regression)
- `mysql-connector-python` — Library menghubungkan aplikasi Python dengan database MySQL

---

## 🚀 Menjalankan Aplikasi

```bash
python app.py
```

Setelah server berjalan, buka browser dan akses:

```
http://localhost:5000
```

---

## 📖 Panduan Penggunaan

### 📋 Halaman Dataset

Halaman utama untuk mengelola data intent.

**Melihat Data:**
- Tabel menampilkan nomor, teks, dan label intent
- Gunakan kolom pencarian untuk mencari teks atau label tertentu
- Gunakan dropdown filter untuk memfilter berdasarkan label spesifik
- Atur jumlah data per halaman (10 / 20 / 50 / 100)
- Navigasi halaman menggunakan pagination di bawah tabel

**Menambah Data:**
1. Klik tombol **+ Tambah Data** di kanan atas
2. Isi kolom **Teks** dengan kalimat intent
3. Isi kolom **Label Intent** (tersedia saran dari label yang ada)
4. Klik **Simpan**

**Mengubah Data:**
1. Klik ikon ✏️ pada baris data yang ingin diubah
2. Ubah teks atau label sesuai kebutuhan
3. Klik **Update**

**Menghapus Data:**
1. Klik ikon 🗑️ pada baris data yang ingin dihapus
2. Konfirmasi penghapusan pada dialog yang muncul

---

###  🏷️ Halaman Label

Halaman untuk kelola data Label

- Mini stats — total label, total data, rata-rata per label
- Daftar label distinct — tiap label tampil sekali dengan jumlah datanya
- Edit inline — isi kolom "Label Baru" untuk perbaiki typo; badge → label_baru muncul real-time
- Deteksi merge — badge kuning ⚡ akan digabung otomatis muncul jika label tujuan sudah ada
- Sticky save bar — muncul di bawah layar saat ada perubahan pending, lengkap dengan counter
- Modal konfirmasi — menampilkan daftar semua perubahan sebelum disimpan
- Hapus label — tombol 🗑️ per baris + konfirmasi sebelum menghapus semua data terkait
- Filter pencarian label di halaman tersebut

---

### ⚡ Halaman Latih Model

Halaman untuk melatih model machine learning dari dataset.

**Langkah Training:**
1. Buka halaman **Latih Model** dari sidebar
2. Periksa status model di panel kiri (tersedia / belum tersedia)
3. Klik tombol **⚡ Mulai Training**
4. Pantau proses pada **Log Training** di panel kanan
5. Setelah selesai, file berikut akan dibuat:
   - `intent_model.pkl` — Model Logistic Regression
   - `vectorizer.pkl` — TF-IDF Vectorizer

> **Catatan:** Dataset harus memiliki minimal 2 data untuk dapat melatih model.

---

### 🔮 Halaman Prediksi

Menguji model yang sudah dilatih dengan teks baru.

1. Buka halaman **Prediksi** dari sidebar
2. Ketik teks pada kolom yang tersedia
3. Tekan **Enter** atau klik tombol **🔮 Prediksi Intent**
4. Hasil akan menampilkan:
   - **Label intent** yang diprediksi
   - **Confidence score** (persentase keyakinan model)

> **Catatan:** Model harus dilatih terlebih dahulu sebelum dapat melakukan prediksi.

---

### 📊 Halaman Statistik

Menampilkan ringkasan dan distribusi dataset:
- Total jumlah data
- Total label unik
- Rata-rata data per label
- Bar chart distribusi per label (diurutkan dari terbanyak)

---

### 🗄️ Halaman Database

Halaman untuk mengatur koneksi MySQL dan memetakan query SQL ke setiap label intent.
Halaman ini terbagi menjadi dua bagian utama: **Konfigurasi Koneksi** dan **Query per Label Intent**.

---

## 🔌 API Endpoints

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/api/dataset` | Ambil data (dengan paginasi & filter) |
| `POST` | `/api/dataset` | Tambah data baru |
| `PUT` | `/api/dataset/<nomor>` | Update data berdasarkan nomor |
| `DELETE` | `/api/dataset/<nomor>` | Hapus data berdasarkan nomor |
| `GET` | `/api/dataset/labels` | Daftar semua label unik |
| `GET` | `/api/dataset/stats` | Statistik dataset |
| `GET` | `/api/labels` | Ambil semua label unik beserta jumlah datanya |
| `GET` | `/api/labels/rename` | Ganti nama label secara bulk (otomatis merge jika label tujuan sudah ada) |
| `DELETE` | `/api/labels/delete` | Hapus semua data dengan label tertentu |
| `POST` | `/api/train` | Latih dan simpan model |
| `GET` | `/api/model/status` | Status ketersediaan model |
| `POST` | `/api/predict` | Prediksi intent dari teks |
| `GET` | `/api/db/config` | Ambil konfigurasi database (password di-mask) |
| `POST` | `/api/db/config` | Simpan konfigurasi koneksi MySQL |
| `POST` | `/api/db/test` | Test koneksi ke database MySQL |
| `GET` | `/api/intent-queries` | Ambil semua query per label intent |
| `PUT` | `/api/intent-queries/<label>` | Simpan atau update query untuk label tertentu |
| `DELETE` | `/api/intent-queries/<label>` | Hapus query untuk label tertentu |

---

## 🛠️ Teknologi yang Digunakan

**Back-end:**
- Python 3.x
- Flask — REST API server
- scikit-learn — TF-IDF Vectorizer + Logistic Regression
- pickle — Serialisasi model

**Front-end:**
- HTML5
- TailwindCSS (CDN)
- Vanilla JavaScript (Fetch API)
- Google Fonts (Syne + Space Mono)

---

## 📝 Format Dataset

File `dataset.json` berformat array JSON dengan struktur:

```json
[
  {
    "nomor": 1,
    "texts": "dimana lokasi Kawah Putih Bandung",
    "label": "info_lokasi_wisata"
  },
  {
    "nomor": 2,
    "texts": "berapa harga tiket masuk Tangkuban Perahu",
    "label": "info_tiket_wisata"
  }
]
```

| Field | Tipe | Deskripsi |
|---|---|---|
| `nomor` | integer | ID unik data (auto-increment) |
| `texts` | string | Kalimat atau pertanyaan intent |
| `label` | string | Kategori intent (snake_case) |

---

## ❓ Troubleshooting

**Server tidak bisa dijalankan:**
- Pastikan Python dan pip sudah terinstal dengan benar
- Pastikan virtual environment sudah diaktifkan
- Jalankan ulang `pip install -r requirements.txt`

**Prediksi tidak bisa dilakukan:**
- Model belum dilatih — buka halaman **Latih Model** dan klik **Mulai Training**

**Data tidak tersimpan:**
- Pastikan file `dataset.json` ada di direktori yang sama dengan `app.py`
- Pastikan Python memiliki izin tulis pada direktori tersebut

---

## 🔗 Intent API — Integrasi n8n & Eksternal

File `intent_api.py` adalah API terpisah yang dirancang khusus untuk integrasi dengan **n8n** atau tools eksternal lainnya. Berjalan di port **5001** (terpisah dari `app.py` di port 5000).

### Menjalankan Intent API

```bash
python intent_api.py
# atau dengan opsi custom:
python intent_api.py --host 0.0.0.0 --port 5001 --debug
```

> **Prasyarat:** Model harus sudah dilatih terlebih dahulu melalui `app.py` → halaman **Latih Model**.

### Endpoint Intent API

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/health` | Health check & status model |
| `GET` | `/model/info` | Info model & daftar semua label |
| `POST` | `/predict` | Prediksi intent dari 1 teks |
| `POST` | `/predict/batch` | Prediksi banyak teks sekaligus (maks 100) |

### Keamanan (Opsional — API Key)

Untuk mengaktifkan autentikasi, set environment variable sebelum menjalankan server:

```bash
# Linux / macOS
export INTENT_API_KEY=rahasia123
python intent_api.py

# Windows
set INTENT_API_KEY=rahasia123
python intent_api.py
```

Tambahkan header berikut di setiap request:
```
X-API-Key: rahasia123
```

Jika `INTENT_API_KEY` tidak di-set, autentikasi dinonaktifkan (semua request diterima).

---

## 🧪 Panduan Uji Coba dengan Postman

### Langkah 0 — Pastikan Server Aktif

Jalankan `intent_api.py` dan pastikan terminal menampilkan:
```
Running on http://0.0.0.0:5001
```

---

### 1. Health Check

Gunakan ini untuk memastikan server aktif dan model sudah siap.

- **Method:** `GET`
- **URL:** `http://localhost:5001/health`
- Klik **Send**

**Response sukses:**
```json
{
  "model_ready": true,
  "status": "ok",
  "timestamp": "2026-03-13T00:00:00Z"
}
```

**Response jika model belum dilatih:**
```json
{
  "model_ready": false,
  "status": "degraded",
  "timestamp": "2026-03-13T00:00:00Z"
}
```

---

### 2. Predict — Prediksi 1 Teks

- **Method:** `POST`
- **URL:** `http://localhost:5001/predict`
- Tab **Body** → pilih **raw** → dropdown ubah ke **JSON**
- Isi body:

```json
{
  "text": "dimana lokasi Kawah Putih Bandung?"
}
```

- Klik **Send**

**Response:**
```json
{
  "status": "ok",
  "text": "dimana lokasi Kawah Putih Bandung?",
  "intent": "info_lokasi_wisata",
  "confidence": 97.34,
  "all_scores": {
    "info_lokasi_wisata": 97.34,
    "info_tiket_wisata": 2.66
  }
}
```

---

### 3. Predict Batch — Prediksi Banyak Teks Sekaligus

- **Method:** `POST`
- **URL:** `http://localhost:5001/predict/batch`
- **Body → raw → JSON:**

```json
{
  "texts": [
    "dimana lokasi Kawah Putih?",
    "berapa harga tiket Tangkuban Perahu?",
    "jam buka Kebun Binatang Bandung?"
  ]
}
```

**Response:**
```json
{
  "status": "ok",
  "count": 3,
  "results": [
    { "text": "dimana lokasi Kawah Putih?", "intent": "info_lokasi_wisata", "confidence": 97.34 },
    { "text": "berapa harga tiket Tangkuban Perahu?", "intent": "info_tiket_wisata", "confidence": 94.10 },
    { "text": "jam buka Kebun Binatang Bandung?", "intent": "info_jam_buka", "confidence": 88.75 }
  ]
}
```

---

### 4. Model Info — Cek Daftar Label

- **Method:** `GET`
- **URL:** `http://localhost:5001/model/info`
- Klik **Send**

**Response:**
```json
{
  "status": "ok",
  "total_classes": 5,
  "classes": ["info_jam_buka", "info_lokasi_wisata", "info_tiket_wisata", "rekomendasi_wisata", "ulasan_wisata"],
  "model_size_kb": 12.4,
  "vec_size_kb": 85.2,
  "model_trained_at": "2026-03-13T08:00:00Z"
}
```

---

### 5. Jika Menggunakan API Key

Tambahkan header di Postman:

1. Klik tab **Headers**
2. Tambahkan baris baru:

| Key | Value |
|---|---|
| `X-API-Key` | `rahasia123` |

---

### Troubleshooting Postman

| Error | Penyebab | Solusi |
|---|---|---|
| `Could not get response` | Server belum jalan | Jalankan `python intent_api.py` |
| `"status": "degraded"` | Model belum dilatih | Buka `app.py` → halaman **Latih Model** |
| `401 Unauthorized` | API Key salah / tidak ada | Tambahkan header `X-API-Key` yang benar |
| `400 Bad Request` | Body bukan JSON | Pastikan pilih **raw → JSON** di Postman |
| `400` field kosong | `text` tidak diisi | Pastikan body berisi field `text` yang tidak kosong |

---

## 🔄 Integrasi dengan n8n

### Konfigurasi HTTP Request Node (Single Predict)

| Setting | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `http://<server>:5001/predict` |
| **Authentication** | None *(atau Header Auth jika pakai API Key)* |
| **Body Content Type** | `JSON` |
| **Body** | `{ "text": "{{ $json.input_text }}" }` |

### Ambil Hasil di Node Berikutnya

| Field | Expression n8n |
|---|---|
| Intent | `{{ $json.intent }}` |
| Confidence | `{{ $json.confidence }}` |
| Status | `{{ $json.status }}` |

### Contoh Alur n8n

```
[Webhook] → [HTTP Request /predict] → [IF confidence > 80] → [aksi selanjutnya]
                                                           ↘ [fallback / eskalasi]
```

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan belajar. Silakan digunakan dan dimodifikasi sesuai kebutuhan.