# rekindle
Rekindle adalah aplikasi e-commerce berbasis web untuk penjualan lilin aromaterapi. Aplikasi ini merupakan transformasi modern dari program berbasis terminal (CLI) menjadi Web App interaktif menggunakan Python Streamlit.Proyek ini menerapkan konsep OOP (Object-Oriented Programming), manajemen Session State, dan desain UI modern (Glassmorphism).

**Fitur Utama**
-  Menu Pembeli untuk Role "Pembeli" : Katalog produk visual, keranjang belanja, diskon otomatis (beli >3 diskon 10%, >5 diskon 20%), dan pelacakan status pesanan.
-  Sisi Admin untuk Role "Admin": Manajemen stok (CRUD), tambah produk dengan gambar, kelola user, update status pengiriman, serta Export/Import Data (CSV).

*Running Program*
- Download file Rekindle.py lalu run di terminal untuk menjalankan program versi terminal (dibuat untuk lebih memahami logika program secara simple)
- Buka link https://rekindle-ilfq77m8t39mqyxnjtvp2z.streamlit.app/ untuk menjalankan program pada file streamlit_rekindle app.py (VERSI DRAFT dari streamlit)
- Buka link https://rekindle-2jeregajxaqbnfzpuvbaz8.streamlit.app/ untuk menjalankan program pada file streamlit_app_updatee.py (VERSI FINAL dari streamlit)

*Notes*
- Username tidak bisa sama dengan username yang sudah ada
- User yang baru terdaftar akan otomatis role nya ter assign sebagai "Pembeli" dan hanya bisa diubah pada menu admin (Kelola User)
- Jika ingin membuka program sebagai admin masukkan "admin" pada bagian username dan "123" pada bagian password
- Data pada program akan hilang jika program di close, maka dari itu PENTING untuk export file sebagai admin untuk menyimpan data
- Jika ingin memasukkan data yang sudah ada, bisa menggunakan fitur import file pada menu admin
- Pembeli akan otomatis dapat diskon sebesar 10% jika membeli total produk (meskipun beda jenis) sebanyak >= 3 buah dan 20% jika membeli >= 5 buah

*User yang sudah terdaftar pada program secara default*
Masukkan username dan password dibawah jika ingin membuka menu admin/pembeli (sesuai dengan role):
username = admin
password = 123
role = admin

username = naya
password = abc
role = pembeli

username = shifa
password = abc
role = pembeli
