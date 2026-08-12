from database import conn, cursor
from utils import header, format_rupiah
from config import (
    HEADER_TABEL,
    KATEGORI_MASUK,
    KATEGORI_KELUAR,
    JENIS_KELUAR,
    JENIS_MASUK
    )
from tabulate import tabulate

def pilih_kategori(data):
   for kode, nama in data.items():
        print(f"{kode}. {nama}")
   kode = input("Pilih kategori : ")
   if kode not in data:
        print("PILIHAN TIDAK TERSEDIA")
        return None

   return data[kode]
   
def input_transaksi():
   pilihan = input("1. PEMASUKAN \n2. PENGELUARAN \npilih (1 atau 2) : ")
   while True:
    try:
      jumlah = int(input("MASUKKAN JUMLAH :"))
      break
     
    except ValueError:
      print("MASUKKAN ANGKA YANG BENAR")
      return

   if pilihan == "1":
        jenis = JENIS_MASUK
        kategori = pilih_kategori(KATEGORI_MASUK)
        if kategori is None:
           print("PILIHAN TIDAK TERSEDIA")
           return
        
        jumlah = abs(jumlah)
    
   elif pilihan == "2":
      jenis = JENIS_KELUAR
      kategori = pilih_kategori(KATEGORI_KELUAR)
      if kategori is None:
         print("MASUKKAN ANGKA YANGH BENAR")
         return
     
      jumlah = -abs(jumlah)

   else:
       print("PILIHAN TIDAK TERSEDIA")
       return

   keterangan = input("KETERANGAN : ")
   return jenis, kategori, keterangan, jumlah

def simpan_transaksi(jenis, kategori, keterangan, jumlah):
   cursor.execute('''
INSERT INTO transaksi_keuangan(jenis, kategori, keterangan, jumlah)
VALUES(?, ?, ?, ?)
''', (jenis, kategori, keterangan, jumlah))
   conn.commit()
   return cursor.lastrowid

def simpan_data():
  header("TRANSAKSI BARU")
  hasil = input_transaksi()

  if hasil is None:
     return 
  jenis, kategori, keterangan, jumlah = hasil

  id_transaksi = simpan_transaksi(
       jenis,
       kategori,
       keterangan,
       jumlah
    )
  print(f"id transaksi : {id_transaksi}")
     

  header("DATA DISIMPAN")

def format_data(rows):
   data = []
   
   for row in rows: 
         data.append([
            row[0],
            row[1],
            row[2],
            row[3],
            format_rupiah(abs(row[4])),
            row[5]
         ])
   return data

def tampilkan_data():
   cursor.execute('SELECT id, jenis, kategori, keterangan, jumlah, tanggal FROM transaksi_keuangan')
   rows = cursor.fetchall()

   data = format_data(rows)

   print(tabulate(data, headers=HEADER_TABEL, tablefmt="grid"))

def tampilkan_menu(data):
    print(f"""
               ID           :  {data[0]}
               jenis        :  {data[1]}
               kategori     :  {data[2]}
               keterangan   :  {data[3]}
               jumlah       :  {format_rupiah(abs(data[4]))}
               tanggal      :  {data[5]}
               """)

def edit():
   try:
    id_edit = int(input("Masukkan id : "))

   except ValueError:
      print("INPUT BERUPAA ANGKA!")
      return
   cursor.execute('SELECT * FROM transaksi_keuangan WHERE id = ?',
                  (id_edit,))

   data = cursor.fetchone()
   
   if data is None:
      print("DATA TIDAK DITEMUKAN")
      return

   else:
      tampilkan_menu(data)
      
      hasil = input_transaksi()
      
      if hasil is None:
           return 
      jenis, kategori, keterangan, jumlah = hasil
      
   cursor.execute('''
            UPDATE transaksi_keuangan
            SET jenis=?,
             kategori=?,
             keterangan=?,
             jumlah=?
         WHERE id=?
      ''',
     (jenis, kategori, keterangan, jumlah, id_edit))      
   conn.commit()
   print("Data berhasil diubah!!!")

def hapus_data():
   try:
    id_hapus = int(input("Masukkan Id : "))

   except ValueError:
      print("INPUT BERUPAA ANGKA!")
      return
   cursor.execute('SELECT * FROM transaksi_keuangan WHERE id = ?',
                  (id_hapus,)
                  )

   data = cursor.fetchone()

   if data is None:
      print("DATA TIDAK DITEMUKAN")
      return

   tampilkan_menu(data)

   konfirmasi = input("YAKIN INGIN MENGHAPUS? (y/n) : ")

   if konfirmasi.upper() == "Y":
      cursor.execute(
         "DELETE FROM transaksi_keuangan WHERE id = ?",
         (id_hapus,)
      )

      conn.commit()
      print("DATA BERHASIL DIHAPUS")

   else:
      print("DATA BATAL DIHAPUS")

