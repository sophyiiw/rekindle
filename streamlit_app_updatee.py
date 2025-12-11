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
  user_login = st.session_state.current_user
    st.sidebar.title(f"Halo, {user_login}")
    menu = st.sidebar.radio("Menu Pembeli:", ["Belanja", "Keranjang & Bayar", "Pesanan Saya", "Pusat Bantuan"])
    
    if st.sidebar.button("Logout"):
        # Reset keranjang saat logout (opsional, tapi bagus utk UX)
        st.session_state.keranjang = [] 
        st.session_state.login_status = False
        st.rerun()
# ============================
# 6. HALAMAN PEMBELI
# ============================
# ============================
# 6. HALAMAN PEMBELI (DIPERBAIKI)
# ============================
# ============================
# 6. HALAMAN PEMBELI (FULL FIX)
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

    # --- KERANJANG (DIPERBAIKI INDENTASI & WARNA) ---
    elif menu == "Keranjang":
        st.markdown("<h1 style='color: #000000;'>Your Cart</h1>", unsafe_allow_html=True)
        
        cart = st.session_state['keranjang']
        if not cart:
            st.info("Keranjang Kosong.")
        else:
            col_kiri, col_kanan = st.columns([2, 1], gap="large")
            
            # Perbaikan Indentasi: 'with' harus menjorok ke dalam 'else'
            with col_kiri:
                st.markdown("<h3 style='color: #000000;'>Product List</h3>", unsafe_allow_html=True)
                st.markdown("---")
                for i, item in enumerate(cart):
                    c1, c2, c3, c4 = st.columns([1.5, 3, 2, 1])
                    with c1: 
                        st.image(item['obj_produk'].img_url, width=80)
                    with c2: 
                        st.markdown(f"<div style='color: #000000; font-weight: bold;'>{item['nama']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='color: #555555; font-size: 0.9em;'>Qty: {item['qty']}</div>", unsafe_allow_html=True)
                    with c3: 
                        st.markdown(f"<div style='color: #000000; font-weight: bold;'>Rp {item['harga'] * item['qty']:,}</div>", unsafe_allow_html=True)
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
                
                st.markdown(f"<div style='color: #000000;'>Subtotal: Rp {subtotal:,}</div>", unsafe_allow_html=True)
                
                if diskon_persen > 0:
                    st.success(f"Diskon {diskon_persen}%: -Rp {int(potongan):,}")
                else:
                    st.caption("Beli min 3 items dapat diskon!")
                
                st.markdown(f"<div style='color: #000000; font-weight: bold; margin-top: 10px; font-size: 1.1em;'>Total: Rp {int(total_akhir):,}</div>", unsafe_allow_html=True)
                
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

    # --- PESANAN SAYA (FIX TAMPILAN TIMELINE) ---
    elif menu == "Pesanan Saya":
        st.title("Riwayat Pesanan")
        
        # CSS Khusus Timeline (Card Style)
        st.markdown("""
        <style>
            /* Card Container */
            .order-card {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border: 1px solid #E0E0E0;
            }
            /* Header Card */
            .order-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #F0F0F0;
                padding-bottom: 12px;
                margin-bottom: 15px;
            }
            .status-pill {
                background-color: #E3F2FD;
                color: #1565C0;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
            }
            .status-pill.success {
                background-color: #E8F5E9;
                color: #2E7D32;
            }
            /* Timeline Items */
            .timeline-row {
                display: flex;
                margin-bottom: 20px;
                position: relative;
            }
            .timeline-icon {
                width: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-right: 15px;
            }
            .dot-circle {
                width: 12px;
                height: 12px;
                background-color: #E0E0E0;
                border-radius: 50%;
                z-index: 2;
            }
            .line-vertical {
                width: 2px;
                height: 100%;
                background-color: #E0E0E0;
                position: absolute;
                left: 19px; /* Posisi tengah icon (40px/2) - 1px */
                top: 12px;
                z-index: 1;
            }
            /* Menghilangkan garis di item terakhir */
            .timeline-row:last-child .line-vertical {
                display: none;
            }
            .timeline-content {
                flex: 1;
            }
            .tm-title { font-weight: bold; color: #333; font-size: 1rem; }
            .tm-desc { color: #888; font-size: 0.85rem; margin-top: 2px; }
            
            /* Active State (Hijau) */
            .active .dot-circle { background-color: #4CAF50; box-shadow: 0 0 0 3px #E8F5E9; }
            .active .line-vertical { background-color: #4CAF50; }
            .active .tm-title { color: #000; }
        </style>
        """, unsafe_allow_html=True)

        found = False
        for t in st.session_state['riwayat_transaksi']:
            if t['pembeli'] == user:
                found = True
                status_db = t['status']
                
                # Logic Progress (1, 2, atau 3)
                progress = 0
                badge_style = "status-pill"
                
                if status_db == "Diproses":
                    progress = 1
                elif status_db == "Sedang Dikirim":
                    progress = 2
                elif status_db == "Selesai":
                    progress = 3
                    badge_style = "status-pill success"

                # Fungsi Helper untuk class HTML
                def get_active(lvl, curr): return "active" if lvl <= curr else ""

                # HTML Card (Tanpa indentasi di dalam string agar tidak jadi kotak hitam)
                html_card = f"""
<div class="order-card">
    <div class="order-header">
        <div>
            <div style="font-weight:bold; font-size:1.1rem; color:#000;">{t['barang']}</div>
            <div style="font-size:0.9rem; color:#666;">Qty: {t['qty']} | Total: Rp {t['total']:,}</div>
        </div>
        <div class="{badge_style}">{status_db}</div>
    </div>
    
    <div style="padding-left: 10px;">
        <div class="timeline-row {get_active(1, progress)}">
            <div class="timeline-icon">
                <div class="dot-circle"></div>
                <div class="line-vertical"></div>
            </div>
            <div class="timeline-content">
                <div class="tm-title">Order Confirmed</div>
                <div class="tm-desc">Pesanan telah diterima sistem.</div>
            </div>
        </div>

        <div class="timeline-row {get_active(2, progress)}">
            <div class="timeline-icon">
                <div class="dot-circle"></div>
                <div class="line-vertical"></div>
            </div>
            <div class="timeline-content">
                <div class="tm-title">Shipping</div>
                <div class="tm-desc">Kurir sedang mengantar pesanan ke lokasi.</div>
            </div>
        </div>

        <div class="timeline-row {get_active(3, progress)}">
            <div class="timeline-icon">
                <div class="dot-circle"></div>
            </div>
            <div class="timeline-content">
                <div class="tm-title">Sent to Customer</div>
                <div class="tm-desc">Pesanan telah sampai di tujuan.</div>
            </div>
        </div>
    </div>
    
    <div style="margin-top:15px; text-align:center;">
        <button style="background:transparent; border:1px solid #4CAF50; color:#4CAF50; padding:6px 20px; border-radius:20px; cursor:pointer; font-size:0.9rem;">
            Rate this delivery
        </button>
    </div>
</div>
"""
                st.markdown(html_card, unsafe_allow_html=True)

        if not found:
            st.info("Belum ada riwayat pesanan.")

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




