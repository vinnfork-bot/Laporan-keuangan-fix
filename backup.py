import os
import shutil
from datetime import datetime
from config import DATABASE_NAME
from utils import header
from database import conn

def backup_database():
    header("BACKUP DATA")

    folder = "backup"

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    waktu = datetime.now().strftime("%Y-%m-%d")
    nama_file = f"BACKUP_DATA {waktu}.db"

    lokasi_backup = os.path.join(folder, nama_file)

    shutil.copy2(DATABASE_NAME, lokasi_backup)

    print(f"backup berhasil")
    print(f"file : {lokasi_backup}")

def restore_database():
    header("RESTRORE DATABASE")

    folder = "backup data"

    if not os.path.exists(folder):
        print("Folder belum ada")
        return

    file_backup = input("Masukkan nama file : ")

    lokasi_backup = os.path.join(folder, file_backup)

    if not os.path.exists(lokasi_backup):
        print("folder tidak ditemukan ")
        return

    konfirmasi = input(
        "WARNING!!!"
        "Database sekarang akan diganti"
        "lanjutkan? (y/n) : "
    )

    if konfirmasi.lower != 'y':
        print("Restorasi dibatalkan")
        return

    print("menutup databse")

    conn.close()

    shutil.copy2(lokasi_backup, "transaksi.db")

    print("database berhasil diubah")
    print("restart program")    