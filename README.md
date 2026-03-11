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

---

## 🗂️ Struktur Proyek

```
intent-manager/
│
├── app.py                  # Back-end Flask (API server)
├── predict_cli.py          # Contoh implementasi prediksi via terminal
├── dataset.json            # Dataset intent (teks + label)
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

**Prediksi tidak bisa dilakukan (web):**
- Model belum dilatih — buka halaman **Latih Model** dan klik **Mulai Training**

**`predict_cli.py` gagal — "File model tidak ditemukan":**
- Jalankan `python app.py`, buka `http://localhost:5000`, latih model terlebih dahulu
- Pastikan `predict_cli.py` berada di folder yang sama dengan `intent_model.pkl` dan `vectorizer.pkl`

**Data tidak tersimpan:**
- Pastikan file `dataset.json` ada di direktori yang sama dengan `app.py`
- Pastikan Python memiliki izin tulis pada direktori tersebut

---

## 🖥️ Contoh Implementasi — Prediksi via Terminal

File `predict_cli.py` adalah contoh implementasi langsung dari model yang sudah dilatih (`intent_model.pkl` + `vectorizer.pkl`), tanpa memerlukan server Flask.

### Prasyarat

Pastikan model sudah dilatih terlebih dahulu melalui aplikasi web (`python app.py` → halaman **Latih Model**).

### Menjalankan

```bash
python predict_cli.py
```

### Tampilan di Terminal

```
╔══════════════════════════════════════════════════════╗
║          🧠  Intent Prediction CLI                   ║
║          Model: TF-IDF + Logistic Regression         ║
╚══════════════════════════════════════════════════════╝

  Memuat model... ✓  (12 intent dimuat)

  ➤ Masukkan teks: dimana lokasi Kawah Putih Bandung

  ────────────────────────────────────────────────────

  📝 Teks     : "dimana lokasi Kawah Putih Bandung"

  🎯 Intent   :  info_lokasi_wisata

  📊 Confidence:
     ████████████████████████░░░░░░  82.4%

  🏆 Top-3 Kandidat:
     ▶ info_lokasi_wisata          ████████████████████  82.4%
       info_tiket_wisata           ████░░░░░░░░░░░░░░░░  12.1%
       rekomendasi_wisata          ██░░░░░░░░░░░░░░░░░░   5.5%

  ────────────────────────────────────────────────────
```

### Perintah Khusus dalam CLI

| Perintah | Fungsi |
|---|---|
| `exit` / `quit` / `q` | Keluar dari program |
| `help` | Tampilkan daftar perintah |
| `clear` | Bersihkan layar terminal |
| `Ctrl+C` | Paksa keluar |

### Cara Kerja

`predict_cli.py` memuat `intent_model.pkl` dan `vectorizer.pkl` menggunakan `pickle`, kemudian untuk setiap teks yang dimasukkan:

1. Teks di-*transform* menggunakan **TF-IDF Vectorizer**
2. Vektor dimasukkan ke **Logistic Regression** untuk mendapat prediksi intent
3. Probabilitas tiap kelas dihitung untuk menampilkan **confidence score** dan **top-3 kandidat**

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan belajar. Silakan digunakan dan dimodifikasi sesuai kebutuhan.