# 🧠 Intent Dataset Manager

Sistem manajemen dataset dan pelatihan model machine learning untuk klasifikasi intent berbasis teks. Dibangun dengan **Python (Flask)** sebagai back-end dan **HTML + TailwindCSS + Vanilla JavaScript** sebagai front-end.

---

## 📌 Fitur Utama

| Fitur | Deskripsi |
|---|---|
| 📋 **Kelola Dataset** | Lihat, tambah, ubah, dan hapus data intent dari file `dataset.json` |
| ⚡ **Latih Model** | Buat model intent (`.pkl`) menggunakan TF-IDF + Logistic Regression |
| 🔮 **Uji Prediksi** | Tes model secara langsung dari antarmuka web |
| 📊 **Statistik** | Distribusi label dan ringkasan dataset |

---

## 🗂️ Struktur Proyek

```
intent-manager/
│
├── app.py                  # Back-end Flask (API server)
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

**Prediksi tidak bisa dilakukan:**
- Model belum dilatih — buka halaman **Latih Model** dan klik **Mulai Training**

**Data tidak tersimpan:**
- Pastikan file `dataset.json` ada di direktori yang sama dengan `app.py`
- Pastikan Python memiliki izin tulis pada direktori tersebut

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan belajar. Silakan digunakan dan dimodifikasi sesuai kebutuhan.
