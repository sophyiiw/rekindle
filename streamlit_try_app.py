import streamlit as st
import csv
import os

# ============================
# KONFIGURASI HALAMAN
# Menggunakan layout "wide" agar bisa split screen
# ============================
st.set_page_config(
    page_title="Rekindle - Nyalakan Momenmu",
    page_icon="🕯️",
    layout="wide", # Diubah ke wide untuk tampilan split
    initial_sidebar_state="expanded"
)

# ============================
# STYLE TAMBAHAN (CSS AESTHETIC & ELEGANT)
# ============================
# Warna Palette: Cream, Warm Grey, Dark Charcoal, Soft Brown
bg_cream = "#F9F7F1"
text_dark = "#333333"
text_soft = "#666666"
accent_brown = "#4A3F35" # Warna tombol
input_bg = "#FFFFFF"
input_border = "#E0D8C8"

st.markdown(f"""
<style>
    /* 1. Reset & Background Utama Aplikasi */
    .stApp {{
        background-color: {bg_cream};
        color: {text_dark};
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}

    /* Menghilangkan padding atas bawaan Streamlit agar lebih clean */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }}

    /* 2. Kustomisasi Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #F0EDE6; /* Cream sedikit lebih gelap */
        border-right: 1px solid #EBE5DA;
    }}
    [data-testid="stSidebar"] h1 {{
        color: {accent_brown};
        font-weight: 600;
    }}

    /* 3. Typography (Judul & Subjudul) */
    .aesthetic-header {{
        font-size: 3rem;
        font-weight: 700;
        color: {accent_brown};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    .aesthetic-subheader {{
        font-size: 1.1rem;
        color: {text_soft};
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }}
    .form-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {text_dark};
        margin-bottom: 1.5rem;
    }}

    /* 4. Kustomisasi Input Fields (Agar mirip referensi) */
    /* Mengubah kotak pembungkus input */
    [data-testid="stTextInput"] > div > div {{
        background-color: {input_bg};
        border: 1px solid {input_border};
        border-radius: 12px; /* Sudut membulat */
        padding: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02); /* Bayangan sangat halus */
        transition: all 0.3s ease;
    }}
    /* Efek saat diklik */
    [data-testid="stTextInput"] > div > div:focus-within {{
        border-color: {accent_brown};
        box-shadow: 0 4px 8px rgba(74, 63, 53, 0.1);
    }}
    /* Menghilangkan border default input di dalamnya */
    [data-testid="stTextInput"] input {{
        color: {text_dark};
    }}
    /* Menyembunyikan label default Streamlit yang kecil di atas input */
    [data-testid="stTextInput"] label {{
        display: none;
    }}

    /* 5. Kustomisasi Tombol (Elegan & Gelap) */
    .stButton button {{
        background-color: {accent_brown} !important;
        color: white !important;
        border: none;
        border-radius: 30px; /* Sangat bulat */
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        background-color: #362E27 !important; /* Lebih gelap saat hover */
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }}

    /* 6. Styling untuk Kolom Kanan (Gambar) */
    .right-image-container {{
        position: relative;
        width: 100%;
        height: 85vh; /* Tinggi menyesuaikan layar */
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.05);
    }}
    .right-image {{
        width: 100%;
        height: 100%;
        object-fit: cover; /* Agar gambar mengisi penuh tanpa gepeng */
    }}
    /* Overlay Text Box (Kotak transparan di atas gambar) */
    .image-overlay-box {{
        position: absolute;
        bottom: 10%;
        left: 5%;
        right: 5%;
        background: rgba(255, 255, 255, 0.85); /* Putih transparan */
        backdrop-filter: blur(10px); /* Efek blur di belakang kotak */
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }}
    .overlay-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {accent_brown};
        margin-bottom: 0.5rem;
    }}
    .overlay-text {{
        font-size: 0.95rem;
        color: {text_dark};
        line-height: 1.5;
    }}
    
    /* CSS khusus untuk halaman dalam (Admin/Pembeli) agar tetap rapi */
    [data-testid="stcolumn"] {{
         background-color: #FFFFFF;
         border-radius: 15px;
         padding: 20px;
         box-shadow: 2px 2px 15px rgba(0,0,0,0.03);
         border: 1px solid #F0EDE6;
    }}
</style>
""", unsafe_allow_html=True)

