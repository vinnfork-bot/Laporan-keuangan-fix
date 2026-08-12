DATABASE_NAME = "transaksi_keuangan.db"
TABLE_NAME = "Transaksi"

HEADER_TABEL = [
    "ID",
    "JENIS",
    "KATEGORI",
    "KETERANGAN",
    "JUMLAH",
    "TANGGAL"
]

LEBAR_HEADER = 75
FREEZE_PANES = "A2"

JENIS_MASUK = "MASUK"
JENIS_KELUAR = "KELUAR"

KATEGORI_MASUK = {
    "1" : "Gajian",
    "2" : "Freelance"
}

KATEGORI_KELUAR = {
    "1" : "Makan",
    "2" : "Transportasi",
    "3" : "Kuota",
    "4" : "Beli",
    "5" : "Lainnya"
}

WARNA_MASUK = "C6E0B4"
WARNA_KELUAR = "F8CECC"
WARNA_HEADER = "1F4E78"
FONT_HEADER = "FFFFFF"

POSISI_BAR = "H22"
POSISI_PIE = "H2"

JUDUL_PIE = "Perbandingan pemasukan \n   dan pengeluaran"
JUDUL_BAR = "Pengeluaran per kategori"

SHEET_GRAFIK = "Data Grafik"