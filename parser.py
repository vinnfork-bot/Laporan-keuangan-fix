from transaksi import simpan_transaksi
from laporan import ambil_saldo
from config import *
from utils import format_rupiah

def parse_pesan(pesan, user_id):
    bagian = pesan.split()

    kategori_input = bagian[0]
    try:
       jumlah = int(bagian[-1])

    except ValueError:
        print("Jumlah tidak valid \ncontoh : \nmakan bakso Rp 10.000")
        return
    keterangan = " ".join(bagian[1:-1])

    kategori = None

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
      print("\nkategori tidak ditemukan")
      print("kategori yang tersedia :")
      print("gajian \nfreelance \nmakan \ntransportasi \nkuota \nlainnya")
      return
    
    simpan_transaksi(
       user_id,
       jenis,
       kategori,
       keterangan,
       jumlah
    )

    saldo = ambil_saldo()

    respon = buat_respon(
      jenis,
      kategori,
      keterangan,
      jumlah, 
      saldo
    )

    print(respon)

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

def kirim_ke_whatsapp(nomor, pesan):
  pass