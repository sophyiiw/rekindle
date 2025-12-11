import streamlit as st
import csv
import os

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
# 2. CSS STYLING (PERBAIKAN WARNA TEKS)
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

    /* =========================================
       PERBAIKAN TOTAL KOLOM INPUT (USERNAME & PASSWORD)
       ========================================= */
    
    /* 1. Reset Jarak */
    [data-testid="stTextInput"] {
        margin-bottom: 15px; 
    }
    
    /* 2. KOTAK PEMBUNGKUS UTAMA (WRAPPER) */
    /* Ini yang menentukan bentuk bulat dan garis pinggir */
    [data-testid="stTextInput"] > div > div {
        background-color: #FFFFFF !important; /* Wajib Putih */
        border: 1px solid #333333 !important; /* Garis pinggir hitam/abu tua tegas */
        border-radius: 15px !important;       /* Sudut membulat */
        color: #333333 !important;
        box-shadow: none !important;          /* Hapus bayangan aneh */
        align-items: center;                  /* Pastikan teks & ikon sejajar */
    }

    /* 3. EFEK SAAT DIKLIK (FOCUS) */
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: #000000 !important;     /* Garis jadi hitam pekat saat diklik */
        border-width: 2px !important;         /* Sedikit lebih tebal biar jelas aktif */
    }

    /* 4. BAGIAN INPUT TEKS (DALAM KOTAK) */
    [data-testid="stTextInput"] input {
        background-color: transparent !important; /* Transparan agar ikut warna wrapper */
        color: #333333 !important;                /* Warna tulisan hitam */
        border: none !important;                  /* Hapus border bawaan input */
    }

    /* 5. BAGIAN TOMBOL MATA (PASSWORD) - INI KUNCI PERBAIKANNYA */
    /* Membuat area tombol mata transparan agar tidak ada blok hitam */
    [data-testid="stTextInput"] button {
        background-color: transparent !important; 
        border: none !important;
        color: #555555 !important; /* Warna ikon mata abu-abu */
    }

    /* 6. Placeholder ("Masukkan username...") */
    [data-testid="stTextInput"] input::placeholder {
        color: #888888 !important;
        opacity: 1;
    }

    /* Sembunyikan Label default Streamlit */
    [data-testid="stTextInput"] label {
        display: none;
    }

    /* =========================================
       ELEMEN LAIN (TABS, TOMBOL, TEXT)
       ========================================= */
    /* Tabs */
    button[data-baseweb="tab"] > div { color: #888888 !important; }
    button[data-baseweb="tab"][aria-selected="true"] > div { color: #000000 !important; font-weight: bold; }
    button[data-baseweb="tab"][aria-selected="true"] { border-bottom-color: #000000 !important; }

    /* Tombol Utama */
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

    /* Container Gambar Kanan & Glass Card */
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
    .glass-text-title {
        font-size: 1.8rem; font-weight: 700; color: #1A1A1A; margin-bottom: 10px;
    }
    .glass-text-body {
        font-size: 1rem; color: #333333;
    }
    
    .hero-title { font-size: 3rem; font-weight: 700; color: #1A1A1A; }
    .hero-subtitle { font-size: 1.1rem; color: #555555; margin-bottom: 2rem; }
    
    .block-container { padding-top: 2rem; max-width: 100%; }
    /* ... (kode css sebelumnya) ... */

    /* --- PERBAIKAN 4: UBAH BENTUK GAMBAR KATALOG JADI ARCH (KUBAH) --- */
    /* Target khusus gambar di dalam kolom katalog */
    div[data-testid="stImage"] img {
        border-radius: 100px 100px 0 0 !important; /* Membuat lengkungan kubah di atas */
        aspect-ratio: 3 / 4 !important;            /* Memaksa gambar jadi agak tinggi (portrait) */
        object-fit: cover !important;              /* Memastikan gambar penuh & tidak gepeng */
        width: 100% !important;
        margin-bottom: 10px;
    }
</style>
</style>
""", unsafe_allow_html=True)

# Placeholder Gambar Produk
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
    def __init__(self, nama, harga, stok, img_url):
        self._nama = nama
        self._harga = harga
        self._stok = stok
        self.img_url = img_url 
    def get_nama(self): return self._nama
    def get_harga(self): return self._harga
    def get_stok(self): return self._stok
    def set_nama(self, nama_baru): self._nama = nama_baru
    def set_harga(self, harga_baru): self._harga = harga_baru
    def set_stok(self, stok_baru): self._stok = stok_baru
    def kurangi_stok(self, jumlah): self._stok = self._stok - jumlah
    def info(self): st.write(f"**{self._nama}** - Stok: {self._stok}")

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
# 4. HALAMAN DEPAN (VISUAL DIPERBAIKI)
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
# 5. HALAMAN UTAMA (SESUDAH LOGIN)
# ============================
def menu_admin():
    st.sidebar.title("Admin Menu")
    menu = st.sidebar.selectbox("Pilih:", ["Stok Gudang", "Logout"])
    if menu == "Stok Gudang":
        st.title("Stok Gudang")
        for p in st.session_state['produk_list']: p.info()
    elif menu == "Logout":
        st.session_state['user_role'] = None; st.rerun()

def menu_pembeli(user):
    st.sidebar.title(f"Halo, {user}")
    menu = st.sidebar.selectbox("Menu:", ["Katalog", "Keranjang", "Logout"])
    if menu == "Katalog":
        st.title("Katalog Produk")
        cols = st.columns(3)
        for i, p in enumerate(st.session_state['produk_list']):
            with cols[i%3]:
                st.image(p.img_url)
                st.write(f"**{p.get_nama()}**")
                st.write(f"Rp {p.get_harga()}")
                if st.button("Beli", key=f"b_{i}"):
                    st.session_state['keranjang'].append({"nama": p.get_nama(), "harga": p.get_harga()})
                    st.toast("Masuk Keranjang!")
    elif menu == "Keranjang":
        st.title("Keranjang")
        st.write(st.session_state['keranjang'])
    elif menu == "Logout":
        st.session_state['user_role'] = None; st.rerun()

# ============================
# 6. MAIN PROGRAM
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
