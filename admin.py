import os
from data import admin, petugas, dokumen, save_csv, petugas_path, dokumen_path

# ==============================
# LOGIN ADMIN DARI CSV
# ==============================

def admin_login():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== LOGIN ADMIN ===")
        u = input("Username: ")
        p = input("Password: ")

        ditemukan = False

        # cek ke CSV admin
        for a in admin:
            if a["username"] == u and a["password"] == p:
                ditemukan = True
                break

        if ditemukan:
            print("\nLogin berhasil!")
            input("Tekan Enter untuk lanjut...")
            return True
        else:
            print("\nUsername atau password salah!")
            input("Tekan Enter untuk coba lagi...")


# ==============================
# MENU ADMIN
# ==============================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu_admin():
    # login dulu
    admin_login()

    while True:
        clear()
        print("=== MENU ADMIN ===")
        print("1. Lihat petugas")
        print("2. Tambah petugas")
        print("3. Lihat jenis dokumen")
        print("4. Tambah jenis dokumen")
        print("0. Kembali")

        p = input("Pilih: ")

        if p == "1":
            clear()
            print("=== DAFTAR PETUGAS ===")
            for x in petugas:
                print("-", x["nama"])
            input("\nTekan Enter untuk kembali...")

        elif p == "2":
            clear()
            print("=== TAMBAH PETUGAS ===")
            nama = input("Nama petugas: ")
            petugas.append({"nama": nama, "password": "1234"})  # password default
            save_csv(petugas_path, ["nama", "password"], petugas)
            print("\nPetugas berhasil ditambahkan! (Password default: 1234)")
            input("Tekan Enter untuk kembali...")

        elif p == "3":
            clear()
            print("=== JENIS DOKUMEN ===")
            for x in dokumen:
                print("-", x["jenis"])
            input("\nTekan Enter untuk kembali...")

        elif p == "4":
            clear()
            print("=== TAMBAH JENIS DOKUMEN ===")
            jenis = input("Jenis dokumen baru: ")
            dokumen.append({"jenis": jenis})
            save_csv(dokumen_path, ["jenis"], dokumen)
            print("\nDokumen baru berhasil ditambahkan!")
            input("Tekan Enter untuk kembali...")

        elif p == "0":
            break
