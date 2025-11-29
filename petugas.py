import os
from data import antrian, riwayat, save_csv, antrian_path, riwayat_path, petugas, dokumen

# ==========================================
# FUNGSI CLEAR
# ==========================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ==========================================
# LOGIN PETUGAS
# ==========================================
def petugas_login():
    while True:
        clear()
        print("=== LOGIN PETUGAS ===")
        nama = input("Nama petugas: ")
        pw = input("Password: ")

        for p in petugas:
            if p["nama"].lower() == nama.lower() and p["password"] == pw:
                print("\nLogin berhasil!")
                input("Tekan Enter...")
                return p["nama"]

        print("\nNama atau password salah!")
        input("Tekan Enter...")


# ==========================================
# MENU PETUGAS
# ==========================================
def menu_petugas():
    nama_petugas = petugas_login()

    while True:
        clear()
        print(f"=== MENU PETUGAS ({nama_petugas}) ===")
        print("1. Lihat Antrian")
        print("2. Proses Antrian")
        print("0. Logout")

        pilihan = input("Pilih: ")

        # ---------------------------
        # LIHAT ANTRIAN
        # ---------------------------
        if pilihan == "1":
            clear()
            print("=== DAFTAR ANTRIAN ===")
            if not antrian:
                print("Tidak ada antrian.")
            else:
                for i, a in enumerate(antrian, start=1):
                    print(f"{i}. ID: {a['id']} | Nama: {a['nama']} | Dokumen: {a['dokumen']} | Status: {a['status']}")
            input("\nTekan Enter...")

        # ---------------------------
        # PROSES ANTRIAN
        # ---------------------------
        elif pilihan == "2":
            if not antrian:
                clear()
                print("Tidak ada antrian.")
                input("\nTekan Enter...")
                continue

            # ambil antrian paling depan (FIFO)
            proses = antrian[0]

            clear()
            print("=== PROSES ANTRIAN ===")
            print(f"ID       : {proses['id']}")
            print(f"Nama     : {proses['nama']}")
            print(f"Dokumen  : {proses['dokumen']}")
            print(f"Status   : {proses['status']}")

            print("\n1. Setujui / Selesai")
            print("2. Batalkan")
            print("0. Kembali")

            aksi = input("Pilih aksi: ")

            if aksi == "1":
                # update status menjadi selesai dan pindahkan ke riwayat
                proses["status"] = "Selesai"
                riwayat.append(proses)
                antrian.pop(0)
                save_csv(antrian_path, ["id","nama","dokumen","status"], antrian)
                save_csv(riwayat_path, ["id","nama","dokumen","status"], riwayat)
                print(f"\nPengajuan ID {proses['id']} berhasil diselesaikan.")

            elif aksi == "2":
                proses["status"] = "Dibatalkan"
                riwayat.append(proses)
                antrian.pop(0)
                save_csv(antrian_path, ["id","nama","dokumen","status"], antrian)
                save_csv(riwayat_path, ["id","nama","dokumen","status"], riwayat)
                print(f"\nPengajuan ID {proses['id']} dibatalkan.")

            else:
                print("\nAksi dibatalkan.")

            input("\nTekan Enter...")

        # ---------------------------
        # LOGOUT
        # ---------------------------
        elif pilihan == "0":
            break
