import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
import csv
import os
from datetime import datetime

# ==========================================
# KONFIGURASI TEMA & UI
# ==========================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLOR_PRIMARY = "#1e3d59"   
COLOR_ACCENT  = "#17a2b8"   
COLOR_SUCCESS = "#28a745"   
COLOR_WARNING = "#ffc107"   
COLOR_DANGER  = "#dc3545"   
COLOR_CARD    = "#2f3640"   

FONT_HEADER = ("Roboto", 24, "bold")
FONT_SUBHEAD = ("Roboto", 18, "bold")
FONT_BODY = ("Roboto", 12)
FONT_BOLD = ("Roboto", 12, "bold")
FONT_BUTTON = ("Roboto", 13, "bold")
FONT_MONO = ("Courier New", 12)

# ==========================================
# DATABASE & LOGIC
# ==========================================

PATHS = {
    "admin": "database/admin.csv",
    "petugas": "database/petugas.csv",
    "dokumen": "database/dokumen.csv",
    "antrian": "database/antrian.csv",
    "warga": "database/warga.csv",
    "riwayat": "database/riwayat.csv"
}

PRIORITY_MAP = {"Darurat": 1, "Ibu Hamil": 2, "Lansia": 3, "Umum": 4}

FIELDNAMES_ANTRIAN = [
    "id", "waktu", "nama", "nik", "telepon", "alamat", 
    "dokumen", "kategori", "deskripsi", "status"
]

