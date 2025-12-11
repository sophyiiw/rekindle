import streamlit as st
import csv
import os

# ============================
# 1. KONFIGURASI HALAMAN (WAJIB PALING ATAS)
# ============================
st.set_page_config(
    page_title="Rekindle Candle Shop",
    page_icon="🕯️",
    layout="wide", # Layout wide agar bisa Split Screen penuh
    initial_sidebar_state="collapsed" # Sidebar disembunyikan di halaman login agar mirip referensi
)

# ============================
# 2. CSS STYLING (ESTETIKA & VISUAL)
# ============================
# Kita suntikkan CSS untuk meniru gaya visual referensi:
# - Background Cream
# - Tombol Hitam Bulat
# - Input Field Bersih
# - Efek Glassmorphism (Kaca Blur)
st.markdown("""
<style>
    /* IMPORT FONT KEREN (Opsional, pakai default juga oke tapi ini lebih mirip) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* BACKGROUND UTAMA CREAM KALEM */
    .stApp {
        background-color: #FAF9F6; /* Warna Cream mirip referensi */
    }

    /* INPUT FIELD STYLING (Kotak isian username/password) */
    .stTextInput > div > div {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px; /* Sudut membulat */
        padding: 5px;
        box-shadow: none;
    }
    .stTextInput > div > div:focus-within {
        border-color: #333333; /* Warna border saat diklik */
    }

    /* TOMBOL STYLING (Hitam Elegan) */
    .stButton > button {
        background-color: #000000 !important; /* Hitam pekat */
        color: #FFFFFF !important;
        border-radius: 30px; /* Sangat bulat seperti pil */
        padding: 0.6rem 2rem;
        font-weight: 600;
        width: 100%;
        border: none;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02); /* Efek zoom sedikit saat hover */
        background-color: #333333 !important;
    }

    /* HEADER TEXT STYLING */
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 2rem;
        font-weight: 300;
    }

    /* CONTAINER GAMBAR KANAN (CSS Khusus untuk layout gambar penuh) */
    .right-image-container {
        position: relative;
        width: 100%;
        height: 90vh; /* Tinggi hampir layar penuh */
        border-radius: 20px;
        overflow: hidden;
        background-image: url('https://images.unsplash.com/photo-1495333241851-4c601735955a?q=80&w=1974&auto=format&fit=crop'); /* Gambar Tanaman/Estetik */
        background-size: cover;
        background-position: center;
    }

    /* EFEK KACA (GLASSMORPHISM) DI ATAS GAMBAR */
    .glass-card {
        position: absolute;
        top: 50%;
        right: -50px; /* Geser sedikit agar artistik */
        transform: translateY(-50%);
        width: 80%;
        background: rgba(255, 255, 255, 0.15); /* Putih transparan */
        backdrop-filter: blur(15px); /* Efek Blur Kuat */
        -webkit-backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    .glass-text-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .glass-text-body {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #F0F0F0;
    }

    /* Menghilangkan padding default Streamlit yang berlebihan */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Gambar untuk produk (Placeholder)
IMG_LAVENDER = "https://images.unsplash.com/photo-1602523961358-f9f03dd557db?w=400&q=80"
IMG_VANILLA = "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=400&q=80"
IMG_SANDALWOOD = "https://images.unsplash.com/photo-1596433809252-260c2745dfdd?w=400&q=80"

# ============================
# 3. CLASS & DATABASE (LOGIKA TIDAK DIUBAH)
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
    def info(self):
        st.write(f"**{self._nama}** - Stok: {self._stok}")

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
# 4. HALAMAN DEPAN MODEL BARU (SPLIT SCREEN)
# ============================
def halaman_depan_split():
    # Membuat 2 kolom: Kiri (Form) dan Kanan (Gambar)
    # Rasio [1, 1.2] agar gambar kanan sedikit lebih lebar
    col_kiri, col_kanan = st.columns([1, 1.2], gap="large")

    # --- KOLOM KIRI: FORMULIR ---
    with col_kiri:
        # Spacer agar konten turun sedikit ke tengah vertikal
        st.write("") 
        st.write("") 
        st.write("") 
        
        # Judul Besar (Menggantikan "Selamat Datang" standar)
        st.markdown('<div class="hero-title">Selamat Datang</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Nyalakan Kembali Momen Berhargamu.</div>', unsafe_allow_html=True)
        
        # Pilihan Login / Daftar menggunakan Tabs (Lebih bersih dari sidebar)
        tab_login, tab_daftar = st.tabs(["Login Akun", "Daftar Baru"])
        
        with tab_login:
            st.markdown("### Login Area")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Masukkan username...")
                password = st.text_input("Password", type="password", placeholder="Masukkan password...")
                st.write("") # Jarak
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
            st.markdown("### Daftar Akun Baru")
            with st.form("reg_form"):
                username_baru = st.text_input("Username baru", placeholder="Buat username unik...")
                password_baru = st.text_input("Password baru", type="password")
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
        
        # Kontak info kecil di bawah (mirip referensi)
        st.write("")
        st.write("")
        st.caption("Butuh bantuan? Hubungi support@rekindle.com")

    # --- KOLOM KANAN: GAMBAR & OVERLAY GLASSMORPHISM ---
    with col_kanan:
        # Menggunakan HTML Murni agar bisa positioning overlay di atas gambar
        st.markdown("""
        <div class="right-image-container">
            <div class="glass-card">
                <div class="glass-text-title">
                    Kualitas Emas untuk Suasana Ruang Anda
                </div>
                <div class="glass-text-body">
                    Koleksi lilin aromaterapi kami dirancang untuk menciptakan ketenangan dan estetika terbaik. Temukan wangi favoritmu sekarang.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================
# 5. HALAMAN UTAMA SETELAH LOGIN (Admin & Pembeli)
# ============================
# (Bagian ini tidak saya ubah logikanya, hanya strukturnya agar tetap jalan)

def menu_admin():
    st.sidebar.title("Admin Menu")
    menu = st.sidebar.selectbox("Pilih:", ["Stok Gudang", "Tambah Produk", "Logout"])
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
    elif menu == "Logout":
        st.session_state['user_role'] = None; st.rerun()

# ============================
# 6. MAIN EXECUTION
# ============================
def main():
    role = st.session_state['user_role']
    
    if role is None:
        # Panggil halaman depan baru yang Aesthetic
        halaman_depan_split()
    elif role == "admin":
        menu_admin()
    elif role == "pembeli":
        menu_pembeli(st.session_state['user_login'])

if __name__ == "__main__":
    main()
