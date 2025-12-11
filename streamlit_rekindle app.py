import streamlit as st
import csv
import io

# ============================
# 1. CLASS DEFINITIONS (TETAP SAMA)
# ============================
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class ProdukLilin:
    def __init__(self, nama, harga, stok):
        self._nama = nama
        self._harga = harga
        self._stok = stok

    def get_nama(self):
        return self._nama
    
    def get_harga(self):
        return self._harga

    def get_stok(self):
        return self._stok

    def set_nama(self, nama_baru):
        self._nama = nama_baru

    def set_harga(self, harga_baru):
        self._harga = harga_baru

    def set_stok(self, stok_baru):
        self._stok = stok_baru

    def kurangi_stok(self, jumlah):
        self._stok = self._stok - jumlah

    # Di Streamlit, info() kita ubah jadi return string atau dictionary agar mudah ditampilkan
    def info_str(self):
        pesan_stok = str(self._stok)
        warning = ""
        if self._stok < 5:
            warning = " (!!! STOK MENIPIS !!!)"
        return f"{self._nama} | Rp {self._harga} | Stok: {pesan_stok}{warning}"

# ============================
# 2. INISIALISASI DATABASE (SESSION STATE)
# ============================
# Streamlit me-refresh script setiap ada interaksi. 
# Kita harus simpan data di st.session_state agar tidak hilang saat refresh.

if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": User("admin", "123", "admin"),
        "naya":  User("naya", "abc", "pembeli"),
        "shifa": User("shifa", "abc", "pembeli")
    }

if 'produk_list' not in st.session_state:
    st.session_state.produk_list = [
        ProdukLilin("Lilin Lavender", 50000, 10),
        ProdukLilin("Lilin Vanila", 45000, 3), 
        ProdukLilin("Lilin Sandalwood", 60000, 5)
    ]

if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []

if 'keranjang' not in st.session_state:
    st.session_state.keranjang = [] 

if 'inbox_laporan' not in st.session_state:
    st.session_state.inbox_laporan = []

if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# ============================
# 3. FUNGSI HELPER
# ============================
def cari_produk(nama_dicari):
    for produk in st.session_state.produk_list:
        if produk.get_nama().lower() == nama_dicari.lower():
            return produk
    return None

def convert_to_csv(data, header, type='list_obj'):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(header)
    
    if type == 'user':
        for username in data:
            u = data[username]
            writer.writerow([u.username, u.password, u.role])
    elif type == 'produk':
        for p in data:
            writer.writerow([p.get_nama(), p.get_harga(), p.get_stok()])
    elif type == 'dict':
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue() # DictWriter handle header differently inside, but here we simplify
        
    return output.getvalue()

def convert_dict_list_to_csv(data, fieldnames):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

# ============================
# 4. HALAMAN LOGIN & REGISTER
# ============================
def halaman_login():
    st.title("=== REKINDLE APP ===")
    
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Masuk"):
            user = st.session_state.users_db.get(username)
            if user is None:
                st.error("Gagal: Username tidak ditemukan!")
            elif user.password != password:
                st.error("Gagal: Password salah!")
            else:
                st.session_state.login_status = True
                st.session_state.current_user = user.username
                st.session_state.current_role = user.role
                st.success(f"Login berhasil! Halo, {user.username}")
                st.rerun()

    with tab2:
        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")
        if st.button("Daftar"):
            if st.session_state.users_db.get(new_user) is not None:
                st.error("Gagal: Username sudah terpakai!")
            elif new_user and new_pass:
                st.session_state.users_db[new_user] = User(new_user, new_pass, "pembeli")
                st.success("Sukses: Akun berhasil dibuat! Silakan Login.")
            else:
                st.warning("Username dan Password tidak boleh kosong.")

