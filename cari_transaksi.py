from database import *
from transaksi import format_data
from tabulate import tabulate
from config import HEADER_TABEL
from datetime import datetime
from utils import header
from transaksi import format_data

def cari_transaksi():
   header("CARI TRANSAKSI")
   
   query = """
SELECT *
FROM transaksi
"""

   filters = []
   values = []

   kategori = input("MASUKKAN KATEGORI : ")
   keterangan = input("MASUKKAN KETERANGAN : ")
   tanggal = input("MASUKKAN TANGGAL, BULAN, DAN TAHUN : ")

   if not (kategori or keterangan or tanggal):
    print("Minimal isi satu filter")
    return

   if kategori:
    filters.append("LOWER(kategori) = LOWER(?)")
    values.append(kategori)

   if keterangan:
    filters.append("keterangan LIKE ?")
    values.append(f"%{keterangan}%")

   if tanggal:
    tanggal = datetime.strptime(
        tanggal, 
        "%d-%m-%Y"
       ).strftime("%Y-%m-%d")
    filters.append("tanggal = ?")
    values.append(tanggal)

   query += " WHERE " + " AND ".join(filters)
   query += " ORDER BY tanggal DESC, id DESC"
   cursor.execute(query, values)

   hasil = cursor.fetchall()
   data = format_data(hasil)

   print(tabulate(
    data,
    headers= HEADER_TABEL,
    tablefmt="grid"
   ))

