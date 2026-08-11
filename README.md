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
  git clone  https://github.com/vinnfork-bot/Laporan-keuangan-fix.git
  
2. Masuk ke repositori
  cd Laporan-keuangan-fix

3. Install library
  pip install openpyexcel tabulate

4. Jalankan aplikasi
  python main.py

📊 Export Excel
Aplikasi dapat membuat laporan transaksi berdasarkan bulan dan tahun.
File laporan akan otomatis masuk ke dalam folder "export".
Laporan excel juga dilengkapin dengan:
  - Tabel transaksi
  - Total pemasukan
  - Total pengeluaran
  - Jumlah saldo
  - Grafik pemasukan dan pengeluaran
  - Grafik pengeluaran berdasarkan kategori

🔎 Pencarian Transaksi
Pencarian bisa dilakukan dengan menggunakan beberapa filter
  - Kategori
  - Keterangan
  - Tanggal
Filter ini bisa digunakan secara bersamaan ataupun salah satu

💾 Backup & Restore
Aplikasi menyediakan fitur Backup dan Restore untuk
menjaga keamanan data transaksi pengguna

🎯 Tujuan Project
Aplikasi ini dibuat sebagai sarana belajar dan pengembangan kemampuan dalam:
 - Python
 - Sqlite
 - Function dan modular programing
 - CRUD
 - File handling 
 - Git dan github
 - Export ke excel
 - Problem solving

📌 Status Project
Version 1.1
Proyek masih dalam tahap pengembangan yang akan dikembangkan lebih lanjut

🔮 Rencana Pengembangan
 - Integrasi dengan sistem lain
 - Memberikan UI/UX yang lebih praktis dan modern

👨‍💻 Author
Alvin