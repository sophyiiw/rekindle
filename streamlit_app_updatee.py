import streamlit as st
import csv
import io

# ============================
# 1. KONFIGURASI HALAMAN
# ============================
st.set_page_config(
    page_title="Rekindle Candle Shop",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================
# 2. CSS STYLING
# ============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #333333;
    }

    /* BACKGROUND UTAMA CREAM */
    .stApp {
        background-color: #FAF9F6;
    }

    /* INPUT STYLING */
    [data-testid="stTextInput"] { margin-bottom: 15px; }
    [data-testid="stTextInput"] > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 15px !important;
        color: #333333 !important;
        box-shadow: none !important;
        align-items: center;
    }
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: #000000 !important;
        border-width: 2px !important;
    }
    [data-testid="stTextInput"] input {
        background-color: transparent !important;
        color: #333333 !important;
        border: none !important;
    }
    [data-testid="stTextInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #555555 !important;
    }
    [data-testid="stTextInput"] input::placeholder { color: #888888 !important; opacity: 1; }
    [data-testid="stTextInput"] label { display: none; }

    /* TABS & BUTTONS */
    button[data-baseweb="tab"] > div { color: #888888 !important; }
    button[data-baseweb="tab"][aria-selected="true"] > div { color: #000000 !important; font-weight: bold; }
    button[data-baseweb="tab"][aria-selected="true"] { border-bottom-color: #000000 !important; }

    .stButton > button {
        background-color: #1A1A1A !important;
        color: white !important;
        border-radius: 30px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #000000 !important;
        transform: scale(1.01);
    }

    /* GLASS CARD & HERO */
    .right-image-container {
        position: relative;
        width: 100%;
        height: 90vh;
        border-radius: 20px;
        overflow: hidden;
        background-image: url('https://images.unsplash.com/photo-1602523961358-f9f03dd557db?q=80&w=1000&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
    }
    .glass-card {
        position: absolute;
        top: 50%;
        right: -40px;
        transform: translateY(-50%);
        width: 85%;
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    .glass-text-title { font-size: 1.8rem; font-weight: 700; color: #000000; margin-bottom: 10px; }
    .glass-text-body { font-size: 1rem; color: #333333; }
    .hero-title { font-size: 3rem; font-weight: 700; color: #000000; }
    .hero-subtitle { font-size: 1.1rem; color: #555555; margin-bottom: 2rem; }
    
    .block-container { padding-top: 2rem; max-width: 100%; }

    /* KATALOG IMAGE STYLING */
    div[data-testid="stImage"] img {
        border-radius: 100px 100px 0 0 !important;
        aspect-ratio: 3 / 4 !important;
        object-fit: cover !important;
        width: 100% !important;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# URL Gambar (Konstanta Visual)
IMG_LAVENDER = "https://i.pinimg.com/736x/1f/7a/b3/1f7ab3ca70a7368b15d124be258c3baa.jpg"
IMG_VANILLA = "https://i.pinimg.com/1200x/3c/23/a0/3c23a06d1d6ed7ade0b75d58d1967072.jpg"
IMG_SANDALWOOD = "https://i.pinimg.com/1200x/7b/c3/9b/7bc39b94e139510186d56d134256a1c0.jpg"

# ============================
# 3. CLASS & DATABASE
# ============================
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class ProdukLilin:
    # Constructor menggabungkan data logika (harga, stok) dan visual (img_url)
    def __init__(self, nama, harga, stok, img_url="https://via.placeholder.com/150"):
        self._nama = nama
        self._harga = harga
        self._stok = stok
        self.img_url = img_url 

    # --- Getter & Setter ---
    def get_nama(self): return self._nama
    def get_harga(self): return self._harga
    def get_stok(self): return self._stok
    def set_nama(self, nama_baru): self._nama = nama_baru
    def set_harga(self, harga_baru): self._harga = harga_baru
    def set_stok(self, stok_baru): self._stok = stok_baru
    
    # --- Logic Bisnis ---
    def kurangi_stok(self, jumlah): 
        self._stok = self._stok - jumlah

    def info_str(self):
        pesan_stok = str(self._stok)
        warning = ""
        if self._stok < 5: warning = " (!!! STOK MENIPIS !!!)"
        return f"{self._nama} | Rp {self._harga} | Stok: {pesan_stok}{warning}"

# --- Helper Functions ---
def cari_produk(nama_dicari):
    for produk in st.session_state['produk_list']:
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
    return output.getvalue()

def convert_dict_list_to_csv(data, fieldnames):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

# --- Init State ---
def init_state():
    if 'users_db' not in st.session_state:
        st.session_state['users_db'] = {
            "admin": User("admin", "123", "admin"),
            "naya":  User("naya", "abc", "pembeli"),
            "shifa": User("shifa", "abc", "pembeli")
        }
    if 'produk_list' not in st.session_state:
        st.session_state['produk_list'] = [
            ProdukLilin("Lilin Lavender", 50000, 10, IMG_LAVENDER),
            ProdukLilin("Lilin Vanila", 45000, 3, IMG_VANILLA), 
            ProdukLilin("Lilin Sandalwood", 60000, 5, IMG_SANDALWOOD)
        ]
    if 'riwayat_transaksi' not in st.session_state: st.session_state['riwayat_transaksi'] = []
    if 'keranjang' not in st.session_state: st.session_state['keranjang'] = []
    if 'inbox_laporan' not in st.session_state: st.session_state['inbox_laporan'] = []
    if 'user_role' not in st.session_state: st.session_state['user_role'] = None 
    if 'user_login' not in st.session_state: st.session_state['user_login'] = ""

init_state()

# ============================
# 4. HALAMAN DEPAN
# ============================
def halaman_depan_split():
    col_kiri, col_kanan = st.columns([1, 1.2], gap="large")

    # --- KOLOM KIRI ---
    with col_kiri:
        st.write("") 
        st.write("") 
        st.write("") 
        
        st.markdown('<div class="hero-title">Hi! Precious People</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Eco Aromatherapy Candle Since 2025.</div>', unsafe_allow_html=True)
        
        # Tabs untuk Login/Register
        tab_login, tab_daftar = st.tabs(["Login Akun", "Daftar Baru"])
        
        with tab_login:
            st.write("")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Masukkan username...", label_visibility="collapsed")
                st.write("")
                password = st.text_input("Password", type="password", placeholder="Masukkan password...", label_visibility="collapsed")
                st.write("")
                submitted = st.form_submit_button("Masuk")
                
                if submitted:
                    user = st.session_state['users_db'].get(username)
                    if user is None:
                        st.error("Username tidak ditemukan.")
                    elif user.password != password:
                        st.error("Password salah.")
                    else:
                        st.session_state['user_role'] = user.role
                        st.session_state['user_login'] = user.username
                        st.success(f"Berhasil masuk, {user.username}!")
                        st.rerun()

        with tab_daftar:
            st.write("")
            with st.form("reg_form"):
                username_baru = st.text_input("Username baru", placeholder="Buat username unik...", label_visibility="collapsed")
                st.write("")
                password_baru = st.text_input("Password baru", type="password", placeholder="Buat password...", label_visibility="collapsed")
                st.write("")
                submitted = st.form_submit_button("Daftar Sekarang")
                
                if submitted:
                    if username_baru in st.session_state['users_db']:
                        st.error("Username sudah terpakai.")
                    elif username_baru == "":
                        st.error("Username tidak boleh kosong.")
                    else:
                        st.session_state['users_db'][username_baru] = User(username_baru, password_baru, "pembeli")
                        st.success("Akun berhasil dibuat! Silakan Login.")
        
        st.write("")
        st.caption("Butuh bantuan? Hubungi support@rekindle.com")

    # --- KOLOM KANAN (GLASS CARD) ---
    with col_kanan:
        st.markdown("""
        <div class="right-image-container">
            <div class="glass-card">
                <div class="glass-text-title">
                    Light Up, Breathe Easy From Waste to Wellness
                </div>
                <div class="glass-text-body">
                    Koleksi lilin aromaterapi kami dirancang untuk menciptakan 
                    ketenangan dan estetika terbaik. Temukan wangi favoritmu sekarang.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================
# 5. HALAMAN ADMIN
# ============================
def menu_admin():
    st.sidebar.title("Admin Dashboard")
    menu = st.sidebar.radio("Menu:", 
        ["Cek Stok", "Tambah Produk", "Edit Produk", "Kelola Role", 
         "Lihat Penjualan", "Update Status", "Laporan Masalah", "Export/Import", "Logout"])

    # 1. Cek Stok
    if menu == "Cek Stok":
        st.title("Stok Gudang")
        data_tampil = []
        for p in st.session_state['produk_list']:
            status = "Aman"
            if p.get_stok() < 5: status = "!!! STOK MENIPIS !!!"
            data_tampil.append({
                "Nama": p.get_nama(), "Harga": p.get_harga(), "Stok": p.get_stok(), "Status": status
            })
        st.table(data_tampil)

    # 2. Tambah Produk
    elif menu == "Tambah Produk":
        st.title("Tambah Produk Baru")
        nama = st.text_input("Nama Produk")
        harga = st.number_input("Harga", min_value=0, step=1000)
        stok = st.number_input("Stok Awal", min_value=0, step=1)
        if st.button("Simpan Produk"):
            st.session_state['produk_list'].append(ProdukLilin(nama, int(harga), int(stok), "https://via.placeholder.com/150"))
            st.success("Produk berhasil ditambahkan!")

    # 3. Edit Produk
    elif menu == "Edit Produk":
        st.title("Edit Produk")
        nama_list = [p.get_nama() for p in st.session_state['produk_list']]
        pilih_nama = st.selectbox("Pilih Produk", nama_list)
        produk_ditemukan = cari_produk(pilih_nama)
        
        if produk_ditemukan:
            c1, c2, c3 = st.columns(3)
            with c1: new_n = st.text_input("Ubah Nama", value=produk_ditemukan.get_nama())
            with c2: new_h = st.number_input("Ubah Harga", value=produk_ditemukan.get_harga())
            with c3: new_s = st.number_input("Ubah Stok", value=produk_ditemukan.get_stok())
            if st.button("Update"):
                produk_ditemukan.set_nama(new_n)
                produk_ditemukan.set_harga(int(new_h))
                produk_ditemukan.set_stok(int(new_s))
                st.success("Update Berhasil")

    # 4. Kelola Role
    elif menu == "Kelola Role":
        st.title("Manajemen User")
        list_users = list(st.session_state['users_db'].keys())
        target = st.selectbox("Pilih User", list_users)
        user_obj = st.session_state['users_db'][target]
        st.write(f"Role: **{user_obj.role}** | Pass: **{user_obj.password}**")
        
        opsi = st.selectbox("Action", ["Ganti Role", "Ganti Password", "Rename User"])
        if opsi == "Ganti Role":
            r_baru = st.selectbox("Role Baru", ["admin", "pembeli"])
            if st.button("Simpan"): user_obj.role = r_baru; st.success("Saved.")
        elif opsi == "Ganti Password":
            p_baru = st.text_input("Password Baru")
            if st.button("Simpan"): user_obj.password = p_baru; st.success("Saved.")
        elif opsi == "Rename User":
            n_baru = st.text_input("Username Baru")
            if st.button("Simpan"):
                if n_baru in st.session_state['users_db']: st.error("Taken!")
                else:
                    user_obj.username = n_baru
                    st.session_state['users_db'][n_baru] = user_obj
                    del st.session_state['users_db'][target]
                    st.success("Renamed!"); st.rerun()

    # 5. Lihat Penjualan
    elif menu == "Lihat Penjualan":
        st.title("Laporan Penjualan")
        search = st.text_input("Cari Pembeli")
        data = [t for t in st.session_state['riwayat_transaksi'] if search.lower() in t['pembeli'].lower()]
        st.dataframe(data)
        st.info(f"Total Pendapatan: Rp {sum(t['total'] for t in data)}")

    # 6. Update Status
    elif menu == "Update Status":
        st.title("Update Status Pesanan")
        if not st.session_state['riwayat_transaksi']: st.write("Kosong.")
        else:
            opts = [f"{i+1}. {t['pembeli']} - {t['barang']} [{t['status']}]" for i,t in enumerate(st.session_state['riwayat_transaksi'])]
            pilih = st.selectbox("Pilih", opts)
            idx = int(pilih.split(".")[0]) - 1
            stat = st.selectbox("Status Baru", ["Diproses", "Sedang Dikirim", "Selesai"])
            if st.button("Update"):
                st.session_state['riwayat_transaksi'][idx]['status'] = stat
                st.success("Updated!"); st.rerun()

    # 7. Laporan Masalah
    elif menu == "Laporan Masalah":
        st.title("Inbox Keluhan")
        for i, msg in enumerate(st.session_state['inbox_laporan']):
            with st.expander(f"Dari {msg['pengirim']} ({msg['jawaban']})"):
                st.write(msg['pesan'])
                balas = st.text_input(f"Balas #{i}", key=f"b{i}")
                if st.button(f"Kirim #{i}", key=f"k{i}"):
                    st.session_state['inbox_laporan'][i]['jawaban'] = balas
                    st.success("Terkirim"); st.rerun()

    # 8. Export/Import
    elif menu == "Export/Import":
        st.title("Backup Data")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Export CSV")
            csv_u = convert_to_csv(st.session_state['users_db'], ['User','Pass','Role'], 'user')
            st.download_button("Download User", csv_u, "users.csv", "text/csv")
            csv_p = convert_to_csv(st.session_state['produk_list'], ['Nama','Harga','Stok'], 'produk')
            st.download_button("Download Produk", csv_p, "produk.csv", "text/csv")
        with c2:
            st.subheader("Import CSV")
            upl = st.file_uploader("Upload File")
            jenis = st.selectbox("Jenis", ["User", "Produk", "Penjualan"])
            if upl and st.button("Import"):
                sio = io.StringIO(upl.getvalue().decode("utf-8"))
                if jenis == "User":
                    r = csv.reader(sio); next(r)
                    st.session_state['users_db'] = {row[0]: User(row[0], row[1], row[2]) for row in r}
                elif jenis == "Produk":
                    r = csv.reader(sio); next(r)
                    st.session_state['produk_list'] = [ProdukLilin(row[0], int(row[1]), int(row[2])) for row in r]
                st.success("Import Sukses")

    elif menu == "Logout":
        st.session_state['user_role'] = None; st.rerun()

# ============================
# 6. HALAMAN PEMBELI
# ============================
def menu_pembeli(user):
    st.sidebar.title(f"Halo, {user}")
    menu = st.sidebar.selectbox("Menu:", ["Katalog", "Keranjang", "Pesanan Saya", "Pusat Bantuan", "Logout"])
    
    # --- KATALOG ---
    if menu == "Katalog":
        st.markdown("<h1 style='color: #000000;'>Katalog Produk</h1>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, p in enumerate(st.session_state['produk_list']):
            with cols[i%3]:
                st.image(p.img_url)
                st.markdown(f"""
                <div style="text-align: left; margin-top: 5px;">
                    <div style="font-weight: bold; font-size: 1.1rem; color: #000000;">{p.get_nama()}</div>
                    <div style="color: #333333;">Rp {p.get_harga()} | Stok: {p.get_stok()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form(key=f"f_{i}"):
                    qty = st.number_input("Qty", 1, max(1, p.get_stok()), key=f"q_{i}")
                    if st.form_submit_button("Beli"):
                        if p.get_stok() < qty: st.error("Stok Kurang!")
                        else:
                            st.session_state['keranjang'].append({
                                "obj_produk": p,
                                "nama": p.get_nama(), 
                                "harga": p.get_harga(),
                                "qty": int(qty)
                            })
                            st.toast("Masuk Keranjang!")

    # --- KERANJANG (BAGIAN YANG DIPERBAIKI INDENTASINYA) ---
    elif menu == "Keranjang":
        st.title("Your Cart")
        cart = st.session_state['keranjang']
        if not cart:
            st.info("Keranjang Kosong.")
        else:
            col_kiri, col_kanan = st.columns([2, 1], gap="large")
            
            # Perbaikan Indentasi dimulai dari sini
            with col_kiri:
                st.subheader("Product List")
                st.markdown("---")
                for i, item in enumerate(cart):
                    c1, c2, c3, c4 = st.columns([1.5, 3, 2, 1])
                    with c1: 
                        st.image(item['obj_produk'].img_url, width=80)
                    with c2: 
                        st.markdown(f"**{item['nama']}**")
                        st.caption(f"Qty: {item['qty']}")
                    with c3: 
                        st.markdown(f"**Rp {item['harga'] * item['qty']:,}**")
                    with c4:
                        if st.button("✕", key=f"d_{i}"):
                            cart.pop(i); st.rerun()
                    st.markdown("---")

            # Bagian Kanan
            with col_kanan:
                total_qty = sum(item['qty'] for item in cart)
                subtotal = sum(item['harga'] * item['qty'] for item in cart)
                
                diskon_persen = 0
                if total_qty >= 5: diskon_persen = 20
                elif total_qty >= 3: diskon_persen = 10
                
                potongan = subtotal * (diskon_persen / 100)
                total_akhir = subtotal - potongan

                st.markdown("""
                <div style="background-color: #F3F3F3; padding: 25px; border-radius: 15px; color: #333;">
                    <h4 style="margin-top:0; color: #000;">Cart Totals</h4>
                    <hr style="border-top: 1px solid #ccc;">
                </div>""", unsafe_allow_html=True)
                
                st.write(f"Subtotal: Rp {subtotal:,}")
                if diskon_persen > 0:
                    st.success(f"Diskon {diskon_persen}%: -Rp {int(potongan):,}")
                else:
                    st.caption("Beli min 3 items dapat diskon!")
                st.write(f"**Total: Rp {int(total_akhir):,}**")
                
                if st.button("Checkout Sekarang"):
                    for item in cart:
                        item['obj_produk'].kurangi_stok(item['qty'])
                        st.session_state['riwayat_transaksi'].append({
                            "pembeli": user,
                            "barang": item['nama'],
                            "qty": item['qty'],
                            "total": int(item['harga'] * item['qty']),
                            "status": "Diproses"
                        })
                    st.session_state['keranjang'] = []
                    st.balloons()
                    st.success("Pembayaran Berhasil!"); st.rerun()

    # --- PESANAN SAYA ---
    elif menu == "Pesanan Saya":
        st.title("Riwayat Pesanan")
        found = False
        for t in st.session_state['riwayat_transaksi']:
            if t['pembeli'] == user:
                st.info(f"{t['barang']} (x{t['qty']}) | Total: Rp {t['total']} | Status: [{t['status']}]")
                found = True
        if not found: st.write("Belum ada pesanan.")

    # --- PUSAT BANTUAN ---
    elif menu == "Pusat Bantuan":
        st.title("Pusat Bantuan")
        tab1, tab2 = st.tabs(["Tulis Laporan", "Riwayat"])
        with tab1:
            pesan = st.text_area("Keluhan:")
            if st.button("Kirim"):
                st.session_state['inbox_laporan'].append({"pengirim": user, "pesan": pesan, "jawaban": "Belum dibalas"})
                st.success("Terkirim")
        with tab2:
            for chat in st.session_state['inbox_laporan']:
                if chat['pengirim'] == user:
                    st.write(f"Q: {chat['pesan']}"); st.write(f"A: {chat['jawaban']}"); st.markdown("---")

    elif menu == "Logout":
        st.session_state['keranjang'] = []
        st.session_state['user_role'] = None
        st.session_state['user_login'] = ""
        st.rerun()

# ============================
# 7. MAIN PROGRAM
# ============================
def main():
    role = st.session_state['user_role']
    if role is None:
        halaman_depan_split()
    elif role == "admin":
        menu_admin()
    elif role == "pembeli":
        menu_pembeli(st.session_state['user_login'])

if __name__ == "__main__":
    main()

