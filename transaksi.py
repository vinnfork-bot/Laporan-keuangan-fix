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
    pilihan = input(
        "1. PEMASUKAN\n"
        "2. PENGELUARAN\n"
        "pilih (1 atau 2) : "
    )

    while True:
        try:
            jumlah = int(input("MASUKKAN JUMLAH : "))
            break

        except ValueError:
            print("MASUKKAN ANGKA YANG BENAR")
            
    if pilihan == "1":
        jenis = JENIS_MASUK

        kategori = pilih_kategori(KATEGORI_MASUK)

        if kategori is None:
            return

        jumlah = abs(jumlah)

    elif pilihan == "2":
        jenis = JENIS_KELUAR

        kategori = pilih_kategori(KATEGORI_KELUAR)

        if kategori is None:
            return

        jumlah = -abs(jumlah)

    else:
        print("PILIHAN TIDAK TERSEDIA")
        return

    keterangan = input("KETERANGAN : ")

    return jenis, kategori, keterangan, jumlah


def simpan_transaksi(user_id, jenis, kategori, keterangan, jumlah):
    cursor.execute("""
        INSERT INTO transaksi_keuangan
        (user_id, jenis, kategori, keterangan, jumlah)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        jenis,
        kategori,
        keterangan,
        jumlah
    ))

    conn.commit()

    return cursor.lastrowid


def simpan_data():
    header("TRANSAKSI BARU")

    hasil = input_transaksi()

    if hasil is None:
        return

    jenis, kategori, keterangan, jumlah = hasil

    # Transaksi dari CLI
    user_id = "CLI"

    id_transaksi = simpan_transaksi(
        user_id,
        jenis,
        kategori,
        keterangan,
        jumlah
    )

    print(f"ID transaksi : {id_transaksi}")

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


def tampilkan_data(user_id="CLI"):
    cursor.execute("""
        SELECT id, jenis, kategori, keterangan, jumlah, tanggal
        FROM transaksi_keuangan
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        print("BELUM ADA TRANSAKSI")
        return

    data = format_data(rows)

    print(
        tabulate(
            data,
            headers=HEADER_TABEL,
            tablefmt="grid"
        )
    )


def tampilkan_menu(data):
    print(f"""
    ID          : {data[0]}
    Jenis       : {data[1]}
    Kategori    : {data[2]}
    Keterangan  : {data[3]}
    Jumlah      : {format_rupiah(abs(data[4]))}
    Tanggal     : {data[5]}
    """)


def edit(user_id="CLI"):
    try:
        id_edit = int(input("Masukkan id : "))

    except ValueError:
        print("INPUT BERUPA ANGKA!")
        return

    cursor.execute("""
        SELECT *
        FROM transaksi_keuangan
        WHERE id = ? AND user_id = ?
    """, (id_edit, user_id))

    data = cursor.fetchone()

    if data is None:
        print("DATA TIDAK DITEMUKAN")
        return

    tampilkan_menu(data)

    hasil = input_transaksi()

    if hasil is None:
        return

    jenis, kategori, keterangan, jumlah = hasil

    cursor.execute("""
        UPDATE transaksi_keuangan
        SET jenis = ?,
            kategori = ?,
            keterangan = ?,
            jumlah = ?
        WHERE id = ?
          AND user_id = ?
    """, (
        jenis,
        kategori,
        keterangan,
        jumlah,
        id_edit,
        user_id
    ))

    conn.commit()

    print("DATA BERHASIL DIUBAH!")


def hapus_data(user_id="CLI"):
    try:
        id_hapus = int(input("Masukkan Id : "))

    except ValueError:
        print("INPUT BERUPA ANGKA!")
        return

    cursor.execute("""
        SELECT *
        FROM transaksi_keuangan
        WHERE id = ? AND user_id = ?
    """, (id_hapus, user_id))

    data = cursor.fetchone()

    if data is None:
        print("DATA TIDAK DITEMUKAN")
        return

    tampilkan_menu(data)

    konfirmasi = input("YAKIN INGIN MENGHAPUS? (y/n) : ")

    if konfirmasi.upper() == "Y":

        cursor.execute("""
            DELETE FROM transaksi_keuangan
            WHERE id = ? AND user_id = ?
        """, (id_hapus, user_id))

        conn.commit()

        print("DATA BERHASIL DIHAPUS")

    else:
        print("DATA BATAL DIHAPUS")