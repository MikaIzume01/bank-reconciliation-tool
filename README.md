# Bank Reconciliation Tool (Aplikasi Rekonsiliasi Bank Otomatis)

Aplikasi web berbasis Python Flask dan Pandas untuk membantu proses rekonsiliasi bank (Bank Reconciliation Statement) secara otomatis antara mutasi rekening koran dan buku besar (general ledger) perusahaan.

## 🚀 Fitur
- Unggah file CSV mutasi bank dan buku besar.
- Pencocokan transaksi otomatis (exact match) berdasarkan nominal dan keterangan.
- Laporan otomatis: transaksi yang sudah cocok, belum tercatat di buku besar, dan belum masuk mutasi bank.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Pandas
- **Frontend:** HTML5, CSS3
- **Data:** File CSV

## ⚙️ Cara Menjalankan
1. Install dependensi:
   ```bash
   pip install flask pandas
   ```
2. Jalankan aplikasi:
   ```bash
   python app.py
   ```
3. Buka di browser: `http://127.0.0.1:5001`
4. Unggah file contoh `sample_bank.csv` dan `sample_ledger.csv` yang disertakan untuk mencoba.

## 📋 Contoh Format CSV
- Kolom wajib: `tanggal`, `keterangan`, `jumlah` (format angka tanpa titik/koma ribuan).