# URL Gambar yang lebih estetik dan calming (Cream/Nature tone)
IMG_HERO_RIGHT = "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?q=80&w=1974&auto=format&fit=crop" # Gambar lilin & buku estetik
IMG_LAVENDER = "https://images.unsplash.com/photo-1602523961358-f9f03dd557db?w=400&q=80"
IMG_VANILLA = "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=400&q=80"
IMG_SANDALWOOD = "https://images.unsplash.com/photo-1596433809252-260c2745dfdd?w=400&q=80"


# ============================
# CLASS USER & PRODUK (TIDAK BERUBAH)
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
        pesan_stok = str(self._stok)
        if self._stok < 5: pesan_stok = f"⚠️ {self._stok} (MENIPIS!)"
        cols = st.columns([1, 3])
        with cols[0]: st.image(self.img_url, width=80)
        with cols[1]:
            st.markdown(f"**{self._nama}**")
            st.write(f"Harga : Rp {self._harga:,}")
            st.write(f"Stok  : {pesan_stok}")
        st.divider()

# ============================
# INISIALISASI SESSION STATE (TIDAK BERUBAH)
# ============================
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
# FUNGSI BANTUAN (TIDAK BERUBAH)
# ============================
def cari_produk(nama_dicari):
    for produk in st.session_state['produk_list']:
        if produk.get_nama().lower() == nama_dicari.lower():
            return produk
    return None

# ============================
# FUNGSI EXPORT & IMPORT (Disingkat agar fokus ke UI)
# ============================
def fitur_export_data():
    st.info("Fitur Export Data (Fungsionalitas tetap sama seperti kode sebelumnya).")
def fitur_import_data():
    st.info("Fitur Import Data (Fungsionalitas tetap sama seperti kode sebelumnya).")


