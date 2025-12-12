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

    /* A. SIDEBAR (KIRI): SEMUA TEKS WAJIB PUTIH */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
    }

    /* B. KONTEN UTAMA (KANAN): JUDUL & PARAGRAF WAJIB HITAM (Supaya kebaca di Cream) */
    .main h1, .main h2, .main h3, .main h4, 
    .main p, .main li, .main label, .main .stMarkdown {
        color: #000000 !important;
    }

    /* C. TOMBOL (PENYELAMAT): TEKS DI DALAM TOMBOL WAJIB PUTIH KEMBALI */
    /* Ini akan menimpa aturan B khusus untuk teks di dalam tombol */
    button p, 
    div[role="button"] p, 
    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-primary"] p {
        color: #FFFFFF !important;
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
    
    /* KATALOG IMAGE */
    div[data-testid="stImage"] img {
        border-radius: 100px 100px 0 0 !important;
        aspect-ratio: 3 / 4 !important;
        object-fit: cover !important;
        width: 100% !important;
        margin-bottom: 10px;
    }
/* ============================================================ */
    /* 👇 PERBAIKAN KHUSUS ADMIN (TABEL JADI HITAM) 👇             */
    /* ============================================================ */
    
    /* Memaksa semua teks dalam tabel berwarna HITAM */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        color: #000000 !important;
    }

    /* Header Tabel (Nama Kolom) */
    div[data-testid="stTable"] th, div[data-testid="stDataFrame"] th {
        color: #000000 !important;
        background-color: #E0E0E0 !important; /* Abu-abu muda supaya header jelas */
        border-bottom: 2px solid #000000 !important;
    }

    /* Isi Tabel (Data) */
    div[data-testid="stTable"] td, div[data-testid="stDataFrame"] td {
        color: #000000 !important;
        background-color: transparent !important;
        border-bottom: 1px solid #CCCCCC !important;
    }
    /* ============================================================ */
