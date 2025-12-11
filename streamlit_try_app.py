import streamlit as st
import csv
import os

# ============================
# CLASS USER
# ============================
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

# ============================
# CLASS PRODUK LILIN
# ============================
class ProdukLilin:
    def __init__(self, nama, harga, stok):
        self._nama = nama
        self._harga = harga
        self._stok = stok

    # --- GETTER ---
    def get_nama(self):
        return self._nama
    
    def get_harga(self):
        return self._harga

    def get_stok(self):
        return self._stok

    # --- SETTER ---
    def set_nama(self, nama_baru):
        self._nama = nama_baru

    def set_harga(self, harga_baru):
        self._harga = harga_baru

    def set_stok(self, stok_baru):
        self._stok = stok_baru

    # --- METHOD LOGIKA ---
    def kurangi_stok(self, jumlah):
        self._stok = self._stok - jumlah

    def info(self):
        # Di Streamlit kita pakai st.write / st.card
        pesan_stok = str(self._stok)
        if self._stok < 5:
            pesan_stok = str(self._stok) + " (!!! STOK MENIPIS !!!)"
            
        st.markdown(f"**{self._nama}**")
        st.write(f"Harga : Rp {self._harga}")
        st.write(f"Stok  : {pesan_stok}")
        st.divider()

# ============================
# INISIALISASI SESSION STATE
# (PENGGANTI DATABASE GLOBAL)
# ============================
def init_state():
    # Database User
    if 'users_db' not in st.session_state:
        st.session_state['users_db'] = {
            "admin": User("admin", "123", "admin"),
            "naya":  User("naya", "abc", "pembeli"),
            "shifa": User("shifa", "abc", "pembeli")
        }

    # Database Produk
    if 'produk_list' not in st.session_state:
        st.session_state['produk_list'] = [
            ProdukLilin("Lilin Lavender", 50000, 10),
            ProdukLilin("Lilin Vanila", 45000, 3), 
            ProdukLilin("Lilin Sandalwood", 60000, 5)
        ]

    # Database Transaksi
    if 'riwayat_transaksi' not in st.session_state:
        st.session_state['riwayat_transaksi'] = []

    # Database Keranjang
    if 'keranjang' not in st.session_state:
        st.session_state['keranjang'] = []

    # Database Laporan
    if 'inbox_laporan' not in st.session_state:
        st.session_state['inbox_laporan'] = []
        
    # Status Login
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None # Belum login
    if 'user_login' not in st.session_state:
        st.session_state['user_login'] = ""

# Panggil fungsi init di awal
init_state()

# ============================
# FUNGSI BANTUAN
# ============================
def cari_produk(nama_dicari):
    for produk in st.session_state['produk_list']:
        if produk.get_nama().lower() == nama_dicari.lower():
            return produk
    return None

