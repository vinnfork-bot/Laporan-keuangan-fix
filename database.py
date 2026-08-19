import sqlite3
from config import DATABASE_NAME

conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
cursor = conn.cursor()

def buat_tabel():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi_keuangan(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id TEXT NOT NULL,
       jenis TEXT NOT NULL,
       kategori TEXT NOT NULL,
       keterangan TEXT NOT NULL,
       jumlah INTEGER NOT NULL,
       tanggal TEXT DEFAULT CURRENT_DATE
       )
    """)
    conn.commit()
buat_tabel()

def tutup_database():
    conn.close()