</style>
""", unsafe_allow_html=True)



# URL Gambar
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
    def __init__(self, nama, harga, stok, img_url="https://via.placeholder.com/150"):
        self._nama = nama
        self._harga = harga
        self._stok = stok
        self.img_url = img_url 

    def get_nama(self): return self._nama
    def get_harga(self): return self._harga
    def get_stok(self): return self._stok
    def set_nama(self, n): self._nama = n
    def set_harga(self, h): self._harga = h
    def set_stok(self, s): self._stok = s
    def kurangi_stok(self, n): self._stok -= n

def cari_produk(nama):
    for p in st.session_state['produk_list']:
        if p.get_nama().lower() == nama.lower(): return p
    return None

def convert_dict_list_to_csv(data, fieldnames):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def convert_to_csv(data, header, type='list_obj'):
    output = io.StringIO(); writer = csv.writer(output); writer.writerow(header)
    if type == 'user':
        for u in data: writer.writerow([data[u].username, data[u].password, data[u].role])
    elif type == 'produk':
        for p in data: writer.writerow([p.get_nama(), p.get_harga(), p.get_stok()])
    return output.getvalue()

def init_state():
    if 'users_db' not in st.session_state:
        st.session_state['users_db'] = {
            "admin": User("admin", "123", "admin"),
            "naya":  User("naya", "abc", "pembeli"),
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
    with col_kiri:
        st.write(""); st.write(""); st.write("")
        st.markdown('<div class="hero-title">Hi! Precious People</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Eco Aromatherapy Candle Since 2025.</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Daftar"])
        with tab1:
            with st.form("login"):
                u = st.text_input("User", placeholder="Username"); p = st.text_input("Pass", type="password", placeholder="Password")
                if st.form_submit_button("Masuk"):
                    user = st.session_state['users_db'].get(u)
                    if user and user.password == p:
                        st.session_state['user_role'] = user.role
                        st.session_state['user_login'] = user.username
                        st.rerun()
                    else: st.error("Gagal Login")
        with tab2:
            with st.form("reg"):
                u = st.text_input("User Baru", placeholder="Username Baru"); p = st.text_input("Pass Baru", type="password", placeholder="Password Baru")
                if st.form_submit_button("Daftar"):
                    if u not in st.session_state['users_db'] and u:
                        st.session_state['users_db'][u] = User(u, p, "pembeli")
                        st.success("Berhasil! Silakan Login.")
                    else: st.error("Username sudah ada / kosong.")

    with col_kanan:
        st.markdown("""<div class="right-image-container"><div class="glass-card">
        <div class="glass-text-title">Light Up, Breathe Easy</div>
        <div class="glass-text-body">Koleksi lilin aromaterapi terbaik untuk ketenangan Anda.</div></div></div>""", unsafe_allow_html=True)

# ============================
# 5. HALAMAN ADMIN
# ============================
def menu_admin():
    st.sidebar.title("Admin Panel")
    menu = st.sidebar.radio("Menu", ["Stok", "Tambah", "Edit", "Kelola User", "Penjualan", "Update Status", "Laporan", "Export/Import", "Logout"])
    
    if menu == "Stok":
        st.title("Gudang")
        st.table([{"Nama": p.get_nama(), "Harga": p.get_harga(), "Stok": p.get_stok()} for p in st.session_state['produk_list']])
    
    elif menu == "Tambah":
        st.title("Tambah Produk")
        
        with st.form("form_tambah_produk"):
            n = st.text_input("Nama Produk")
            h = st.number_input("Harga (Rp)", min_value=0, step=500)
            s = st.number_input("Stok Awal", min_value=0, step=1)
            
            # 1. Tambahkan Widget File Uploader
            uploaded_file = st.file_uploader("Upload Gambar Produk", type=['png', 'jpg', 'jpeg'])
            
            submit = st.form_submit_button("Simpan Produk")

            if submit:
                if n and h > 0:
                    # 2. Logika Penentuan Gambar
                    # Jika ada file diupload, pakai file itu. Jika tidak, pakai gambar default.
                    gambar_final = "https://via.placeholder.com/150" # Default jika kosong
                    
                    if uploaded_file is not None:
                        gambar_final = uploaded_file # Simpan objek file langsung
                    
                    # 3. Masukkan ke database session
                    st.session_state['produk_list'].append(
                        ProdukLilin(n, int(h), int(s), gambar_final)
                    )
                    st.success(f"Berhasil menambahkan {n}!")
                else:
                    st.error("Nama tidak boleh kosong dan Harga harus > 0")

    elif menu == "Edit":
        st.title("Edit Produk")
        names = [p.get_nama() for p in st.session_state['produk_list']]
        sel = st.selectbox("Produk", names)
        p = cari_produk(sel)
        if p:
            nn = st.text_input("Nama", p.get_nama())
            nh = st.number_input("Harga", value=p.get_harga())
            ns = st.number_input("Stok", value=p.get_stok())
            if st.button("Update"): p.set_nama(nn); p.set_harga(nh); p.set_stok(ns); st.success("Updated")

    elif menu == "Kelola User":
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
                    
    elif menu == "Penjualan":
        st.title("Riwayat Penjualan")
        st.dataframe(st.session_state['riwayat_transaksi'])

    elif menu == "Update Status":
        st.title("Update Status")
        if not st.session_state['riwayat_transaksi']: st.write("Belum ada transaksi.")
        else:
            opts = [f"{i+1}. {t['pembeli']} - {t['barang']} [{t['status']}]" for i,t in enumerate(st.session_state['riwayat_transaksi'])]
            sel = st.selectbox("Pilih Pesanan", opts)
            idx = int(sel.split(".")[0])-1
            stat = st.selectbox("Status Baru", ["Diproses", "Sedang Dikirim", "Selesai"])
            if st.button("Update"): 
                st.session_state['riwayat_transaksi'][idx]['status'] = stat
                st.success("Status Updated"); st.rerun()

    elif menu == "Laporan":
        st.title("Laporan Masuk")
        for i, m in enumerate(st.session_state['inbox_laporan']):
            with st.expander(f"Pesan dari {m['pengirim']}"):
                st.write(f"Isi: {m['pesan']}")
                b = st.text_input(f"Jawab #{i}", key=f"b{i}")
                if st.button("Kirim Balasan", key=f"k{i}"): m['jawaban'] = b; st.success("Terkirim")

    elif menu == "Export/Import":
        st.subheader("📥 Export Data (Download)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Export User
            csv_users = convert_to_csv(st.session_state.users_db, ['Username', 'Password', 'Role'], 'user')
            st.download_button("Download Data User", csv_users, "data_users.csv", "text/csv")
            
            # 2. Export Produk
            csv_produk = convert_to_csv(st.session_state.produk_list, ['Nama Produk', 'Harga', 'Stok'], 'produk')
            st.download_button("Download Data Produk", csv_produk, "data_produk.csv", "text/csv")

        with col2:
            # 3. Export Penjualan
            if st.session_state.riwayat_transaksi:
                csv_sales = convert_dict_list_to_csv(st.session_state.riwayat_transaksi, ['pembeli', 'barang', 'qty', 'total', 'status'])
                st.download_button("Download Data Penjualan", csv_sales, "data_penjualan.csv", "text/csv")
            else:
                st.button("Data Penjualan Kosong", disabled=True)

            # 4. Export Laporan 
            if st.session_state.inbox_laporan:
                csv_laporan = convert_dict_list_to_csv(st.session_state.inbox_laporan, ['pengirim', 'pesan', 'jawaban'])
                st.download_button("Download Data Laporan", csv_laporan, "data_laporan.csv", "text/csv")
            else:
                st.button("Data Laporan Kosong", disabled=True)

        st.divider()
        
        st.subheader("📤 Import Data (Upload)")
        uploaded_file = st.file_uploader("Upload File CSV")
        
        if uploaded_file is not None:
            # Pilihan ditambah Laporan
            tipe_import = st.selectbox("Ini file apa?", ["User", "Produk", "Penjualan", "Laporan"])
            
            if st.button("Proses Import"):
                try:
                    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                    
                    # --- IMPORT USER ---
                    if tipe_import == "User":
                        reader = csv.reader(stringio)
                        next(reader) # skip header
                        st.session_state.users_db.clear()
                        for row in reader:
                            st.session_state.users_db[row[0]] = User(row[0], row[1], row[2])
                        st.success("Import User Sukses!")

                    # --- IMPORT PRODUK ---
                    elif tipe_import == "Produk":
                        reader = csv.reader(stringio)
                        next(reader)
                        st.session_state.produk_list.clear()
                        for row in reader:
                            # row[0]=nama, row[1]=harga, row[2]=stok
                            st.session_state.produk_list.append(ProdukLilin(row[0], int(row[1]), int(row[2])))
                        st.success("Import Produk Sukses!")
                    
                    # --- IMPORT PENJUALAN ---
                    elif tipe_import == "Penjualan":
                        reader = csv.DictReader(stringio)
                        st.session_state.riwayat_transaksi.clear()
                        for row in reader:
                            row['qty'] = int(row['qty'])
                            row['total'] = int(row['total'])
                            st.session_state.riwayat_transaksi.append(row)
                        st.success("Import Penjualan Sukses!")

                    # --- IMPORT LAPORAN  ---
                    elif tipe_import == "Laporan":
                        reader = csv.DictReader(stringio)
                        st.session_state.inbox_laporan.clear()
                        for row in reader:
                            st.session_state.inbox_laporan.append(row)
                        st.success("Import Laporan Sukses!")

                except Exception as e:
                    st.error(f"Gagal Import: {e}")

    elif menu == "Logout":
        st.session_state['keranjang'] = []
        st.session_state['user_role'] = None; st.session_state['user_login'] = ""; st.rerun()
        
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
                st.markdown(f"<div style='color: #000; font-weight: bold;'>{p.get_nama()}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #333;'>Rp {p.get_harga()} | Stok: {p.get_stok()}</div>", unsafe_allow_html=True)
                
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

    # --- KERANJANG ---
    elif menu == "Keranjang":
        st.markdown("<h1 style='color: #000000;'>Your Cart</h1>", unsafe_allow_html=True)
        cart = st.session_state['keranjang']
        
        if not cart:
            st.info("Keranjang Kosong.")
            
            # CEK PESAN SUKSES
            if 'checkout_berhasil' in st.session_state and st.session_state['checkout_berhasil']:
                st.balloons()
                st.success("Pembayaran Berhasil! Terima kasih.")
                st.session_state['checkout_berhasil'] = False 
        else:
            col_kiri, col_kanan = st.columns([2, 1], gap="large")
            
            with col_kiri:
                st.markdown("<h3 style='color: #000000;'>Product List</h3>", unsafe_allow_html=True)
                for i, item in enumerate(cart):
                    c1, c2, c3, c4 = st.columns([1.5, 3, 2, 1])
                    with c1: st.image(item['obj_produk'].img_url, width=80)
                    with c2: 
                        st.markdown(f"<div style='color: #000;'><b>{item['nama']}</b></div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='color: #555;'>Qty: {item['qty']}</div>", unsafe_allow_html=True)
                    with c3: 
                        st.markdown(f"<div style='color: #000;'><b>Rp {item['harga']*item['qty']:,}</b></div>", unsafe_allow_html=True)
                    with c4:
                        if st.button("X", key=f"d_{i}"): cart.pop(i); st.rerun()
                    st.markdown("---")

            with col_kanan:
                subtotal = sum(item['harga'] * item['qty'] for item in cart)
                total_qty = sum(item['qty'] for item in cart)
                diskon = 0.1 if total_qty >= 3 else 0
                potongan = subtotal * diskon
                
                st.markdown("""<div style="background:#F3F3F3; padding:20px; border-radius:10px;"><h4 style="color:#000; margin-top:0;">Cart Totals</h4><hr></div>""", unsafe_allow_html=True)
                st.markdown(f"<div style='color:#000;'>Subtotal: Rp {subtotal:,}</div>", unsafe_allow_html=True)
                if diskon > 0: st.success(f"Diskon 10%: -Rp {int(potongan):,}")
                st.markdown(f"<div style='color:#000; font-weight:bold; font-size:1.2em; margin-top:10px;'>Total: Rp {int(subtotal-potongan):,}</div>", unsafe_allow_html=True)
                
                if st.button("Checkout Sekarang"):
                    for item in cart:
                        item['obj_produk'].kurangi_stok(item['qty'])
                        st.session_state['riwayat_transaksi'].append({
                            "pembeli": user, 
                            "barang": item['nama'],
                            "qty": item['qty'], 
                            "total": int(item['harga']*item['qty']),
                            "status": "Diproses"
                        })
                    
                    st.session_state['keranjang'] = []
                    st.session_state['checkout_berhasil'] = True
                    st.rerun()

    # --- PESANAN SAYA ---
    elif menu == "Pesanan Saya":
        st.markdown("<h1 style='color: #000000;'>Riwayat Pesanan</h1>", unsafe_allow_html=True)
        found = False
        for t in st.session_state['riwayat_transaksi']:
            if t['pembeli'] == user:
                st.info(f"{t['barang']} (x{t['qty']}) | Total: Rp {t['total']:,} | Status: [{t['status']}]")
                found = True
        
        if not found:
            st.info("Belum ada riwayat pesanan.")

    # --- PUSAT BANTUAN ---
    elif menu == "Pusat Bantuan":
        st.markdown("<h1 style='color: #000000;'>Pusat Bantuan</h1>", unsafe_allow_html=True)
        
        tab_tulis, tab_riwayat = st.tabs(["Tulis Laporan", "Lihat Balasan"])
        
        with tab_tulis:
            st.write("Sampaikan keluhan atau pertanyaan Anda kepada admin.")
            with st.form("form_laporan"):
                pesan_user = st.text_area("Tulis pesan Anda di sini:", height=150)
                btn_kirim = st.form_submit_button("Kirim Laporan")
                
                if btn_kirim:
                    if pesan_user.strip() == "":
                        st.warning("Pesan tidak boleh kosong.")
                    else:
                        st.session_state['inbox_laporan'].append({
                            "pengirim": user,
                            "pesan": pesan_user,
                            "jawaban": "Belum dibalas"
                        })
                        st.success("Laporan berhasil dikirim ke Admin!")

        with tab_riwayat:
            st.write("")
            found = False
            for chat in st.session_state['inbox_laporan']:
                if chat['pengirim'] == user:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px;">
                            <strong style="color: #333;">Q (Anda):</strong><br>
                            <span style="color: #555;">{chat['pesan']}</span>
                            <hr style="margin: 8px 0;">
                            <strong style="color: #333;">A (Admin):</strong><br>
                            <span style="color: {'red' if chat['jawaban']=='Belum dibalas' else 'green'}; font-weight: bold;">
                                {chat['jawaban']}
                            </span>
                        </div>""", unsafe_allow_html=True)
                    found = True
            if not found: st.info("Belum ada riwayat laporan.")

    elif menu == "Logout":
        st.session_state['keranjang'] = []
        st.session_state['user_role'] = None; st.session_state['user_login'] = ""; st.rerun()

# ============================
# 7. MAIN PROGRAM
# ============================
def main():
    if not st.session_state['user_role']:
        halaman_depan_split()
    elif st.session_state['user_role'] == "admin":
        menu_admin()
    else:
        menu_pembeli(st.session_state['user_login'])

if __name__ == "__main__":
    main()