def load_csv(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0: return []
    with open(path, newline='', encoding='utf-8') as f: return list(csv.DictReader(f))

def save_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

DATA = {
    "admin": load_csv(PATHS["admin"]),
    "petugas": load_csv(PATHS["petugas"]),
    "dokumen": load_csv(PATHS["dokumen"]),
    "antrian": load_csv(PATHS["antrian"]),
    "warga": load_csv(PATHS["warga"]),
    "riwayat": load_csv(PATHS["riwayat"])
}

if not DATA["admin"]:
    DATA["admin"].append({"username": "admin", "password": "admin"})
    save_csv(PATHS["admin"], ["username", "password"], DATA["admin"])
if not DATA["dokumen"]:
    DATA["dokumen"] = [{"jenis": "KTP"}, {"jenis": "Kartu Keluarga"}, {"jenis": "Akta Kelahiran"}]
    save_csv(PATHS["dokumen"], ["jenis"], DATA["dokumen"])

# ==========================================
# APLIKASI UTAMA
# ==========================================

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Informasi Manajemen Dokumen Terpadu")
        self.geometry("1200x800")
        self.center_window(1200, 800)
        
        self.setup_treeview_style()
        self.show_main_menu()
        
        self.clock_label = None
        self.update_clock()

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def reset_window_size(self):
        self.after(100, lambda: self.geometry("1200x800"))
        self.after(100, lambda: self.center_window(1200, 800))

    def clear_window(self):
        for widget in self.winfo_children(): widget.destroy()

    def setup_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=35, fieldbackground="#2b2b2b", font=("Roboto", 11))
        style.configure("Treeview.Heading", background="#1e3d59", foreground="white", font=("Roboto", 11, "bold"))
        style.map("Treeview", background=[('selected', '#17a2b8')])
        style.configure("Darurat.Treeview", foreground="#dc3545", font=("Roboto", 11, "bold"))

    def update_clock(self):
        now = datetime.now().strftime("%d-%m-%Y  |  %H:%M:%S WIB")
        if self.clock_label:
            self.clock_label.configure(text=now)
        self.after(1000, self.update_clock)

    def get_sorted_queue(self):
        def sort_key(item):
            prio = PRIORITY_MAP.get(item.get("kategori", "Umum"), 4)
            try: id_val = int(item["id"])
            except: id_val = 999999
            return (prio, id_val)
        return sorted(DATA["antrian"], key=sort_key)

    def create_sidebar_btn(self, parent, text, command):
        ctk.CTkButton(parent, text=text, fg_color="transparent", border_width=1, border_color="gray", 
                      width=200, height=40, font=FONT_BUTTON, anchor="w", command=command).pack(pady=5)

    # ------------------------------------------
    # MAIN MENU
    # ------------------------------------------
    def show_main_menu(self):
        self.clear_window()
        self.reset_window_size()
        
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_frame.pack(expand=True, fill="both")
        
        header = ctk.CTkFrame(main_frame, height=80, corner_radius=0, fg_color=COLOR_PRIMARY)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="SISTEM PELAYANAN TERPADU", font=("Roboto", 24, "bold"), text_color="white").pack(side="left", padx=30, pady=20)
        self.clock_label = ctk.CTkLabel(header, text="Clock...", font=("Roboto", 14), text_color="#d1d8e0")
        self.clock_label.pack(side="right", padx=30)

        content = ctk.CTkFrame(main_frame, fg_color="transparent")
        content.pack(expand=True)
        ctk.CTkLabel(content, text="Silakan pilih portal akses Anda:", font=("Roboto", 16), text_color="gray").pack(pady=(0, 30))

        grid_frame = ctk.CTkFrame(content, fg_color="transparent")
        grid_frame.pack()

        self.create_menu_card(grid_frame, "WARGA", "Akses Permohonan", COLOR_SUCCESS, self.show_warga_menu, 0)
        self.create_menu_card(grid_frame, "PETUGAS", "Loket Pelayanan", COLOR_WARNING, self.show_petugas_login, 1)
        self.create_menu_card(grid_frame, "ADMINISTRATOR", "Pengaturan Sistem", COLOR_PRIMARY, self.show_admin_login, 2)

        ctk.CTkButton(main_frame, text="KELUAR APLIKASI", fg_color="transparent", border_width=1, border_color=COLOR_DANGER,
                      text_color=COLOR_DANGER, font=FONT_BUTTON, hover_color="#333", width=200, command=self.quit).pack(pady=30)

    def create_menu_card(self, parent, title, subtitle, color, command, col):
        card = ctk.CTkButton(parent, text=f"{title}\n\n{subtitle}", width=260, height=180,
                             font=("Roboto", 22, "bold"), fg_color=COLOR_CARD, corner_radius=10, 
                             border_width=2, border_color=color, hover_color=color, command=command)
        card.grid(row=0, column=col, padx=15, pady=15)

    def create_login_screen(self, title, callback_login, callback_back):
        self.clear_window()
        frame = ctk.CTkFrame(self, width=400, height=450, corner_radius=15, fg_color=COLOR_CARD)
        frame.pack(expand=True)
        frame.pack_propagate(False)
        ctk.CTkLabel(frame, text=title, font=("Roboto", 20, "bold"), text_color=COLOR_ACCENT).pack(pady=(50, 40))
        entry_user = ctk.CTkEntry(frame, placeholder_text="Username", width=300, height=45, font=FONT_BODY)
        entry_user.pack(pady=10)
        entry_pass = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300, height=45, font=FONT_BODY)
        entry_pass.pack(pady=10)
        ctk.CTkButton(frame, text="LOGIN SYSTEM", width=300, height=45, font=FONT_BUTTON, fg_color=COLOR_PRIMARY,
                      command=lambda: callback_login(entry_user.get(), entry_pass.get())).pack(pady=30)
        ctk.CTkButton(frame, text="KEMBALI", fg_color="transparent", text_color="gray", font=FONT_BUTTON, command=callback_back).pack()

    # ==========================================
    # WARGA FEATURES
    # ==========================================
    def show_warga_menu(self):
        self.clear_window()
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color=COLOR_CARD)
        frame.pack(expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text="PORTAL WARGA", font=FONT_HEADER, text_color=COLOR_SUCCESS).pack(pady=40, padx=80)
        ctk.CTkButton(frame, text="LOGIN AKUN", width=250, height=50, font=FONT_BUTTON, fg_color=COLOR_SUCCESS, command=self.show_warga_login).pack(pady=10)
        ctk.CTkButton(frame, text="REGISTRASI BARU", width=250, height=50, font=FONT_BUTTON, fg_color="transparent", border_width=1, border_color=COLOR_SUCCESS, command=self.show_warga_register).pack(pady=10)
        ctk.CTkButton(frame, text="KEMBALI KE MENU", width=250, font=FONT_BUTTON, fg_color="transparent", text_color="gray", command=self.show_main_menu).pack(pady=30)

    def show_warga_register(self):
        self.clear_window()
        frame = ctk.CTkFrame(self, width=400, height=500, corner_radius=15, fg_color=COLOR_CARD)
        frame.pack(expand=True)
        frame.pack_propagate(False)
        ctk.CTkLabel(frame, text="REGISTRASI AKUN", font=FONT_SUBHEAD).pack(pady=(40, 30))
        entry_nama = ctk.CTkEntry(frame, placeholder_text="Nama Lengkap", width=300, height=40)
        entry_nama.pack(pady=10)
        entry_pass = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300, height=40)
        entry_pass.pack(pady=10)
        
        def do_register():
            nama = entry_nama.get()
            pw = entry_pass.get()
            if not nama or not pw: return messagebox.showerror("Error", "Mohon lengkapi data.")
            if any(w['nama'].lower() == nama.lower() for w in DATA['warga']): return messagebox.showerror("Error", "Nama sudah terdaftar.")
            DATA["warga"].append({"nama": nama, "password": pw})
            save_csv(PATHS["warga"], ["nama", "password"], DATA["warga"])
            messagebox.showinfo("Sukses", "Registrasi berhasil.")
            self.show_warga_login()

        ctk.CTkButton(frame, text="DAFTAR SEKARANG", width=300, height=40, font=FONT_BUTTON, fg_color=COLOR_SUCCESS, command=do_register).pack(pady=20)
        ctk.CTkButton(frame, text="BATAL", fg_color="transparent", font=FONT_BUTTON, text_color="gray", command=self.show_warga_menu).pack()

    def show_warga_login(self):
        def login_logic(u, p):
            for w in DATA["warga"]:
                if w["nama"].lower() == u.lower() and w["password"] == p:
                    self.show_warga_dashboard(w["nama"])
                    return
            messagebox.showerror("Error", "Nama atau Password Salah")
        self.create_login_screen("LOGIN WARGA", login_logic, self.show_warga_menu)

    def show_warga_dashboard(self, nama):
        self.clear_window()
        self.reset_window_size()

        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#222")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="DASHBOARD", font=FONT_SUBHEAD, text_color="gray").pack(pady=(30,10))
        ctk.CTkLabel(sidebar, text=nama.upper(), font=("Roboto", 16, "bold"), text_color="white").pack(pady=(0, 40))
        
        def open_pengajuan(): self.clear_content_warga(); self.page_buat_pengajuan(nama)
        def open_status(): self.clear_content_warga(); self.page_status_warga(nama)
        def open_profil(): self.clear_content_warga(); self.page_profil(nama, "warga")

        self.create_sidebar_btn(sidebar, "Buat Pengajuan", open_pengajuan)
        self.create_sidebar_btn(sidebar, "Status & Riwayat", open_status)
        self.create_sidebar_btn(sidebar, "Profil Saya", open_profil)
        ctk.CTkButton(sidebar, text="LOGOUT", fg_color=COLOR_DANGER, width=200, height=40, font=FONT_BUTTON, command=self.show_main_menu).pack(pady=20, side="bottom")

        self.warga_content = ctk.CTkFrame(self, fg_color="transparent")
        self.warga_content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        open_pengajuan()

    def clear_content_warga(self):
        for w in self.warga_content.winfo_children(): w.destroy()

    def page_buat_pengajuan(self, nama):
        scroll_frame = ctk.CTkScrollableFrame(self.warga_content, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll_frame, text="FORMULIR PENGAJUAN", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkLabel(scroll_frame, text="1. DATA DIRI", font=FONT_SUBHEAD, text_color=COLOR_ACCENT).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(scroll_frame, text="NIK:", font=FONT_BOLD).pack(anchor="w"); entry_nik = ctk.CTkEntry(scroll_frame, width=400); entry_nik.pack(anchor="w", pady=(0,10))
        ctk.CTkLabel(scroll_frame, text="No. HP:", font=FONT_BOLD).pack(anchor="w"); entry_hp = ctk.CTkEntry(scroll_frame, width=400); entry_hp.pack(anchor="w", pady=(0,10))
        ctk.CTkLabel(scroll_frame, text="Alamat:", font=FONT_BOLD).pack(anchor="w"); entry_alamat = ctk.CTkTextbox(scroll_frame, width=400, height=60); entry_alamat.pack(anchor="w", pady=(0,20))

        ctk.CTkLabel(scroll_frame, text="2. DETAIL PERMOHONAN", font=FONT_SUBHEAD, text_color=COLOR_ACCENT).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(scroll_frame, text="Dokumen:", font=FONT_BOLD).pack(anchor="w"); combo_dok = ctk.CTkComboBox(scroll_frame, values=[d['jenis'] for d in DATA['dokumen']], width=400); combo_dok.pack(anchor="w", pady=(0,10))
        ctk.CTkLabel(scroll_frame, text="Kategori Prioritas:", font=FONT_BOLD).pack(anchor="w")
        prio_var = ctk.StringVar(value="Umum")
        frame_radio = ctk.CTkFrame(scroll_frame, fg_color="transparent"); frame_radio.pack(anchor="w", pady=5)
        for k in ["Umum", "Lansia", "Ibu Hamil", "Darurat"]:
            ctk.CTkRadioButton(frame_radio, text=k, variable=prio_var, value=k, text_color=COLOR_DANGER if k=="Darurat" else "white").pack(side="left", padx=(0,20))
        
        ctk.CTkLabel(scroll_frame, text="Alasan (Wajib untuk Darurat):", font=FONT_BOLD).pack(anchor="w", pady=(10,0))
        entry_deskripsi = ctk.CTkTextbox(scroll_frame, width=400, height=60); entry_deskripsi.pack(anchor="w", pady=(0,20))

        def submit():
            nik, hp, alamat = entry_nik.get(), entry_hp.get(), entry_alamat.get("1.0", "end-1c").strip()
            dok, deskripsi, kat = combo_dok.get(), entry_deskripsi.get("1.0", "end-1c").strip(), prio_var.get()
            
            if not nik or not hp or not alamat or not dok: return messagebox.showerror("Gagal", "Lengkapi Data Diri & Dokumen.")
            if kat == "Darurat" and len(deskripsi) < 5: return messagebox.showerror("Gagal", "Isi alasan darurat dengan jelas.")

            new_id = str(max([int(x['id']) for x in DATA['antrian']] + [int(x['id']) for x in DATA['riwayat']] + [0]) + 1)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            DATA["antrian"].append({"id": new_id, "waktu": timestamp, "nama": nama, "nik": nik, "telepon": hp, "alamat": alamat, "dokumen": dok, "kategori": kat, "deskripsi": deskripsi, "status": "Menunggu"})
            save_csv(PATHS["antrian"], FIELDNAMES_ANTRIAN, DATA["antrian"])
            
            messagebox.showinfo("Sukses", f"Tiket #{new_id} berhasil dikirim ke petugas.")
            self.page_status_warga(nama)

        ctk.CTkButton(scroll_frame, text="KIRIM PERMOHONAN", width=200, height=45, font=FONT_BUTTON, fg_color=COLOR_SUCCESS, command=submit).pack(anchor="w", pady=40)

    def page_status_warga(self, nama):
        ctk.CTkLabel(self.warga_content, text="STATUS PENGAJUAN", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        
        self.tree_status = ttk.Treeview(self.warga_content, columns=("ID", "Dokumen", "Prioritas", "Status"), show="headings")
        self.tree_status.heading("ID", text="ID"); self.tree_status.column("ID", width=60, anchor="center")
        self.tree_status.heading("Dokumen", text="Dokumen"); self.tree_status.column("Dokumen", width=250)
        self.tree_status.heading("Prioritas", text="Prioritas"); self.tree_status.column("Prioritas", width=100)
        self.tree_status.heading("Status", text="Status"); self.tree_status.column("Status", width=120)
        self.tree_status.pack(fill="both", expand=True)
        
        sorted_q = self.get_sorted_queue()
        for i in sorted_q: 
            if i["nama"] == nama: self.tree_status.insert("", "end", values=(i["id"], i["dokumen"], i["kategori"], "DALAM ANTRIAN"))
        for i in DATA["riwayat"]:
            if i["nama"] == nama: self.tree_status.insert("", "end", values=(i["id"], i["dokumen"], i["kategori"], i['status'].upper()))

        ctk.CTkLabel(self.warga_content, text="*Klik data berstatus SELESAI, lalu tekan tombol di bawah.", text_color="gray").pack(anchor="w", pady=(10,0))
        ctk.CTkButton(self.warga_content, text="LIHAT BUKTI PENGAMBILAN", width=250, height=45, 
                      fg_color=COLOR_ACCENT, font=FONT_BUTTON, command=self.tampilkan_struk_layar).pack(pady=20)

    def tampilkan_struk_layar(self):
        selected = self.tree_status.selection()
        if not selected: return messagebox.showwarning("Peringatan", "Pilih data dari tabel terlebih dahulu.")
        
        item = self.tree_status.item(selected); val = item['values']
        id_tiket = str(val[0]); status = val[3]

        if "SELESAI" not in status: return messagebox.showerror("Gagal", "Dokumen belum selesai.")

        data = next((x for x in DATA["riwayat"] if str(x["id"]) == id_tiket), None)
        if not data: return

        # --- JENDELA POP-UP STRUK ---
        struk_win = ctk.CTkToplevel(self)
        struk_win.title("Bukti Pengambilan")
        struk_win.geometry("400x550")
        struk_win.attributes('-topmost', True)
        
        paper = ctk.CTkFrame(struk_win, fg_color="white", corner_radius=0)
        paper.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(paper, text="BUKTI PENGAMBILAN", font=("Courier New", 20, "bold"), text_color="black").pack(pady=(20,5))
        ctk.CTkLabel(paper, text="SISTEM PELAYANAN TERPADU", font=("Courier New", 10), text_color="black").pack(pady=(0,20))
        
        txt = f"\nID TIKET      : {id_tiket}\nTANGGAL       : {datetime.now().strftime('%d-%m-%Y')}\n----------------------------------\nPEMOHON       : {data['nama']}\nNIK           : {data.get('nik','-')}\nDOKUMEN       : {data['dokumen']}\nSTATUS        : {data['status'].upper()}\n----------------------------------\n\nSilakan tunjukkan layar ini\nkepada petugas loket.\n"
        ctk.CTkLabel(paper, text=txt, font=("Courier New", 12), text_color="black", justify="left").pack(padx=10)
        ctk.CTkButton(paper, text="TUTUP", fg_color="#333", text_color="white", width=100, command=struk_win.destroy).pack(pady=20)

    # ------------------------------------------
    # PROFIL PAGE
    # ------------------------------------------
    def page_profil(self, nama, role):
        parent = self.warga_content if role == "warga" else self.petugas_content_area
        ctk.CTkLabel(parent, text="PENGATURAN PROFIL", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(card, text="Nama Akun:", font=FONT_BODY, text_color="gray").pack(anchor="w", padx=20, pady=(20,0))
        ctk.CTkLabel(card, text=nama, font=("Roboto", 20, "bold")).pack(anchor="w", padx=20, pady=(0,20))
        
        ctk.CTkLabel(parent, text="Ubah Password", font=FONT_SUBHEAD, text_color=COLOR_ACCENT).pack(anchor="w", pady=(30, 10))
        entry_old = ctk.CTkEntry(parent, placeholder_text="Password Lama", show="*", width=300); entry_old.pack(anchor="w", pady=5)
        entry_new = ctk.CTkEntry(parent, placeholder_text="Password Baru", show="*", width=300); entry_new.pack(anchor="w", pady=5)
        
        def save_pass():
            old_p = entry_old.get(); new_p = entry_new.get()
            db = DATA["warga"] if role == "warga" else DATA["petugas"]
            path = PATHS["warga"] if role == "warga" else PATHS["petugas"]
            user = next((u for u in db if u["nama"] == nama), None)
            
            if user and user["password"] == old_p:
                if not new_p: return messagebox.showerror("Gagal", "Password baru kosong.")
                user["password"] = new_p
                save_csv(path, ["nama", "password"], db)
                messagebox.showinfo("Sukses", "Password diubah."); entry_old.delete(0, "end"); entry_new.delete(0, "end")
            else: messagebox.showerror("Gagal", "Password lama salah.")

        ctk.CTkButton(parent, text="SIMPAN PERUBAHAN", fg_color=COLOR_PRIMARY, width=200, command=save_pass).pack(anchor="w", pady=20)

    # ==========================================
    # PETUGAS FEATURES
    # ==========================================
    def show_petugas_login(self):
        def login_logic(u, p):
            for x in DATA["petugas"]:
                if x["nama"].lower() == u.lower() and x["password"] == p:
                    self.show_petugas_dashboard(x["nama"])
                    return
            messagebox.showerror("Error", "Akses Ditolak")
        self.create_login_screen("LOGIN PETUGAS", login_logic, self.show_main_menu)

    def show_petugas_dashboard(self, nama_petugas):
        self.clear_window()
        self.reset_window_size()

        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#222")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="PANEL PETUGAS", font=FONT_SUBHEAD, text_color="gray").pack(pady=(30,10))
        ctk.CTkLabel(sidebar, text=nama_petugas.upper(), font=("Roboto", 16, "bold"), text_color="white").pack(pady=(0, 40))

        def open_loket(): self.clear_content_petugas(); self.page_loket_petugas()
        def open_profil(): self.clear_content_petugas(); self.page_profil(nama_petugas, "petugas")

        self.create_sidebar_btn(sidebar, "Loket Antrian", open_loket)
        self.create_sidebar_btn(sidebar, "Profil Saya", open_profil)
        ctk.CTkButton(sidebar, text="LOGOUT", fg_color=COLOR_DANGER, width=200, height=40, font=FONT_BUTTON, command=self.show_main_menu).pack(pady=20, side="bottom")

        self.petugas_content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.petugas_content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        open_loket()

    def clear_content_petugas(self):
        for w in self.petugas_content_area.winfo_children(): w.destroy()

    def page_loket_petugas(self):
        container = self.petugas_content_area
        left_frame = ctk.CTkFrame(container, fg_color=COLOR_CARD)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=15)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Cari ID / Nama...", height=35)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(search_frame, text="CARI", width=80, height=35, fg_color=COLOR_PRIMARY, command=self.refresh_petugas_queue).pack(side="right")
        
        self.tree_petugas = ttk.Treeview(left_frame, columns=("ID", "Prioritas", "Nama", "Dokumen"), show="headings")
        self.tree_petugas.heading("ID", text="ID"); self.tree_petugas.column("ID", width=50)
        self.tree_petugas.heading("Prioritas", text="PRIORITAS"); self.tree_petugas.column("Prioritas", width=100)
        self.tree_petugas.heading("Nama", text="NAMA"); self.tree_petugas.column("Nama", width=150)
        self.tree_petugas.heading("Dokumen", text="DOKUMEN"); self.tree_petugas.column("Dokumen", width=150)
        self.tree_petugas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.right_frame = ctk.CTkFrame(container, width=350, fg_color=COLOR_CARD)
        self.right_frame.pack(side="right", fill="y")
        
        ctk.CTkLabel(self.right_frame, text="KONTROL LOKET", font=FONT_SUBHEAD).pack(pady=20)
        self.btn_call = ctk.CTkButton(self.right_frame, text="PANGGIL ANTRIAN", height=50, fg_color=COLOR_WARNING, text_color="black", font=FONT_BUTTON, command=self.petugas_panggil_next)
        self.btn_call.pack(pady=10, padx=20, fill="x")
        
        self.action_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.action_frame.pack(fill="both", expand=True, padx=10)
        self.current_process = None
        self.refresh_petugas_queue()

    def refresh_petugas_queue(self):
        for item in self.tree_petugas.get_children(): self.tree_petugas.delete(item)
        sorted_q = self.get_sorted_queue()
        keyword = self.search_entry.get().lower()
        for item in sorted_q:
            if keyword in item['nama'].lower() or keyword in item['id']:
                tag = "Darurat" if item['kategori'] == "Darurat" else ""
                self.tree_petugas.insert("", "end", values=(item["id"], item["kategori"].upper(), item["nama"], item["dokumen"]), tags=(tag,))

    def petugas_panggil_next(self):
        sorted_q = self.get_sorted_queue()
        if not sorted_q: return messagebox.showinfo("Info", "Antrian kosong.")
        
        self.current_process = sorted_q[0]
        for w in self.action_frame.winfo_children(): w.destroy()
        
        ctk.CTkLabel(self.action_frame, text="SEDANG DILAYANI", font=FONT_BOLD, text_color="gray").pack(pady=(30, 10))
        detail = ctk.CTkFrame(self.action_frame, fg_color="#222", corner_radius=10)
        detail.pack(fill="x", padx=10)
        
        color = COLOR_DANGER if self.current_process["kategori"] == "Darurat" else COLOR_ACCENT
        ctk.CTkLabel(detail, text=self.current_process["kategori"].upper(), text_color=color, font=("Roboto", 18, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(detail, text=f"Tiket #{self.current_process['id']} - {self.current_process['nama']}", font=FONT_BODY).pack()
        
        info = f"NIK: {self.current_process.get('nik', '-')}\nDeskripsi: {self.current_process.get('deskripsi', '-')}"
        ctk.CTkLabel(detail, text=info, font=("Roboto", 11), justify="center").pack(pady=10)

        ctk.CTkButton(self.action_frame, text="SELESAI", fg_color=COLOR_SUCCESS, height=40, command=lambda: self.selesaikan("Selesai")).pack(pady=10, fill="x")
        ctk.CTkButton(self.action_frame, text="TOLAK", fg_color=COLOR_DANGER, height=40, command=lambda: self.selesaikan("Ditolak")).pack(pady=0, fill="x")

    def selesaikan(self, status):
        target = self.current_process
        DATA["antrian"] = [x for x in DATA["antrian"] if x["id"] != target["id"]]
        target["status"] = status
        DATA["riwayat"].append(target)
        save_csv(PATHS["antrian"], FIELDNAMES_ANTRIAN, DATA["antrian"])
        save_csv(PATHS["riwayat"], FIELDNAMES_ANTRIAN, DATA["riwayat"])
        self.current_process = None
        for w in self.action_frame.winfo_children(): w.destroy()
        self.refresh_petugas_queue()

    # ==========================================
    # ADMIN FEATURES
    # ==========================================
    def show_admin_login(self):
        def login_logic(u, p):
            for a in DATA["admin"]:
                if a["username"] == u and a["password"] == p:
                    self.show_admin_dashboard()
                    return
            messagebox.showerror("Error", "Login Gagal")
        self.create_login_screen("LOGIN ADMINISTRATOR", login_logic, self.show_main_menu)

    def show_admin_dashboard(self):
        self.clear_window()
        self.reset_window_size()

        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#1a1a1a")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="ADMIN PANEL", font=FONT_SUBHEAD, text_color="white").pack(pady=30)
        self.create_sidebar_btn(sidebar, "Manajemen Petugas", self.admin_page_users)
        self.create_sidebar_btn(sidebar, "Laporan & Data", self.admin_page_stats)
        ctk.CTkButton(sidebar, text="LOGOUT", fg_color=COLOR_DANGER, font=FONT_BUTTON, command=self.show_main_menu).pack(side="bottom", pady=20)
        self.admin_content = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        self.admin_page_stats()

    def clear_admin(self):
        for w in self.admin_content.winfo_children(): w.destroy()

    def admin_page_users(self):
        self.clear_admin()
        ctk.CTkLabel(self.admin_content, text="MANAJEMEN PETUGAS", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(self.admin_content, columns=("Nama", "Pass"), show="headings", height=8)
        tree.heading("Nama", text="NAMA"); tree.heading("Pass", text="PASSWORD")
        tree.pack(fill="x")
        for p in DATA["petugas"]: tree.insert("", "end", values=(p["nama"], "******"))
        
        def add_p():
            dialog = ctk.CTkInputDialog(text="Nama Petugas:", title="Tambah")
            nama = dialog.get_input()
            if nama:
                DATA["petugas"].append({"nama": nama, "password": "1234"})
                save_csv(PATHS["petugas"], ["nama", "password"], DATA["petugas"])
                self.admin_page_users()
        ctk.CTkButton(self.admin_content, text="+ TAMBAH PETUGAS", width=200, height=40, font=FONT_BUTTON, command=add_p).pack(pady=20, anchor="w")

    def admin_page_stats(self):
        self.clear_admin()
        ctk.CTkLabel(self.admin_content, text="DASHBOARD DATA", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        
        frame = ctk.CTkFrame(self.admin_content, fg_color="transparent"); frame.pack(fill="x", pady=10)
        for i, (t, v, c) in enumerate([("ANTRIAN", len(DATA["antrian"]), COLOR_WARNING), ("SELESAI", len([x for x in DATA["riwayat"] if x["status"]=="Selesai"]), COLOR_SUCCESS), ("DARURAT", len([x for x in DATA["antrian"] if x["kategori"]=="Darurat"]), COLOR_DANGER)]):
            card = ctk.CTkFrame(frame, fg_color=c, width=220, height=100); card.grid(row=0, column=i, padx=10)
            ctk.CTkLabel(card, text=t, text_color="black", font=FONT_BOLD).pack(pady=(20,0))
            ctk.CTkLabel(card, text=str(v), text_color="black", font=("Roboto", 30, "bold")).pack()

        ctk.CTkLabel(self.admin_content, text="REKAP DATA LENGKAP", font=FONT_SUBHEAD).pack(anchor="w", pady=(30, 10))
        table_frame = ctk.CTkFrame(self.admin_content, fg_color="transparent"); table_frame.pack(fill="both", expand=True)
        cols = ("ID", "Waktu", "NIK", "Nama", "Dokumen", "Status")
        self.tree_admin = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols: self.tree_admin.heading(c, text=c); self.tree_admin.column(c, width=100)
        self.tree_admin.column("Dokumen", width=200)
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_admin.yview); self.tree_admin.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y"); self.tree_admin.pack(fill="both", expand=True)

        all_data = sorted(DATA["antrian"] + DATA["riwayat"], key=lambda x: int(x['id']), reverse=True)
        for i in all_data: self.tree_admin.insert("", "end", values=(i["id"], i.get("waktu","-"), i.get("nik","-"), i["nama"], i["dokumen"], i["status"]))

        # TOMBOL DETAIL ADMIN BUAT LIAT DATA
        self.tree_admin.bind("<Double-1>", lambda e: self.admin_show_detail_popup())
        ctk.CTkLabel(self.admin_content, text="*Klik dua kali pada baris untuk melihat detail lengkap.", text_color="gray").pack(anchor="w", pady=(10,0))
        ctk.CTkButton(self.admin_content, text="LIHAT DETAIL DATA", width=200, command=self.admin_show_detail_popup).pack(anchor="w", pady=20)

    def admin_show_detail_popup(self):
        selected = self.tree_admin.selection()
        if not selected: return messagebox.showwarning("Peringatan", "Pilih data dulu.")
        item = self.tree_admin.item(selected); val = item['values']; id_tik = str(val[0])
        
        data = next((x for x in DATA["antrian"] + DATA["riwayat"] if str(x["id"]) == id_tik), None)
        if not data: return

        # POP-UP DETAIL
        win = ctk.CTkToplevel(self); win.title("Detail Data Warga"); win.geometry("400x550"); win.attributes('-topmost', True)
        
        ctk.CTkLabel(win, text="DETAIL DATA PEMOHON", font=FONT_SUBHEAD).pack(pady=20)
        f = ctk.CTkScrollableFrame(win, width=350, height=450); f.pack(pady=10)
        
        fields = [("ID Tiket", data['id']), ("Waktu", data.get('waktu','-')), ("Nama", data['nama']), 
                  ("NIK", data.get('nik','-')), ("HP", data.get('telepon','-')), ("Alamat", data.get('alamat','-')),
                  ("Dokumen", data['dokumen']), ("Kategori", data['kategori']), ("Status", data['status'])]
        
        for k, v in fields:
            ctk.CTkLabel(f, text=k, font=("Roboto", 10, "bold"), text_color="gray").pack(anchor="w", padx=10)
            ctk.CTkLabel(f, text=v, font=("Roboto", 14)).pack(anchor="w", padx=10, pady=(0, 10))
            
        ctk.CTkLabel(f, text="Deskripsi / Alasan:", font=("Roboto", 10, "bold"), text_color="gray").pack(anchor="w", padx=10)
        ctk.CTkTextbox(f, height=100, width=300).pack(pady=5); 
        t = f.winfo_children()[-1]; t.insert("0.0", data.get('deskripsi','-')); t.configure(state="disabled")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()