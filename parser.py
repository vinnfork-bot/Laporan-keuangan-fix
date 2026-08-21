from transaksi import simpan_transaksi, hapus_data, tampilkan_data, konfirmasi_data
from laporan import ambil_saldo, ambil_riwayat
from config import *
from utils import format_rupiah
from database import cursor

def parse_pesan(pesan, user_id):
    pesan = pesan.lower().strip()

    if pesan == "hai":
      return "Hai bozs \nAda yang bisa gw bantu? \nKetik *menu* untuk melihat perintah"

    if pesan == "menu":
      return """📱MENU KEUANGAN
      Ketik :
      -Saldo
      -Riwayat
      -Tambah
      -Hapus
      """
    if pesan == "saldo":
      saldo = ambil_saldo(user_id)
      return f"""💳 SALDO ANDA
      Saldo anda saat ini : 
      {format_rupiah(saldo)}
"""
    if pesan == "riwayat":
      return ambil_riwayat(user_id)

    if pesan.startswith("hapus"):
      bagian = pesan.split()

      if len(bagian) != 2:
        return "❌ Format salah.\nContoh: hapus 3"

      id_hapus = bagian[1]

      return hapus_data(user_id, id_hapus)

    if pesan.startswith("ya"):
      bagian = pesan.split()

      if len(bagian) != 2:
        return "Format salah.\nContoh :\nYa 1"
      id_hapus = bagian[1]
      return konfirmasi_data(user_id, id_hapus)

    if pesan.startswith("tidak"):
      bagian = pesan.split()

      if len(bagian) != 2:
        return "Format salah.\nContoh :\nYa 1"
      return "Penghapusan transaksi dibatalkan"

    if pesan == "tambah":
      return """TAMBAH TRANSAKSI :
      format : <kategori> <keterangan> <jumlah>
      
      contoh:
      Makan bakso 15000
      📥 PEMASUKAN
- gajian
- freelance

📤 PENGELUARAN
- makan
- transportasi
- kuota
- lainnya
      """
    bagian = pesan.split()

    if len(bagian) < 2:
      return """format tidak valid
      ketik *menu* untuk bantuan"""

    kategori_input = bagian[0]
    try:
       jumlah = int(bagian[-1])

    except ValueError:
        print("Jumlah tidak valid \ncontoh : \nmakan bakso Rp 10.000 \nKetik 'menu' untuk melihat bantuan")
        return
    keterangan = " ".join(bagian[1:-1])

    kategori = None
    jenis = None

    for nama in KATEGORI_MASUK.values():
     if kategori_input.lower() == nama.lower():
        kategori = nama
        jenis = JENIS_MASUK
        jumlah = abs(jumlah)
        break
    
    for nama in KATEGORI_KELUAR.values():
      if kategori_input.lower() == nama.lower():
        kategori = nama
        jenis = JENIS_KELUAR
        jumlah = -abs(jumlah)
        break

    if kategori is None:
      return """Kategori tidak ditemukan
      KATEGORI YANG ADA:
      📥 Pemasukan
- gajian
- freelance

📤 Pengeluaran
- makan
- transportasi
- kuota
- lainnya"""
    
    simpan_transaksi(
       user_id,
       jenis,
       kategori,
       keterangan,
       jumlah
    )

    saldo = ambil_saldo(user_id)

    respon = buat_respon(
      jenis,
      kategori,
      keterangan,
      jumlah, 
      saldo
    )

    return respon

def buat_respon(jenis, kategori, keterangan, jumlah, saldo):
  if jenis == JENIS_MASUK:
    teks_jenis = "Pemasukan"

  else:
    teks_jenis = "Pengeluaran"

  return f"""
✅ Transaksi berhasil disimpan!

📊 Jenis       : {teks_jenis}
📁 Kategori    : {kategori}
📝 Keterangan  : {keterangan}
💰 Jumlah      : {format_rupiah(abs(jumlah))}

💳 Saldo sekarang: {format_rupiah(saldo)}
"""