# ============================
# FUNGSI EXPORT & IMPORT
# ============================
def fitur_export_data():
    st.subheader("--- MENU EXPORT DATA (CSV) ---")
    jenis = st.selectbox("Pilih data yang mau diexport:", 
                         ["Data User", "Data Produk", "Riwayat Penjualan", "Laporan Masalah"])
    
    if st.button("Export Sekarang"):
        if jenis == "Data User":
            filename = "data_users.csv"
            header = ['Username', 'Password', 'Role']
            data_rows = []
            db = st.session_state['users_db']
            for username in db:
                u = db[username] 
                data_rows.append([u.username, u.password, u.role])
            
            with open(filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(data_rows)
            st.success(f">> Sukses export {filename}!")

        elif jenis == "Data Produk":
            filename = "data_produk.csv"
            header = ['Nama Produk', 'Harga', 'Stok']
            data_rows = []
            for produk in st.session_state['produk_list']:
                data_rows.append([produk.get_nama(), produk.get_harga(), produk.get_stok()])
        
            with open(filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(data_rows)
            st.success(f">> Sukses export {filename}!")

        elif jenis == "Riwayat Penjualan":
            tx = st.session_state['riwayat_transaksi']
            if len(tx) == 0:
                st.warning("Data penjualan masih kosong.")
            else:
                filename = "data_penjualan.csv"
                header = ['pembeli', 'barang', 'qty', 'total', 'status']
                with open(filename, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=header)
                    writer.writeheader()
                    writer.writerows(tx)
                st.success(f">> Sukses export {filename}!")

        elif jenis == "Laporan Masalah":
            lapor = st.session_state['inbox_laporan']
            if len(lapor) == 0:
                st.warning("Data laporan masih kosong.")
            else:
                filename = "data_laporan.csv"
                header = ['pengirim', 'pesan', 'jawaban']
                with open(filename, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=header)
                    writer.writeheader()
                    writer.writerows(lapor)
                st.success(f">> Sukses export {filename}!")

def fitur_import_data():
    st.subheader("--- IMPORT DATA (LOAD SAVE FILE) ---")
    st.warning("Peringatan: Data lama akan ditimpa.")
    
    if st.button("Yakin Load Data?"):
        # 1. IMPORT USER
        if os.path.exists("data_users.csv"):
            with open("data_users.csv", "r") as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader) # Skip Header
                rows = [r for r in csvreader]
            st.session_state['users_db'].clear()
            for row in rows:
                st.session_state['users_db'][row[0]] = User(row[0], row[1], row[2])
            st.success(">> Sukses load User.")
        else:
            st.error(">> File data_users.csv tidak ada.")

        # 2. IMPORT PRODUK
        if os.path.exists("data_produk.csv"):
            with open("data_produk.csv", "r") as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                rows = [r for r in csvreader]
            st.session_state['produk_list'].clear()
            for row in rows:
                st.session_state['produk_list'].append(ProdukLilin(row[0], int(row[1]), int(row[2])))
            st.success(">> Sukses load Produk.")
        else:
            st.error(">> File data_produk.csv tidak ada.")

        # 3. IMPORT PENJUALAN
        if os.path.exists("data_penjualan.csv"):
            with open("data_penjualan.csv", "r") as csvfile:
                csvreader = csv.DictReader(csvfile)
                rows = []
                for row in csvreader:
                    row['qty'] = int(row['qty'])
                    row['total'] = int(row['total'])
                    rows.append(row)
            st.session_state['riwayat_transaksi'] = rows
            st.success(">> Sukses load Penjualan.")
        else:
            st.error(">> File data_penjualan.csv tidak ada.")

        # 4. IMPORT LAPORAN
        if os.path.exists("data_laporan.csv"):
            with open("data_laporan.csv", "r") as csvfile:
                csvreader = csv.DictReader(csvfile)
                rows = [r for r in csvreader]
            st.session_state['inbox_laporan'] = rows
            st.success(">> Sukses load Laporan.")
        else:
            st.error(">> File data_laporan.csv tidak ada.")

# ============================
# LOGIN & REGISTER PAGE
# ============================
def halaman_login():
    st.title("=== LOGIN REKINDLE ===")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Masuk")
        
        if submitted:
            user = st.session_state['users_db'].get(username)
            
            if user is None:
                st.error("Gagal: Username tidak ditemukan!")
            elif user.password != password:
                st.error("Gagal: Password salah!")
            else:
                # Login Sukses
                st.session_state['user_role'] = user.role
                st.session_state['user_login'] = user.username
                st.success(f"Login berhasil! Halo, {user.username}")
                st.rerun() # Refresh halaman

def halaman_register():
    st.title("=== DAFTAR AKUN BARU ===")
    
    with st.form("reg_form"):
        username_baru = st.text_input("Username baru")
        password_baru = st.text_input("Password baru", type="password")
        submitted = st.form_submit_button("Daftar")
        
        if submitted:
            if username_baru in st.session_state['users_db']:
                st.error(">> Gagal: Username sudah terpakai!")
            elif username_baru == "":
                st.error("Username tidak boleh kosong")
            else:
                st.session_state['users_db'][username_baru] = User(username_baru, password_baru, "pembeli")
                st.success("Sukses: Akun berhasil dibuat! Silakan Login.")

# ============================
# HALAMAN ADMIN
# ============================
def menu_admin():
    st.sidebar.title("ADMIN MENU")
    menu = st.sidebar.radio("Pilih:", [
        "Cek Stok Gudang", "Tambah Produk", "Edit Produk", "Kelola Role User",
        "Lihat Penjualan", "Update Status Pengiriman", "Cek Laporan Masalah",
        "Export/Import Data", "Logout"
    ])

    if menu == "Cek Stok Gudang":
        st.subheader("--- GUDANG ---")
        for p in st.session_state['produk_list']:
            p.info()

    elif menu == "Tambah Produk":
        st.subheader("--- TAMBAH PRODUK ---")
        with st.form("tambah_prod"):
            nama = st.text_input("Nama Produk")
            harga = st.number_input("Harga", min_value=0, step=1000)
            stok = st.number_input("Stok", min_value=0, step=1)
            submit = st.form_submit_button("Simpan")
            if submit:
                st.session_state['produk_list'].append(ProdukLilin(nama, int(harga), int(stok)))
                st.success("Disimpan.")

    elif menu == "Edit Produk":
        st.subheader("--- EDIT DATA PRODUK ---")
        # Pilih produk dulu pakai selectbox biar lebih gampang
        list_nama_produk = [p.get_nama() for p in st.session_state['produk_list']]
        pilih_prod = st.selectbox("Pilih produk:", list_nama_produk)
        
        produk_terpilih = cari_produk(pilih_prod)
        if produk_terpilih:
            st.write(f"Edit: {produk_terpilih.get_nama()}")
            opsi_edit = st.selectbox("Mau ubah apa?", ["Ubah Nama", "Ubah Harga", "Ubah Stok"])
            
            with st.form("edit_form"):
                nilai_baru = st.text_input("Masukkan nilai baru:")
                submit_edit = st.form_submit_button("Update")
                
                if submit_edit:
                    if opsi_edit == "Ubah Nama":
                        produk_terpilih.set_nama(nilai_baru)
                        st.success(">> Berhasil ubah nama!")
                    elif opsi_edit == "Ubah Harga":
                        if nilai_baru.isdigit():
                            produk_terpilih.set_harga(int(nilai_baru))
                            st.success(">> Berhasil ubah harga!")
                        else: st.error("Harga harus angka.")
                    elif opsi_edit == "Ubah Stok":
                        if nilai_baru.isdigit():
                            produk_terpilih.set_stok(int(nilai_baru))
                            st.success(">> Berhasil ubah stok!")
                        else: st.error("Stok harus angka.")

    elif menu == "Kelola Role User":
        st.subheader("--- DAFTAR PENGGUNA ---")
        db = st.session_state['users_db']
        
        # Tampilkan tabel user
        data_tampil = []
        for u in db:
            data_tampil.append({"Username": db[u].username, "Role": db[u].role})
        st.table(data_tampil)

        st.write("Edit User:")
        target = st.selectbox("Pilih Username:", list(db.keys()))
        
        if target:
            aksi = st.selectbox("Aksi:", ["Ubah Status", "Ubah Password", "Rename User"])
            val_baru = st.text_input("Nilai Baru:")
            if st.button("Lakukan Perubahan"):
                if aksi == "Ubah Status":
                    db[target].role = val_baru
                    st.success(">> Sip! Status berhasil diubah.")
                elif aksi == "Ubah Password":
                    db[target].password = val_baru
                    st.success(">> Sip! Password berhasil diubah.")
                elif aksi == "Rename User":
                    if val_baru in db:
                        st.error(">> Gagal: Nama sudah dipakai.")
                    else:
                        obj_user = db[target]
                        obj_user.username = val_baru
                        db[val_baru] = obj_user
                        del db[target]
                        st.success(f">> Sip! Berubah jadi {val_baru}")
                        st.rerun()

    elif menu == "Lihat Penjualan":
        st.subheader("--- RIWAYAT PENJUALAN ---")
        cari = st.text_input("Cari nama pembeli:")
        
        total_pendapatan = 0
        tx_list = st.session_state['riwayat_transaksi']
        
        if len(tx_list) > 0:
            for tx in tx_list:
                if cari.lower() in tx['pembeli'].lower():
                    st.write(f"{tx['pembeli']} | Beli: {tx['barang']} | Rp {tx['total']} | Status: {tx['status']}")
                    total_pendapatan += tx['total']
            st.divider()
            st.metric("TOTAL UANG MASUK", f"Rp {total_pendapatan}")
        else:
            st.info("Belum ada data penjualan.")

    elif menu == "Update Status Pengiriman":
        st.subheader("--- UPDATE STATUS PESANAN ---")
        tx_list = st.session_state['riwayat_transaksi']
        
        # Buat list string untuk selectbox
        opsi_tx = []
        for i, tx in enumerate(tx_list):
            opsi_tx.append(f"{i+1}. {tx['pembeli']} - {tx['barang']} [{tx['status']}]")
            
        if opsi_tx:
            pilihan = st.selectbox("Pilih transaksi:", opsi_tx)
            status_baru = st.selectbox("Status Baru:", ["Diproses", "Sedang Dikirim", "Selesai"])
            
            if st.button("Update Status"):
                # Ambil index dari string (misal "1. naya..." ambil angka 0)
                idx = int(pilihan.split(".")[0]) - 1
                tx_list[idx]['status'] = status_baru
                st.success(f">> Status diubah jadi: {status_baru}")
                st.rerun()
        else:
            st.info("Tidak ada transaksi.")

    elif menu == "Cek Laporan Masalah":
        st.subheader("--- INBOX LAPORAN USER ---")
        laporan_list = st.session_state['inbox_laporan']
        
        if not laporan_list:
            st.info("Tidak ada pesan masuk.")
        else:
            # Pilih pesan untuk dibalas
            opsi_pesan = [f"{i+1}. Dari {m['pengirim']}: {m['pesan']}" for i, m in enumerate(laporan_list)]
            pilih_pesan = st.selectbox("Pilih Pesan:", opsi_pesan)
            
            idx = int(pilih_pesan.split(".")[0]) - 1
            st.write(f"**Pesan:** {laporan_list[idx]['pesan']}")
            st.write(f"**Balasan Saat Ini:** {laporan_list[idx]['jawaban']}")
            
            balasan_baru = st.text_input("Tulis balasan Admin:")
            if st.button("Kirim Balasan"):
                laporan_list[idx]['jawaban'] = balasan_baru
                st.success(">> Balasan terkirim!")
                st.rerun()

    elif menu == "Export/Import Data":
        tab1, tab2 = st.tabs(["Export", "Import"])
        with tab1:
            fitur_export_data()
        with tab2:
            fitur_import_data()

    elif menu == "Logout":
        st.session_state['user_role'] = None
        st.session_state['user_login'] = ""
        st.rerun()

# ============================
# HALAMAN PEMBELI
# ============================
def menu_pembeli(user_login):
    st.sidebar.title(f"PEMBELI ({user_login})")
    menu = st.sidebar.radio("Menu:", [
        "Belanja", "Keranjang & Bayar", "Cek Pesanan", "Lapor Masalah", "Logout"
    ])

    if menu == "Belanja":
        st.subheader("--- KATALOG PRODUK ---")
        # Tampilkan produk dalam Grid
        cols = st.columns(3)
        prod_list = st.session_state['produk_list']
        
        for i, produk in enumerate(prod_list):
            with cols[i % 3]:
                st.markdown(f"### {produk.get_nama()}")
                st.write(f"Harga: Rp {produk.get_harga()}")
                st.write(f"Stok: {produk.get_stok()}")
                
                with st.form(f"beli_{i}"):
                    qty = st.number_input("Jml Beli", min_value=1, max_value=produk.get_stok(), key=f"q_{i}")
                    add = st.form_submit_button("Masuk Keranjang")
                    if add:
                        if qty <= produk.get_stok():
                             item_belanja = {
                                "obj_produk": produk, # Simpan referensi objek
                                "nama": produk.get_nama(),
                                "harga": produk.get_harga(),
                                "qty": qty
                            }
                             st.session_state['keranjang'].append(item_belanja)
                             st.success(">> Berhasil masuk keranjang!")
                        else:
                             st.error("Stok kurang!")

    elif menu == "Keranjang & Bayar":
        st.subheader("--- KASIR REKINDLE ---")
        keranjang = st.session_state['keranjang']
        
        if not keranjang:
            st.warning(">> Keranjang kosong.")
        else:
            total_belanja = 0
            total_qty = 0
            
            st.write("Rincian Belanja:")
            for item in keranjang:
                subtotal = item['harga'] * item['qty']
                st.write(f"- {item['nama']} (x{item['qty']}) = Rp {subtotal}")
                total_belanja += subtotal
                total_qty += item['qty']
            
            st.divider()
            
            # Hitung Diskon
            persen_diskon = 0
            if total_qty >= 5:
                persen_diskon = 20
            elif total_qty >= 3:
                persen_diskon = 10
            
            potongan_harga = total_belanja * (persen_diskon / 100)
            total_akhir = total_belanja - potongan_harga
            
            st.write(f"Total Awal   : Rp {int(total_belanja)}")
            if persen_diskon > 0:
                st.success(f"DISKON {persen_diskon}% : -Rp {int(potongan_harga)}")
            else:
                st.info("DISKON : - (Beli min 3 dpt diskon!)")
            
            st.markdown(f"### TOTAL BAYAR : Rp {int(total_akhir)}")
            
            if st.button("Bayar Sekarang"):
                # Proses bayar
                for item in keranjang:
                    # Kurangi stok di object aslinya
                    item['obj_produk'].kurangi_stok(item['qty'])
                    # Masukkan history
                    st.session_state['riwayat_transaksi'].append({
                        "pembeli": user_login,
                        "barang": item['nama'],
                        "qty": item['qty'],
                        "total": item['harga'] * item['qty'],
                        "status": "Diproses"
                    })
                st.balloons()
                st.success(">> Pembayaran LUNAS! Terima kasih.")
                st.session_state['keranjang'] = [] # Kosongkan keranjang
                st.rerun()

    elif menu == "Cek Pesanan":
        st.subheader("--- RIWAYAT PESANAN SAYA ---")
        tx_list = st.session_state['riwayat_transaksi']
        ada = False
        for tx in tx_list:
            if tx['pembeli'] == user_login:
                st.write(f"- {tx['barang']} (x{tx['qty']}) | Total: Rp {tx['total']} | Status: **[{tx['status']}]**")
                ada = True
        if not ada:
            st.info(">> Belum ada pesanan.")

    elif menu == "Lapor Masalah":
        st.subheader("--- PUSAT BANTUAN ---")
        tab_tulis, tab_cek = st.tabs(["Tulis Laporan", "Cek Riwayat"])
        
        with tab_tulis:
            with st.form("lapor_form"):
                pesan_user = st.text_area("Tulis keluhan/pertanyaan Anda:")
                kirim = st.form_submit_button("Kirim Laporan")
                if kirim:
                    st.session_state['inbox_laporan'].append({
                        "pengirim": user_login,
                        "pesan": pesan_user,
                        "jawaban": "Belum dibalas"
                    })
                    st.success(">> Laporan terkirim ke Admin.")

        with tab_cek:
            laporan_list = st.session_state['inbox_laporan']
            ada_laporan = False
            for chat in laporan_list:
                if chat['pengirim'] == user_login:
                    st.write(f"**Q (Anda):** {chat['pesan']}")
                    st.info(f"**A (Admin):** {chat['jawaban']}")
                    st.divider()
                    ada_laporan = True
            if not ada_laporan:
                st.write(">> Belum ada riwayat laporan.")

    elif menu == "Logout":
        st.session_state['user_role'] = None
        st.session_state['user_login'] = ""
        st.rerun()

# ============================
# MAIN PROGRAM (NAVIGASI UTAMA)
# ============================
def main():
    # Cek Role
    role = st.session_state['user_role']
    user = st.session_state['user_login']

    if role is None:
        # Tampilan Awal (Belum Login)
        menu_awal = st.sidebar.selectbox("Menu Utama", ["Login", "Register"])
        if menu_awal == "Login":
            halaman_login()
        else:
            halaman_register()
            
    elif role == "admin":
        menu_admin()
        
    elif role == "pembeli":
        menu_pembeli(user)

if __name__ == "__main__":
    main()
