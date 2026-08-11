from config import LEBAR_HEADER

def format_rupiah(angka):
    return f"Rp{angka:,.0f}".replace(",",".")

def header(judul):
    print("=" * LEBAR_HEADER)

    print(judul.center(LEBAR_HEADER))
    print("=" * LEBAR_HEADER)

def keluar():
    header("THANKS")