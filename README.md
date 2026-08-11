# Aplikasi Keuangan 
Aplikasi pencatat keuangan berbasis python dan Sqlite.
Aplikasi ini dibuat sebagai proyek portofolio dan perkembangan
saya dalam belajar Python, Database, Sqlite, dan pengembangan 
aplikasi secara modular, yang dapat membantu mempermudah 
pekerjaan dalam membuat laporan data.

## Fitur
- Tambah transaksi pemasukan dan pengeluaran
- Melihat riwayat transaksi
- Melihat total saldo
- Edit transaksi
- Hapus transaksi
- Rekap transaksi bulanan
- Ekspor ke bentuk file excel
- Mencari transaksi berdasarkan
   - Kategori
   - Keterangan
   - Tanggal
- Backup database
- Restore database
- Grafik pemasukan dan pengeluaran
- Menyimpan data menggunakan Sqlite


## Teknologi
- Python
- SQLite
- OpenPyXL
- Tabulate

## 📁 Struktur Project

```text
APLIKASI KEUANGAN V1.0/
│
├── main.py              # Program utama
├── database.py          # Koneksi dan database
├── transaksi.py         # Fungsi transaksi
├── laporan.py           # Laporan dan saldo
├── cari_transaksi.py    # Pencarian transaksi
├── export_excel.py      # Export ke Excel dan grafik
├── backup.py            # Backup dan restore database
├── config.py            # Konfigurasi aplikasi
├── utils.py             # Fungsi bantuan
├── backup/              # Penyimpanan backup database
├── export/              # Penyimpanan file Excel
└── README.md            # Dokumentasi project

## 📁 Cara menjalankan

1. Clone repositori
  git clone https://github.com/USERNAME/NAMA-REPOSITORY.git

2. Masuk ke repositori
  cd NAMA-REPOSITORY