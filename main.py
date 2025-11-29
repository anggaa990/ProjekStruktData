import os
from admin import menu_admin
from petugas import menu_petugas
from warga import menu_warga

def clear():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    clear()
    print("\n=== SISTEM MANAJEMEN DOKUMEN ===")
    print("1. Admin")
    print("2. Petugas")
    print("3. Warga")
    print("0. Keluar")

    p = input("Pilih role: ")

    if p == "1":
        menu_admin()     

    elif p == "2":
        menu_petugas()   

    elif p == "3":
        menu_warga()    

    elif p == "0":
        print("Program selesai.")
        break
