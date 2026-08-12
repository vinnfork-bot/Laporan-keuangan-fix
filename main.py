from transaksi import (
    simpan_data,
    tampilkan_data,
    edit,
    hapus_data
)

from laporan import rekap_bulanan, tampilkan_saldo
from export_excel import export_to_excel
from utils import header, keluar
from database import conn
from backup import *
from cari_transaksi import cari_transaksi
from parser import parse_pesan
while True:
    header("keuangan")

    print("""
1. tambah transaksi
2. lihat riwayat transaksi
3. lihat total saldo
4. edit transaksi
5. hapus transaksi
6. rekap bulanan
7. ekspor ke excel
8. cari transaksi
9. backup database
10. restore database
11. parser pesan
0. keluar
""")
    

    menu = input("Pilih Menu : ")

    if menu == '1':
     simpan_data()

    elif menu == '2':
     tampilkan_data()

    elif menu == '3':
      tampilkan_data()
      tampilkan_saldo()

    elif menu == '4':
      edit()

    elif menu == '5':
      hapus_data()

    elif menu == '6':
      rekap_bulanan()

    elif menu == '7':
      export_to_excel()

    elif menu == '8':
      cari_transaksi()

    elif menu == '9':
      backup_database()

    elif menu == '10':
      restore_database()

    elif menu == '11':
      pesan = input("Pesan : ")
      parse_pesan(pesan)

    elif menu == '0':
      keluar()
      break

    else:
      print("PILIHAN TIDAK ADA")
      

conn.close()