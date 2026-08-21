from transaksi import format_data
from database import conn, cursor
from tabulate import tabulate
from config import HEADER_TABEL
from utils import format_rupiah

def header(judul):
   print("=" * 75)
   print(judul.center(75))
   print("=" * 75)

def ambil_saldo(user_id):
  cursor.execute("""
SELECT COALESCE(SUM(jumlah), 0)
FROM transaksi_keuangan
WHERE user_id = ?
""", (user_id,))
  saldo = cursor.fetchone()[0]
  return saldo

def tampilkan_saldo(user_id):
     
     cursor.execute("""
          SELECT COALESCE SUM(jumlah)
          FROM transaksi_keuangan
          WHERE user_id = ?
          """,(user_id)
          )
     total_saldo = cursor.fetchone()[0]
     if total_saldo is None:
         total_saldo =0
     
     print("TOTAL SALDO ANDA ADALAH :")
     print(format_rupiah(total_saldo))
     print(" ")
     print("=" * 75)

def rekap_bulanan(user_id):
   header("Rekapan bulanan")
   try:
     bulan = input("Masukkan bulan : ")

     bulan = int(bulan)

     if bulan < 1 or bulan > 12:
             print("MASUKKAN BULAN YANG BENAR")
             return
     
     bulan = f"{int(bulan):02d}"
   
   except ValueError:
     print("MASUKKAN ANGKA YANG BENAR")
     return

   tahun = input("Masukkan tahun : ")

   print("\n \nmencari transaksi bulan ",(bulan)," pada tahun ",(tahun))

   cursor.execute("""
    SELECT id, jenis, kategori, keterangan, jumlah, tanggal
    FROM transaksi_keuangan
    WHERE strftime('%m', tanggal) = ?
    AND strftime('%Y', tanggal) = ?
    AND user_id = ?
""", (bulan, tahun, user_id))

   hasil = cursor.fetchall()

   total_masuk = 0
   total_keluar = 0

   data = format_data(rows=hasil)

   for row in hasil:
       if row[2] == "MASUK":
           total_masuk += row[5]
       else:
           total_keluar += abs(row[5])

   print(tabulate(
      data,
      headers=HEADER_TABEL, 
      tablefmt="grid"))

   total_saldo = total_masuk - total_keluar
   print("\nTOTAL PEMASUKAN ANDA BULAN INI ADALAH : ", format_rupiah(total_masuk))
   print("\nTOTAL PENGELUARAN ANDA BULAN INI ADALAH : ", format_rupiah(total_keluar))
   print("\nTOTAL SALDO ANDA BULAN INI ADALAH : ", format_rupiah(total_saldo))

def ambil_riwayat(user_id):
  cursor.execute("""
SELECT
id,
jenis,
kategori,
keterangan,
jumlah,
tanggal
FROM transaksi_keuangan
WHERE user_id = ?
ORDER BY id DESC
LIMIT 10
""", (user_id,))

  rows = cursor.fetchall()

  if not rows:
    return """Tidak ada transaksi"""

  teks = "📋 RIWAYAT TRANSAKSI\n\n"

  for row in rows:
    id_transaksi = row[0]
    jenis = row[1]
    kategori = row[2]
    keterangan = row[3]
    jumlah = row[4]
    tanggal = row[5]

    if jumlah >= 0:
      simbol = "📥"

    else:
       simbol = "📤"

    teks += f"""\n 🆔 ID: {id_transaksi}
{simbol} {kategori}
📝 {keterangan}
💰 {format_rupiah(abs(jumlah))}
📅 {tanggal}
"""

  return teks
