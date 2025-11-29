import csv
import os

# ==========================================
# FUNGSI LOAD & SAVE CSV
# ==========================================

def load_csv(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_csv(path, fieldnames, rows):
    # pastikan folder ada
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# ==========================================
# LOKASI FILE CSV
# ==========================================

admin_path   = "database/admin.csv"       
petugas_path = "database/petugas.csv"
dokumen_path = "database/dokumen.csv"
antrian_path = "database/antrian.csv"
warga_path   = "database/warga.csv"
riwayat_path = "database/riwayat.csv"    


admin   = load_csv(admin_path)
petugas = load_csv(petugas_path)
dokumen = load_csv(dokumen_path)
antrian = load_csv(antrian_path)
warga   = load_csv(warga_path)
riwayat = load_csv(riwayat_path)