# ============================
# 5. HALAMAN ADMIN
# ============================
def menu_admin():
    st.sidebar.title("Menu Admin")
    menu = st.sidebar.radio("Pilih Menu:", 
        ["Cek Stok", "Tambah Produk", "Edit Produk", "Kelola Role", 
         "Lihat Penjualan", "Update Status", "Laporan Masalah", "Export/Import"])

    if st.sidebar.button("Logout"):
        st.session_state.login_status = False
        st.session_state.current_user = None
        st.rerun()

    st.header(f"Admin Dashboard: {menu}")

    # --- 1. CEK STOK ---
    if menu == "Cek Stok":
        data_tampil = []
        for p in st.session_state.produk_list:
            status = "Aman"
            if p.get_stok() < 5: status = "!!! STOK MENIPIS !!!"
            data_tampil.append({
                "Nama": p.get_nama(),
                "Harga": p.get_harga(),
                "Stok": p.get_stok(),
                "Status": status
            })
        st.table(data_tampil)

    # --- 2. TAMBAH PRODUK ---
    elif menu == "Tambah Produk":
        nama = st.text_input("Nama Produk")
        harga = st.number_input("Harga", min_value=0, step=1000)
        stok = st.number_input("Stok Awal", min_value=0, step=1)
        if st.button("Simpan Produk"):
            st.session_state.produk_list.append(ProdukLilin(nama, int(harga), int(stok)))
            st.success("Produk berhasil ditambahkan!")

    # --- 3. EDIT PRODUK ---
    elif menu == "Edit Produk":
        nama_list = [p.get_nama() for p in st.session_state.produk_list]
        pilih_nama = st.selectbox("Pilih Produk", nama_list)
        
        produk_ditemukan = cari_produk(pilih_nama)
        if produk_ditemukan:
            st.write(f"Edit Data: **{produk_ditemukan.get_nama()}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                baru_nama = st.text_input("Ubah Nama", value=produk_ditemukan.get_nama())
            with col2:
                baru_harga = st.number_input("Ubah Harga", value=produk_ditemukan.get_harga())
            with col3:
                baru_stok = st.number_input("Ubah Stok", value=produk_ditemukan.get_stok())
            
            if st.button("Update Produk"):
                produk_ditemukan.set_nama(baru_nama)
                produk_ditemukan.set_harga(int(baru_harga))
                produk_ditemukan.set_stok(int(baru_stok))
                st.success("Data produk berhasil diupdate!")

    # --- 4. KELOLA ROLE USER ---
    elif menu == "Kelola Role":
        list_users = list(st.session_state.users_db.keys())
        target_username = st.selectbox("Pilih User", list_users)
        
        user_obj = st.session_state.users_db[target_username]
        st.write(f"Role saat ini: **{user_obj.role}** | Password: **{user_obj.password}**")

        opsi_edit = st.selectbox("Mau edit apa?", ["Role", "Password", "Rename User"])
        
        if opsi_edit == "Role":
            role_baru = st.selectbox("Pilih Role Baru", ["admin", "pembeli"])
            if st.button("Simpan Role"):
                user_obj.role = role_baru
                st.success("Role berubah.")
        
        elif opsi_edit == "Password":
            pass_baru = st.text_input("Password Baru")
            if st.button("Simpan Password"):
                user_obj.password = pass_baru
                st.success("Password berubah.")

        elif opsi_edit == "Rename User":
            nama_baru = st.text_input("Username Baru")
            if st.button("Ganti Username"):
                if nama_baru in st.session_state.users_db:
                    st.error("Nama sudah dipakai!")
                else:
                    user_obj.username = nama_baru
                    st.session_state.users_db[nama_baru] = user_obj
                    del st.session_state.users_db[target_username]
                    st.success(f"Berubah menjadi {nama_baru}")
                    st.rerun()

    # --- 5. LIHAT PENJUALAN ---
    elif menu == "Lihat Penjualan":
        search = st.text_input("Cari Nama Pembeli (Opsional)")
        total_pendapatan = 0
        data_sales = []
        
        for t in st.session_state.riwayat_transaksi:
            if search.lower() in t['pembeli'].lower():
                data_sales.append(t)
                total_pendapatan += t['total']
        
        if data_sales:
            st.dataframe(data_sales)
            st.info(f"TOTAL PENDAPATAN (Tampil): Rp {total_pendapatan}")
        else:
            st.warning("Belum ada data penjualan.")

    # --- 6. UPDATE STATUS ---
    elif menu == "Update Status":
        if not st.session_state.riwayat_transaksi:
            st.write("Tidak ada transaksi.")
        else:
            # Buat list string untuk selectbox
            options = []
            for i, t in enumerate(st.session_state.riwayat_transaksi):
                options.append(f"{i+1}. {t['pembeli']} - {t['barang']} [{t['status']}]")
            
            pilihan = st.selectbox("Pilih Transaksi", options)
            index = int(pilihan.split(".")[0]) - 1
            
            new_status = st.selectbox("Set Status Baru", ["Diproses", "Sedang Dikirim", "Selesai"])
            if st.button("Update Status"):
                st.session_state.riwayat_transaksi[index]['status'] = new_status
                st.success(f"Status diubah jadi {new_status}")
                st.rerun()

    # --- 7. LAPORAN MASALAH ---
    elif menu == "Laporan Masalah":
        if not st.session_state.inbox_laporan:
            st.write("Inbox Kosong.")
        else:
            for i, msg in enumerate(st.session_state.inbox_laporan):
                with st.expander(f"Pesan dari {msg['pengirim']} (Status: {msg['jawaban']})"):
                    st.write(f"**Keluhan:** {msg['pesan']}")
                    balasan = st.text_input(f"Jawab pesan #{i+1}", key=f"ans_{i}")
                    if st.button(f"Kirim Balasan #{i+1}", key=f"btn_{i}"):
                        st.session_state.inbox_laporan[i]['jawaban'] = balasan
                        st.success("Balasan terkirim.")
                        st.rerun()

    # --- 8. EXPORT / IMPORT ---
    elif menu == "Export/Import":
        st.subheader("Export Data (Download CSV)")
        
        # 1. Export User
        csv_users = convert_to_csv(st.session_state.users_db, ['Username', 'Password', 'Role'], 'user')
        st.download_button("Download Data User", csv_users, "data_users.csv", "text/csv")
        
        # 2. Export Produk
        csv_produk = convert_to_csv(st.session_state.produk_list, ['Nama Produk', 'Harga', 'Stok'], 'produk')
        st.download_button("Download Data Produk", csv_produk, "data_produk.csv", "text/csv")

        # 3. Export Penjualan
        if st.session_state.riwayat_transaksi:
            csv_sales = convert_dict_list_to_csv(st.session_state.riwayat_transaksi, ['pembeli', 'barang', 'qty', 'total', 'status'])
            st.download_button("Download Data Penjualan", csv_sales, "data_penjualan.csv", "text/csv")

        st.divider()
        st.subheader("Import Data (Upload CSV)")
        uploaded_file = st.file_uploader("Upload File CSV (Contoh: data_produk.csv)")
        
        if uploaded_file is not None:
            tipe_import = st.selectbox("Ini file apa?", ["User", "Produk", "Penjualan"])
            if st.button("Proses Import"):
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                
                if tipe_import == "User":
                    reader = csv.reader(stringio)
                    next(reader) # skip header
                    st.session_state.users_db.clear()
                    for row in reader:
                        st.session_state.users_db[row[0]] = User(row[0], row[1], row[2])
                    st.success("Import User Sukses!")

                elif tipe_import == "Produk":
                    reader = csv.reader(stringio)
                    next(reader)
                    st.session_state.produk_list.clear()
                    for row in reader:
                        st.session_state.produk_list.append(ProdukLilin(row[0], int(row[1]), int(row[2])))
                    st.success("Import Produk Sukses!")
                
                elif tipe_import == "Penjualan":
                    reader = csv.DictReader(stringio)
                    st.session_state.riwayat_transaksi.clear()
                    for row in reader:
                        row['qty'] = int(row['qty'])
                        row['total'] = int(row['total'])
                        st.session_state.riwayat_transaksi.append(row)
                    st.success("Import Penjualan Sukses!")


# ============================
# 6. HALAMAN PEMBELI
# ============================
def menu_pembeli():
    user_login = st.session_state.current_user
    st.sidebar.title(f"Halo, {user_login}")
    menu = st.sidebar.radio("Menu Pembeli:", ["Belanja", "Keranjang & Bayar", "Pesanan Saya", "Pusat Bantuan"])
    
    if st.sidebar.button("Logout"):
        # Reset keranjang saat logout (opsional, tapi bagus utk UX)
        st.session_state.keranjang = [] 
        st.session_state.login_status = False
        st.rerun()

    # --- 1. BELANJA ---
    if menu == "Belanja":
        st.header("Katalog Produk")
        
        # Tampilan Grid Sederhana
        cols = st.columns(2)
        for i, produk in enumerate(st.session_state.produk_list):
            with cols[i % 2]:
                st.write("---")
                st.subheader(produk.get_nama())
                st.write(f"Harga: Rp {produk.get_harga()}")
                st.write(f"Sisa Stok: {produk.get_stok()}")
                
                with st.form(key=f"beli_{i}"):
                    qty = st.number_input("Jumlah", min_value=1, max_value=produk.get_stok() if produk.get_stok() > 0 else 1, key=f"q_{i}")
                    add_btn = st.form_submit_button("Masuk Keranjang")
                    
                    if add_btn:
                        if produk.get_stok() < qty:
                            st.error("Stok tidak cukup!")
                        else:
                            item_belanja = {
                                "obj_produk": produk, # Reference object
                                "nama": produk.get_nama(),
                                "harga": produk.get_harga(),
                                "qty": int(qty)
                            }
                            st.session_state.keranjang.append(item_belanja)
                            st.success(f"Masuk keranjang: {produk.get_nama()} (x{qty})")

    # --- 2. KERANJANG & BAYAR ---
    elif menu == "Keranjang & Bayar":
        st.header("Keranjang Belanja")
        if not st.session_state.keranjang:
            st.info("Keranjang Anda kosong.")
        else:
            total_belanja = 0
            total_qty = 0
            
            # Tampilkan list
            for item in st.session_state.keranjang:
                subtotal = item['harga'] * item['qty']
                st.write(f"- **{item['nama']}** (x{item['qty']}) = Rp {subtotal}")
                total_belanja += subtotal
                total_qty += item['qty']
            
            st.divider()
            
            # Logika Diskon (Sama persis dengan source asli)
            persen_diskon = 0
            if total_qty >= 5:
                persen_diskon = 20
            elif total_qty >= 3:
                persen_diskon = 10
            
            potongan_harga = total_belanja * (persen_diskon / 100)
            total_akhir = total_belanja - potongan_harga
            
            st.write(f"Total Awal: Rp {int(total_belanja)}")
            if persen_diskon > 0:
                st.success(f"DISKON {persen_diskon}%: -Rp {int(potongan_harga)}")
            else:
                st.write("DISKON: - (Beli min 3 items dapat diskon!)")
            
            st.subheader(f"TOTAL BAYAR: Rp {int(total_akhir)}")
            
            if st.button("Bayar Sekarang"):
                # Proses kurangi stok dan catat history
                for item in st.session_state.keranjang:
                    # Method kurangi stok dari Class
                    item['obj_produk'].kurangi_stok(item['qty'])
                    
                    st.session_state.riwayat_transaksi.append({
                        "pembeli": user_login,
                        "barang": item['nama'],
                        "qty": item['qty'],
                        "total": item['harga'] * item['qty'],
                        "status": "Diproses"
                    })
                
                st.session_state.keranjang.clear()
                st.balloons()
                st.success("Pembayaran LUNAS! Terima kasih.")

    # --- 3. PESANAN SAYA ---
    elif menu == "Pesanan Saya":
        st.header("Riwayat Pesanan")
        found = False
        for t in st.session_state.riwayat_transaksi:
            if t['pembeli'] == user_login:
                st.info(f"{t['barang']} (x{t['qty']}) | Total: Rp {t['total']} | Status: [{t['status']}]")
                found = True
        if not found:
            st.write("Belum ada riwayat pesanan.")

    # --- 4. PUSAT BANTUAN ---
    elif menu == "Pusat Bantuan":
        st.header("Lapor Masalah")
        
        tab_tulis, tab_riwayat = st.tabs(["Tulis Laporan", "Lihat Balasan"])
        
        with tab_tulis:
            pesan_user = st.text_area("Tulis keluhan Anda:")
            if st.button("Kirim Laporan"):
                st.session_state.inbox_laporan.append({
                    "pengirim": user_login,
                    "pesan": pesan_user,
                    "jawaban": "Belum dibalas"
                })
                st.success("Laporan terkirim ke Admin.")
        
        with tab_riwayat:
            found = False
            for chat in st.session_state.inbox_laporan:
                if chat['pengirim'] == user_login:
                    st.write(f"**Q (Anda):** {chat['pesan']}")
                    st.write(f"**A (Admin):** {chat['jawaban']}")
                    st.write("---")
                    found = True
            if not found:
                st.write("Belum ada riwayat.")


# ============================
# 7. MAIN LOGIC (ROUTING)
# ============================
if __name__ == "__main__":
    if not st.session_state.login_status:
        halaman_login()
    else:
        role = st.session_state.current_role
        if role == "admin":
            menu_admin()
        else:
            menu_pembeli()
