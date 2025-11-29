import os
import uuid
from data import dokumen, antrian, save_csv, antrian_path, warga, warga_path, riwayat, riwayat_path

# ==========================================
# FUNGSI CLEAR
# ==========================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# REGISTER WARGA
# ==========================================
def register_warga():
    while True:
        clear()
        print("=== REGISTER WARGA ===")
        nama = input("Nama lengkap: ")
        password = input("Password: ")

        for w in warga:
            if w["nama"].lower() == nama.lower():
                print("\nNama sudah digunakan!")
                input("Tekan Enter...")
                return

        warga.append({"nama": nama, "password": password})
        save_csv(warga_path, ["nama", "password"], warga)

        print("\nRegistrasi berhasil!")
        input("Tekan Enter...")
        return


# ==========================================
# LOGIN WARGA
# ==========================================
def login_warga():
    while True:
        clear()
        print("=== LOGIN WARGA ===")
        nama = input("Nama: ")
        pw = input("Password: ")

        for w in warga:
            if w["nama"].lower() == nama.lower() and w["password"] == pw:
                print("\nLogin berhasil!")
                input("Tekan Enter...")
                return w["nama"]

        print("\nNama atau password salah!")
        input("Tekan Enter...")


# ==========================================
# MENU WARGA
# ==========================================
def menu_warga():
    # login/register
    while True:
        clear()
        print("=== AKSES WARGA ===")
        print("1. Login")
        print("2. Register")
        print("0. Kembali")

        pil = input("Pilih: ")

        if pil == "1":
            nama_login = login_warga()
            break
        elif pil == "2":
            register_warga()
        elif pil == "0":
            return

    # setelah login
    while True:
        clear()
        print(f"=== MENU WARGA ({nama_login}) ===")
        print("1. Buat Pengajuan Dokumen")
        print("2. Lihat Status Semua Pengajuan")
        print("0. Logout")

        p = input("Pilih: ")

        # ---------------------------------
        # BUAT PENGAJUAN
        # ---------------------------------
        if p == "1":
            clear()
            print("=== PENGAJUAN DOKUMEN ===")
            print("Nama:", nama_login)

            print("\nPilih jenis dokumen:")
            for i, d in enumerate(dokumen):
                print(f"{i+1}. {d['jenis']}")

            idx = int(input("\nPilih nomor: ")) - 1
            jenis = dokumen[idx]['jenis']

            # nomor antrian berurutan
            if antrian:
                last_id = max(int(a["id"]) for a in antrian)
            else:
                last_id = 0
            nomor = str(last_id + 1)

            antrian.append({
                "id": nomor,
                "nama": nama_login,
                "dokumen": jenis,
                "status": "Menunggu"
            })

            save_csv(antrian_path, ["id", "nama", "dokumen", "status"], antrian)

            print("\nPengajuan berhasil!")
            print("Nomor Antrian:", nomor)
            input("\nTekan Enter...")

        # ---------------------------------
        # LIHAT STATUS SEMUA PENGAJUAN
        # ---------------------------------
        elif p == "2":
            clear()
            print(f"=== STATUS PENGAJUAN {nama_login} ===")

            found = False

            # cek antrian aktif
            for a in antrian:
                if a["nama"].lower() == nama_login.lower():
                    found = True
                    print(f"[Menunggu] ID: {a['id']} | Dokumen: {a['dokumen']}")

            # cek riwayat
            for r in riwayat:
                if r["nama"].lower() == nama_login.lower():
                    found = True
                    print(f"[{r['status']}] ID: {r['id']} | Dokumen: {r['dokumen']}")

            if not found:
                print("Belum ada pengajuan.")

            input("\nTekan Enter...")

        elif p == "0":
            return
