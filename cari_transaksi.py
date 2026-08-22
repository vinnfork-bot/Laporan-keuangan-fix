from database import *
from tabulate import tabulate
from datetime import datetime
from utils import format_rupiah


def format_hasil_filter(rows):
   if not rows:
    return "Tidak ada transaksi yang cocok dengan filter."

   teks = "HASIL FILTER"
   for row in rows:
    teks += f"""\n
🆔 ID: {row[0]}
📁 Kategori: {row[3]}
📝 {row[4]}
💰 {format_rupiah(row[5])}
📅 {row[6]}"""

   return teks

def cari_transaksi(user_id, filters):
   
   query = """
SELECT *
FROM transaksi_keuangan
WHERE user_id = ?
"""

   kondisi = []
   values = [user_id]

   kategori = filters.get("kategori")
   keterangan = filters.get("keterangan")
   tanggal = filters.get("tanggal")

   if not (kategori or keterangan or tanggal):
    print("Minimal isi satu filter")
    return

   if kategori:
    kondisi.append("LOWER(kategori) = LOWER(?)")
    values.append(kategori)

   if keterangan:
    kondisi.append("keterangan LIKE ?")
    values.append(f"%{keterangan}%")

   if tanggal:
    tanggal = datetime.strptime(
        tanggal, 
        "%d-%m-%Y"
       ).strftime("%Y-%m-%d")
    kondisi.append("tanggal = ?")
    values.append(tanggal)

   query += " AND " + " AND ".join(kondisi)
   query += " ORDER BY tanggal DESC, id DESC"
   cursor.execute(query, values)

   hasil = cursor.fetchall()
   data = format_hasil_filter(hasil)
   print("QUERY:", query)
   print("VALUES:", values)
   return data
