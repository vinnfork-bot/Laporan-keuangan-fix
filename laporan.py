from transaksi import format_data
from database import conn, cursor
from tabulate import tabulate
from config import HEADER_TABEL
from utils import format_rupiah

def header(judul):
   print("=" * 75)
   print(judul.center(75))
   print("=" * 75)

def ambil_saldo():
  cursor.execute('''
SELECT COALESCE(SUM(jumlah), 0)
FROM transaksi_keuangan
''')
  saldo = cursor.fetchone()[0]
  return saldo

def tampilkan_saldo():
     cursor.execute("SELECT SUM(jumlah) FROM transaksi_keuangan")
     total_saldo = cursor.fetchone()[0]
     if total_saldo is None:
         total_saldo =0
     
     print("TOTAL SALDO ANDA ADALAH :")
     print(format_rupiah(total_saldo))
     print(" ")
     print("=" * 75)

def rekap_bulanan():
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
                 SELECT *
                 FROM transaksi_keuangan
                 WHERE strftime('%m', tanggal) = ?
                 AND strftime('%Y', tanggal) = ?
                 """,(bulan, tahun))

   hasil = cursor.fetchall()

   total_masuk = 0
   total_keluar = 0

   data = format_data(rows=hasil)

   for row in hasil:
       if row[1] == "MASUK":
           total_masuk += row[4]
       else:
           total_keluar += abs(row[4])

   print(tabulate(
      data,
      headers=HEADER_TABEL, 
      tablefmt="grid"))

   total_saldo = total_masuk - total_keluar
   print("\nTOTAL PEMASUKAN ANDA BULAN INI ADALAH : ", format_rupiah(total_masuk))
   print("\nTOTAL PENGELUARAN ANDA BULAN INI ADALAH : ", format_rupiah(total_keluar))
   print("\nTOTAL SALDO ANDA BULAN INI ADALAH : ", format_rupiah(total_saldo))