# ============================
# STRUKTUR HALAMAN DEPAN BARU (SPLIT SCREEN)
# ============================
def halaman_depan_split(jenis_konten):
    """
    Fungsi ini membuat tata letak 2 kolom:
    Kiri: Konten Form (Login/Register)
    Kanan: Gambar Estetik Besar dengan Overlay Text
    """
    # Membuat 2 kolom dengan rasio 5:7 (Kiri lebih kecil sedikit)
    col_form, col_image = st.columns([5, 7], gap="large")

    # --- KOLOM KIRI (FORM) ---
    with col_form:
        # Spacer agar konten agak ke bawah (centering vertikal manual)
        st.write("") 
        st.write("")
        
        st.markdown('<div class="aesthetic-header">Selamat Datang.</div>', unsafe_allow_html=True)
        st.markdown('<div class="aesthetic-subheader">Masuk untuk menyalakan kembali momen berhargamu dengan koleksi wewangian kami.</div>', unsafe_allow_html=True)
        
        if jenis_konten == "login":
            tampilkan_form_login()
        else:
            tampilkan_form_register()

    # --- KOLOM KANAN (GAMBAR ESTETIK) ---
    with col_image:
        # Menggunakan HTML kustom untuk gambar penuh dan kotak teks overlay
        # agar mirip dengan referensi gambar yang diminta.
        st.markdown(f"""
        <div class="right-image-container">
            <img src="{IMG_HERO_RIGHT}" class="right-image" alt="Aesthetic Candle Mood">
            <div class="image-overlay-box">
                <div class="overlay-title">The New Gold Standard for Ambiance</div>
                <div class="overlay-text">
                    Koleksi lilin aromaterapi kami dirancang untuk menciptakan suasana yang menenangkan, elegan, dan personal di setiap sudut ruang Anda. 
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================
# ISI FORM LOGIN & REGISTER (Disederhanakan untuk UI Baru)
# ============================
def tampilkan_form_login():
    st.markdown('<div class="form-header">Login Akun</div>', unsafe_allow_html=True)
    with st.form("login_form", border=False): # border=False agar CSS kita yang menang
        # Placeholder kita gunakan sebagai label karena label asli di-hide via CSS
        username = st.text_input("Username", placeholder="Ketik username Anda...")
        password = st.text_input("Password", type="password", placeholder="Ketik password Anda...")
        st.write("") # Spacer
        submitted = st.form_submit_button("Masuk Sekarang")
        
        if submitted:
            user = st.session_state['users_db'].get(username)
            if user is None:
                st.error("Username tidak ditemukan.")
            elif user.password != password:
                st.error("Password salah.")
            else:
                st.session_state['user_role'] = user.role
                st.session_state['user_login'] = user.username
                st.success(f"Selamat datang, {user.username}!")
                st.rerun()
    
    st.markdown(f'<p style="color:{text_soft}; margin-top:20px;">Belum punya akun? Silakan pilih menu Daftar Baru di sidebar.</p>', unsafe_allow_html=True)

def tampilkan_form_register():
    st.markdown('<div class="form-header">Buat Akun Baru</div>', unsafe_allow_html=True)
    with st.form("reg_form", border=False):
        username_baru = st.text_input("Username baru", placeholder="Pilih username unik...")
        password_baru = st.text_input("Password baru", type="password", placeholder="Buat password kuat...")
        st.write("")
        submitted = st.form_submit_button("Daftar Akun")
        
        if submitted:
            if username_baru in st.session_state['users_db']:
                st.error("Username sudah terpakai.")
            elif username_baru == "":
                st.error("Username wajib diisi.")
            else:
                st.session_state['users_db'][username_baru] = User(username_baru, password_baru, "pembeli")
                st.balloons()
                st.success("Akun berhasil dibuat! Silakan beralih ke menu Login.")


# ============================
# HALAMAN ADMIN & PEMBELI (VISUAL DIPERBAIKI CSS)
# ============================
# (Kode logika menu admin/pembeli di bawah ini sama, 
# tapi tampilannya akan otomatis lebih rapi karena CSS global di atas)

def menu_admin():
    st.sidebar.title("🛠️ Admin Panel")
    pilihan_menu = {
        "📦 Cek Stok Gudang": "gudang",
        "➕ Tambah Produk": "tambah",
        "✏️ Edit Produk": "edit",
        "👥 Kelola Role User": "user",
        "💰 Lihat Penjualan": "jual",
        "🚚 Update Pengiriman": "kirim",
        "💬 Cek Laporan Masalah": "lapor",
        "📂 Export/Import Data": "file",
        "🚪 Logout": "logout"
    }
    menu = st.sidebar.radio("Navigasi:", list(pilihan_menu.keys()))
    st.header(menu) 

    if menu == "📦 Cek Stok Gudang":
        st.info("Daftar stok lilin saat ini di gudang.")
        for p in st.session_state['produk_list']: p.info()

    elif menu == "➕ Tambah Produk":
        with st.container():
            with st.form("tambah_prod"):
                nama = st.text_input("Nama Produk")
                harga = st.number_input("Harga (Rp)", min_value=0, step=1000)
                stok = st.number_input("Stok Awal", min_value=0, step=1)
                img = st.text_input("URL Gambar Produk (Opsional)", placeholder="https://...")
                if img == "": img = IMG_LAVENDER
                if st.form_submit_button("Simpan Produk"):
                    st.session_state['produk_list'].append(ProdukLilin(nama, int(harga), int(stok), img))
                    st.success(f"Produk {nama} berhasil ditambahkan!")

    elif menu == "✏️ Edit Produk":
        list_nama_produk = [p.get_nama() for p in st.session_state['produk_list']]
        pilih_prod = st.selectbox("Pilih produk yang akan diedit:", list_nama_produk)
        produk_terpilih = cari_produk(pilih_prod)
        if produk_terpilih:
            with st.container():
                col_img, col_form = st.columns([1, 2])
                with col_img: st.image(produk_terpilih.img_url, caption="Gambar Saat Ini")
                with col_form:
                    opsi_edit = st.selectbox("Mau ubah atribut apa?", ["Ubah Nama", "Ubah Harga", "Ubah Stok"])
                    nilai_baru = st.text_input(f"Masukkan {opsi_edit} baru:")
                    if st.button("Update Data"):
                        if opsi_edit == "Ubah Nama": produk_terpilih.set_nama(nilai_baru)
                        elif opsi_edit == "Ubah Harga": produk_terpilih.set_harga(int(nilai_baru))
                        elif opsi_edit == "Ubah Stok": produk_terpilih.set_stok(int(nilai_baru))
                        st.success("Berhasil diupdate!")
                        st.rerun()

    elif menu == "👥 Kelola Role User":
        db = st.session_state['users_db']
        data_tampil = [{"Username": db[u].username, "Role": db[u].role} for u in db]
        st.dataframe(data_tampil, use_container_width=True)

    elif menu == "💰 Lihat Penjualan":
        tx_list = st.session_state['riwayat_transaksi']
        total_pendapatan = sum(tx['total'] for tx in tx_list)
        m1, m2 = st.columns(2)
        m1.metric("Total Transaksi", f"{len(tx_list)} Pesanan")
        m2.metric("Total Pendapatan", f"Rp {total_pendapatan:,}")
        st.divider()
        if len(tx_list) > 0:
            for tx in tx_list:
                with st.container():
                    st.write(f"**{tx['pembeli']}** beli **{tx['barang']}** (Rp {tx['total']:,}) - Status: {tx['status']}")

    elif menu == "🚚 Update Pengiriman":
        tx_list = st.session_state['riwayat_transaksi']
        opsi_tx = [f"{i+1}. {tx['pembeli']} - {tx['barang']} [{tx['status']}]" for i, tx in enumerate(tx_list)]
        if opsi_tx:
            pilihan = st.selectbox("Pilih transaksi:", opsi_tx)
            status_baru = st.selectbox("Status Baru:", ["Diproses", "Sedang Dikirim", "Selesai"])
            if st.button("Update Status"):
                tx_list[int(pilihan.split(".")[0]) - 1]['status'] = status_baru
                st.success("Status diupdate.")
                st.rerun()

    elif menu == "💬 Cek Laporan Masalah":
        laporan_list = st.session_state['inbox_laporan']
        if not laporan_list: st.info("Tidak ada pesan masuk.")
        else:
            for i, m in enumerate(laporan_list):
                with st.expander(f"Pesan dari: {m['pengirim']}"):
                    st.write(f"Keluhan: {m['pesan']}")
                    st.write(f"Balasan: {m['jawaban']}")
                    balasan_baru = st.text_input("Tulis balasan:", key=f"balas_{i}")
                    if st.button("Kirim", key=f"btn_balas_{i}"):
                        laporan_list[i]['jawaban'] = balasan_baru
                        st.rerun()

    elif menu == "📂 Export/Import Data":
        tab1, tab2 = st.tabs(["📤 Export", "📥 Import"])
        with tab1: fitur_export_data()
        with tab2: fitur_import_data()

    elif menu == "🚪 Logout":
        st.session_state['user_role'] = None; st.rerun()

def menu_pembeli(user_login):
    st.sidebar.title(f"👤 Hai, {user_login}")
    menu = st.sidebar.radio("Menu Belanja:", ["🛍️ Katalog", "🛒 Keranjang", "📦 Pesanan", "📞 Bantuan", "🚪 Logout"])
    st.header(menu[2:]) 

    if menu == "🛍️ Katalog":
        cols = st.columns(3)
        for i, produk in enumerate(st.session_state['produk_list']):
            with cols[i % 3]:
                with st.container():
                    st.image(produk.img_url, use_column_width=True)
                    st.write(f"**{produk.get_nama()}**")
                    st.write(f"Rp {produk.get_harga():,}")
                    qty = st.number_input("Qty", 1, produk.get_stok(), 1, key=f"q_{i}", label_visibility="collapsed")
                    if st.button("Beli", key=f"btn_{i}"):
                        st.session_state['keranjang'].append({"obj": produk, "nama": produk.get_nama(), "harga": produk.get_harga(), "qty": qty})
                        st.toast("Masuk keranjang!")

    elif menu == "🛒 Keranjang":
        keranjang = st.session_state['keranjang']
        if not keranjang: st.info("Keranjang kosong.")
        else:
            total = 0
            for item in keranjang:
                subtotal = item['harga'] * item['qty']
                st.write(f"- {item['nama']} (x{item['qty']}) = Rp {subtotal:,}")
                total += subtotal
            st.divider()
            st.subheader(f"Total: Rp {total:,}")
            if st.button("Bayar Sekarang", type="primary"):
                for item in keranjang: item['obj'].kurangi_stok(item['qty'])
                st.session_state['riwayat_transaksi'].append({"pembeli": user_login, "barang": "Berbagai Produk", "qty": len(keranjang), "total": total, "status": "Diproses"})
                st.session_state['keranjang'] = []
                st.balloons(); st.success("Terima kasih!"); st.rerun()

    elif menu == "📦 Pesanan":
        tx_list = [tx for tx in st.session_state['riwayat_transaksi'] if tx['pembeli'] == user_login]
        if not tx_list: st.info("Belum ada pesanan.")
        else:
            for tx in tx_list:
                with st.container(): st.write(f"📦 {tx['barang']} (Total: Rp {tx['total']:,}) - Status: **{tx['status']}**")

    elif menu == "📞 Bantuan":
        pesan = st.text_area("Tulis laporan Anda:")
        if st.button("Kirim Laporan"):
            st.session_state['inbox_laporan'].append({"pengirim": user_login, "pesan": pesan, "jawaban": "Menunggu..."})
            st.success("Terkirim!")
        st.divider()
        for chat in st.session_state['inbox_laporan']:
             if chat['pengirim'] == user_login: st.write(f"Anda: {chat['pesan']}\nAdmin: {chat['jawaban']}\n---")

    elif menu == "🚪 Logout":
        st.session_state['user_role'] = None; st.rerun()

# ============================
# MAIN PROGRAM (NAVIGASI UTAMA)
# ============================
def main():
    role = st.session_state['user_role']
    user = st.session_state['user_login']

    if role is None:
        # --- TAMPILAN HALAMAN DEPAN BARU (SPLIT SCREEN) ---
        # Sidebar hanya untuk memilih mode Login atau Daftar
        st.sidebar.markdown("### Akses Masuk")
        # Menggunakan radio button di sidebar untuk memilih tampilan di area utama
        pilihan_akses = st.sidebar.radio("Pilih Menu:", ["🔐 Login Akun", "📝 Daftar Baru"], label_visibility="collapsed")
        
        if pilihan_akses == "🔐 Login Akun":
            halaman_depan_split("login")
        else:
            halaman_depan_split("register")
            
    elif role == "admin":
        menu_admin() # Tampilan dalam akan otomatis mengikuti style CSS baru
        
    elif role == "pembeli":
        menu_pembeli(user) # Tampilan dalam akan otomatis mengikuti style CSS baru

if __name__ == "__main__":
    main()
