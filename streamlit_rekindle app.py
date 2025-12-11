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
        # Menggunakan tanda underscore (_) artinya data ini dilindungi
        self._nama = nama
        self._harga = harga
        self._stok = stok

    # --- GETTER (Untuk Mengambil Data) ---
    def get_nama(self):
        return self._nama
    
    def get_harga(self):
        return self._harga

    def get_stok(self):
        return self._stok

    # --- SETTER (Untuk Mengubah Data) ---
    def set_nama(self, nama_baru):
        self._nama = nama_baru

    def set_harga(self, harga_baru):
        self._harga = harga_baru

    def set_stok(self, stok_baru):
        self._stok = stok_baru

    # --- METHOD KHUSUS (LOGIKA BISNIS) ---
    def kurangi_stok(self, jumlah):
        self._stok = self._stok - jumlah

    def info(self):
        # [cite_start]Logika Peringatan jika stok menipis [cite: 13]
        pesan_stok = str(self._stok)
        if self._stok < 5:
            pesan_stok = str(self._stok) + " (!!! STOK MENIPIS !!!)"
            
        # Tampilan sederhana baris per baris
        print("   Nama  : " + self._nama)
        print("   Harga : Rp " + str(self._harga))
        print("   Stok  : " + pesan_stok)
        print("   ------------------------")

# ============================
# DATABASE (DICTIONARY & LIST)
# ============================

# Database User (DICTIONARY)
users_db = {
    "admin": User("admin", "123", "admin"),
    "naya":  User("naya", "abc", "pembeli"),
    "shifa":   User("shifa", "abc", "pembeli")
}

# Database Produk (LIST)
produk_list = [
    ProdukLilin("Lilin Lavender", 50000, 10),
    ProdukLilin("Lilin Vanila", 45000, 3), 
    ProdukLilin("Lilin Sandalwood", 60000, 5)
]

# Database Transaksi (LIST)
riwayat_transaksi = []

# Database Keranjang (LIST)
keranjang = [] 

# Database Laporan Masalah / Chat (LIST)
inbox_laporan = []

# ============================
# FUNGSI EXPORT DATA (CSV)
# ============================
def export_data():
    while True:
        print("\n--- MENU EXPORT DATA (CSV) ---")
        print("1. Export Data User")
        print("2. Export Data Produk")
        print("3. Export Riwayat Penjualan")
        print("4. Export Laporan Masalah")
        print("0. Kembali")
        
        pilih = input("Pilih menu export: ")

        # --- 1. EXPORT USER ---
        if pilih == "1":
            filename = "data_users.csv"
            header = ['Username', 'Password', 'Role']
            
            # Siapkan data baris per baris
            data_rows = []
            for username in users_db:
                data_user = users_db[username] 
                data_rows.append([data_user.username, data_user.password, data_user.role])
            
            # Simpan ke file
            with open(filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)     # Tulis Judul
                writer.writerows(data_rows) # Tulis Isi
            print(">> Sukses export data user!")
            
        # --- 2. EXPORT PRODUK ---
        elif pilih == "2":
            filename = "data_produk.csv"
            header = ['Nama Produk', 'Harga', 'Stok']
        
            # Siapkan data baris per baris
            data_rows = []
            # Ambil data pakai Getter
            for produk in produk_list:
                data_rows.append([produk.get_nama(), produk.get_harga(), produk.get_stok()])
        
            # Simpan ke file
            with open(filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(data_rows)
            print(">> Sukses export data produk!")

        # --- 3. EXPORT PENJUALAN ---
        elif pilih == "3":
            if len(riwayat_transaksi) == 0:
                print("Data penjualan masih kosong.")
            else:
                filename = "data_penjualan.csv"
                header = ['pembeli', 'barang', 'qty', 'total', 'status']
            
                with open(filename, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=header)
                    writer.writeheader()
                    writer.writerows(riwayat_transaksi)
                print(">> Sukses export data penjualan!")

        # --- 4. EXPORT LAPORAN ---
        elif pilih == "4":
            if len(inbox_laporan) == 0:
                print("Data laporan masih kosong.")
            else:
                filename = "data_laporan.csv"
                header = ['pengirim', 'pesan', 'jawaban']
            
                with open(filename, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=header)
                    writer.writeheader()
                    writer.writerows(inbox_laporan)
                print(">> Sukses export data laporan!")
    
        elif pilih == "0":
            print("Batal export.")
            break

# ============================
# FUNGSI IMPORT (LOAD) 
# ============================
def import_data():
    print("\n--- IMPORT DATA (LOAD SAVE FILE) ---")
    print("Peringatan: Data lama akan ditimpa.")
    yakin = input("Yakin load data? (y/n): ")
    if yakin != 'y': return

    # 1. IMPORT USER (ARRAY STYLE)
    if os.path.exists("data_users.csv"):
        with open("data_users.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader) # Skip Header
            rows = []
            for row in csvreader:
                rows.append(row)
        # Masukkan ke Database
        users_db.clear()
        for row in rows:
            # row[0]=username, row[1]=password, row[2]=role
            users_db[row[0]] = User(row[0], row[1], row[2])
        print(">> Sukses load User.")
    else:
        print(">> File data_users.csv tidak ada.")

    # 2. IMPORT PRODUK (ARRAY STYLE)
    if os.path.exists("data_produk.csv"):
        with open("data_produk.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            rows = []
            for row in csvreader:
                rows.append(row)
        # Masukkan ke Database
        produk_list.clear()
        for row in rows:
            nama = row[0]
            harga = int(row[1]) # Ubah text ke angka
            stok = int(row[2])
            produk_list.append(ProdukLilin(nama, harga, stok))
        print(">> Sukses load Produk.")
    else:
        print(">> File data_produk.csv tidak ada.")

    # 3. IMPORT PENJUALAN (DICT STYLE)
    if os.path.exists("data_penjualan.csv"):
        with open("data_penjualan.csv", "r") as csvfile:
            csvreader = csv.DictReader(csvfile)
            rows = []
            for row in csvreader:
                rows.append(row)
        # Masukkan ke Database
        riwayat_transaksi.clear()
        for row in rows:
            # Perbaiki tipe data angka
            row['qty'] = int(row['qty'])
            row['total'] = int(row['total'])
            riwayat_transaksi.append(row)
        print(">> Sukses load Penjualan.")
    else:
        print(">> File data_penjualan.csv tidak ada.")

    # 4. IMPORT LAPORAN (DICT STYLE)
    if os.path.exists("data_laporan.csv"):
        with open("data_laporan.csv", "r") as csvfile:
            csvreader = csv.DictReader(csvfile)
            rows = []
            for row in csvreader:
                rows.append(row)
        # Masukkan ke Database
        inbox_laporan.clear()
        for row in rows:
            inbox_laporan.append(row)
        print(">> Sukses load Laporan.")
    else:
        print(">> File data_laporan.csv tidak ada.")

# ============================
# FUNGSI BANTUAN
# ============================
def cari_produk(nama_dicari):
    for produk in produk_list:
        if produk.get_nama().lower() == nama_dicari.lower():
            return produk 

# ============================
# LOGIN
# ============================
def login():
    print("\n=== LOGIN REKINDLE ===")
    username = input("Username: ")
    password = input("Password: ")

    # 1. AMBIL DATA USER DARI DICTIONARY
    # users_db.get(username) akan mencari kunci. 
    # Kalau tidak ada, dia mengembalikan None (Kosong).
    user = users_db.get(username)   

    # 2. CEK APAKAH USERNAME DITEMUKAN?
    if user is None:
        print("Gagal: Username tidak ditemukan!")
        return None, None # Balikkan None dua kali (Role & Username kosong)

    # 3. CEK APAKAH PASSWORD COCOK?
    # Karena 'user' adalah Object Class, kita akses password pakai .password
    if user.password != password:
        print("Gagal: Password salah!")
        return None, None

    # 4. KALAU LOLOS SEMUA PENGECEKAN
    print(f"Login berhasil! Halo, {user.username}")
    return user.role, user.username

# ============================
# REGISTERASI
# ============================
def register():
    print("\n=== DAFTAR AKUN BARU ===")
    username = input("Username baru: ")

    # 1. CEK DULU APAKAH SUDAH ADA?
    # Kita coba ambil datanya.
    cek_user = users_db.get(username)

    # 2. KALAU TERNYATA ADA ISINYA (Bukan None), BERARTI SUDAH TERPAKAI
    if cek_user is not None:
        print(">> Gagal: Username sudah terpakai!")
        return 
    # 3. KALAU KOSONG (None), LANJUT BUAT AKUN
    password = input("Password baru: ")
    
    # Buat Object User baru, lalu simpan ke dictionary 'users'
    users_db[username] = User(username, password, "pembeli")
    print("Sukses: Akun berhasil dibuat! Silakan Login.")


# ============================
# 7. MENU ADMIN
# ============================
def menu_admin():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Cek Stok Gudang")
        print("2. Tambah Produk")
        print("3. Edit Produk")
        print("4. Kelola Role User")
        print("5. Lihat Penjualan")
        print("6. Update Status Pengiriman")
        print("7. Cek Laporan Masalah")
        print("8. Export Data ke CSV")
        print("9. Import Data dari CSV")
        print("0. Logout")
        
        pilih = input("Pilih: ")

        if pilih == "1":
            print("\n--- GUDANG ---")
            for p in produk_list:
                p.info()

        elif pilih == "2":
            nama = input("Nama: ")
            harga_str = input("Harga: ")
            stok_str = input("Stok: ")
            if harga_str.isdigit() and stok_str.isdigit():
                produk_list.append(ProdukLilin(nama, int(harga_str), int(stok_str)))
                print("Disimpan.")
            else:
                print("Harga/Stok harus angka.")

        elif pilih == "3":
            print("\n--- EDIT DATA PRODUK ---")
            nama_dicari = input("Masukkan nama produk yang mau diedit: ")
            # Cari produknya dulu
            produk_ditemukan = cari_produk(nama_dicari)
            # Cek ketemu atau tidak
            if produk_ditemukan is not None:
                print("Produk ditemukan: " + produk_ditemukan.get_nama())
                print("Mau ubah apa?")
                print("1. Ubah Nama")
                print("2. Ubah Harga")
                print("3. Ubah Stok")
                pilihan_edit = input("Pilih nomor (1-3): ")
                # --- UBAH NAMA ---
                if pilihan_edit == "1":
                    nama_baru = input("Masukkan Nama Baru: ")
                    produk_ditemukan.set_nama(nama_baru)
                    print(">> Berhasil ubah nama!")
                # --- UBAH HARGA ---
                elif pilihan_edit == "2":
                    input_harga = input("Masukkan Harga Baru: ")
                    # Cek apakah inputnya angka
                    if input_harga.isdigit():
                        harga_angka = int(input_harga)
                        produk_ditemukan.set_harga(harga_angka)
                        print(">> Berhasil ubah harga!")
                    else:
                        print(">> Gagal: Harga harus berupa angka.")
                # --- UBAH STOK ---
                elif pilihan_edit == "3":
                    input_stok = input("Masukkan Stok Baru: ")
                    # Cek apakah inputnya angka
                    if input_stok.isdigit():
                        stok_angka = int(input_stok)
                        produk_ditemukan.set_stok(stok_angka)
                        print(">> Berhasil ubah stok!")
                    else:
                        print(">> Gagal: Stok harus berupa angka.")
                else:
                    print("Pilihan tidak valid.")
            else:
                print("Produk tidak ditemukan.")

        elif pilih == "4":
            print("\n--- DAFTAR PENGGUNA ---")
            for username in users_db:
                data_user = users_db[username]
                print(f"- Username: {data_user.username} | Password: {data_user.password} | Role: {data_user.role}")
            print("----------------------------------------")
            target_username = input("Ketik username yang mau diedit: ")
            if target_username in users_db:
                print(f"\nUser '{target_username}' ditemukan.")
                print("1. Ubah Status (Admin/Pembeli)")
                print("2. Ubah Password")
                print("3. Ubah Nama User (Rename)")
                mau_ubah = input("Pilih nomor (1-3): ")
                # --- GANTI ROLE ---
                if mau_ubah == "1":
                    role_baru = input("Status baru (admin/pembeli): ")
                    users_db[target_username].role = role_baru
                    print(">> Sip! Status berhasil diubah.")
                # --- GANTI PASSWORD (BARU) ---
                elif mau_ubah == "2":
                    pass_baru = input("Password baru: ")
                    users_db[target_username].password = pass_baru
                    print(">> Sip! Password berhasil diubah.")
                # --- GANTI USERNAME (BARU) ---
                elif mau_ubah == "3":
                    nama_baru = input("Username baru: ")
                    # Cek dulu nama baru sudah dipakai orang lain belum?
                    if nama_baru in users_db:
                        print(">> Gagal: Nama itu sudah dipakai user lain!")
                    else:
                        # Logika Ganti Nama:
                        # 1. Ambil data lama
                        data_user = users_db[target_username]
                        # 2. Ganti nama di dalam datanya
                        data_user.username = nama_baru
                        # 3. Pindah ke kunci (laci) baru
                        users_db[nama_baru] = data_user
                        # 4. Hapus kunci (laci) lama
                        del users_db[target_username]
                        print(f">> Sip! Berubah jadi {nama_baru}")
            else: 
                print(">> User tidak ada.")

        elif pilih == "5":
            print("\n--- RIWAYAT PENJUALAN ---")
            total_pendapatan = 0
            cari_nama = input("Cari nama pembeli (Kosongkan utk lihat semua): ").lower()
            for transaksi in riwayat_transaksi:
                nama_pembeli = transaksi['pembeli']
                # Cek apakah nama yang dicari ada di nama pembeli?
                if cari_nama in nama_pembeli.lower():
                    barang = transaksi['barang']
                    total  = transaksi['total']
                    status = transaksi['status']
                    print(nama_pembeli + " | Beli: " + barang + " | Rp " + str(total) + " | Status: " + status)
                    # Hitung total uang
                    total_pendapatan = total_pendapatan + total
            print("----------------------------------------")
            print("TOTAL UANG MASUK: Rp " + str(total_pendapatan))
            
        elif pilih == "6":
            print("\n--- UPDATE STATUS PESANAN ---")
            nomor = 1
            for transaksi in riwayat_transaksi:
                print(str(nomor) + ". " + transaksi['pembeli'] + " - " + transaksi['barang'] + " [" + transaksi['status'] + "]")
                nomor = nomor + 1
            input_nomor = input("Pilih nomor transaksi yang mau diupdate: ")
            # Cek apakah inputnya angka?
            if input_nomor.isdigit():
                index = int(input_nomor) - 1
                # Cek apakah nomornya valid (ada di dalam list)?
                if index >= 0 and index < len(riwayat_transaksi):
                    print("Pilih Status Baru:")
                    print("1. Diproses")
                    print("2. Sedang Dikirim")
                    print("3. Selesai / Sampai")
                    pilihan_status = input("Masukkan nomor status (1-3): ")
                    # Logika if-else sederhana untuk ganti status
                    if pilihan_status == "1":
                        riwayat_transaksi[index]['status'] = "Diproses"
                        print(">> Status diubah jadi: Diproses")
                    elif pilihan_status == "2":
                        riwayat_transaksi[index]['status'] = "Sedang Dikirim"
                        print(">> Status diubah jadi: Sedang Dikirim")
                    elif pilihan_status == "3":
                        riwayat_transaksi[index]['status'] = "Selesai"
                        print(">> Status diubah jadi: Selesai")
                    else:
                        print(">> Pilihan status tidak ada.")
                else:
                    print(">> Nomor transaksi tidak ditemukan.")
            else:
                print(">> Input harus angka.")
            
        elif pilih == "7":
            print("\n--- INBOX LAPORAN USER ---")
            if len(inbox_laporan) == 0:
                print("Tidak ada pesan masuk.")
            else:
                nomor = 1
                for pesan in inbox_laporan:
                    print(str(nomor) + ". Dari: " + pesan['pengirim'])
                    print("   Keluhan: " + pesan['pesan'])
                    print("   Balasan: " + pesan['jawaban'])
                    print("----------------------------------------")
                    nomor = nomor + 1
                input_nomor = input("Nomor pesan yang mau dibalas (0 batal): ")
                if input_nomor.isdigit():
                    index = int(input_nomor) - 1
                    # Cek validitas nomor pesan
                    if index >= 0 and index < len(inbox_laporan):
                        balasan_admin = input("Tulis balasan Anda: ")
                        # Update dictionary laporan
                        inbox_laporan[index]['jawaban'] = balasan_admin
                        print(">> Balasan terkirim!")
                    elif index == -1:
                        print(">> Batal membalas.")
                    else:
                        print(">> Nomor pesan tidak valid.")
                else:
                    print(">> Input harus angka.")
        elif pilih == "8":
            export_data()
        
        elif pilih == "9":
            import_data()
            
        elif pilih == "0":
            break


# ============================
# 8. MENU PEMBELI
# ============================
def menu_pembeli(user_login):
    while True:
        print("\n--- PEMBELI (" + user_login + ") ---")
        print("1. Belanja")
        print("2. Keranjang & Bayar")
        print("3. Cek Pesanan")
        print("4. Lapor Masalah")
        print("0. Logout")

        pilih = input("Pilih: ")

        if pilih == "1":
            print("\n--- KATALOG PRODUK ---")
            for produk in produk_list:
                produk.info()
            nama_dicari = input("Masukkan Nama Produk yang mau dibeli (0 batal): ")
            # Cek apakah user mau batal?
            if nama_dicari == '0':
                continue # Kembali ke menu awal
            # Cari produknya
            produk_ditemukan = cari_produk(nama_dicari)
            if produk_ditemukan:
                input_jumlah = input("Mau beli berapa? ")
                # Cek apakah inputnya angka
                if input_jumlah.isdigit():
                    jumlah_beli = int(input_jumlah)
                    stok_tersedia = produk_ditemukan.get_stok()
                    # Cek stok cukup atau tidak
                    if jumlah_beli <= stok_tersedia:
                        # Buat data item belanja (Dictionary)
                        item_belanja = {
                            "obj_produk": produk_ditemukan,
                            "nama": produk_ditemukan.get_nama(),
                            "harga": produk_ditemukan.get_harga(),
                            "qty": jumlah_beli
                        }
                        # Masukkan ke list keranjang
                        keranjang.append(item_belanja)
                        print(">> Berhasil masuk keranjang!")
                    else:
                        print(">> Stok tidak cukup (Sisa: " + str(stok_tersedia) + ")")
                else:
                    print(">> Jumlah harus berupa angka.")
            else:
                print(">> Produk tidak ditemukan.")

        elif pilih == "2":
            # Cek dulu: Keranjangnya ada isinya gak?
            if len(keranjang) == 0:
                print(">> Keranjang belanja masih kosong.")
                continue 
            print("\n--- KASIR REKINDLE ---")
            total_bayar = 0
            # TAHAP 1: Tampilkan rincian belanjaan
            for item in keranjang:
                nama_barang = item['nama']
                jumlah_beli = item['qty']
                harga_satuan = item['harga']
                # Hitung harga per barang
                subtotal = harga_satuan * jumlah_beli
                # Tampilkan ke layar
                print("- " + nama_barang + " (x" + str(jumlah_beli) + ") = Rp " + str(subtotal))
                # Tambahkan ke total keseluruhan
                total_bayar = total_bayar + subtotal
            print("------------------------------")
            print("TOTAL HARUS DIBAYAR: Rp " + str(total_bayar))
            # TAHAP 2: Konfirmasi Pembayaran
            jawaban = input("Bayar sekarang? (ketik 'ya' atau 'tidak'): ")
            if jawaban == "ya":
                # Proses barang satu per satu
                for item in keranjang:
                    # 1. Kurangi Stok Fisik di Gudang
                    produk_asli = item['obj_produk']
                    produk_asli.kurangi_stok(item['qty'])
                    # 2. Catat ke Buku Riwayat Penjualan
                    catatan_baru = {
                        "pembeli": user_login,
                        "barang": item['nama'],
                        "qty": item['qty'],
                        "total": item['harga'] * item['qty'],
                        "status": "Diproses"
                    }
                    riwayat_transaksi.append(catatan_baru)
                print(">> Pembayaran LUNAS! Terima kasih.")
                # Kosongkan keranjang karena sudah dibayar
                # Kita pakai cara paling standar: hapus sampai habis
                keranjang.clear()
            else:
                print(">> Pembayaran dibatalkan.")

        elif pilih == "3":
            print("\n--- RIWAYAT PESANAN SAYA ---")
            ada_pesanan = False
            for transaksi in riwayat_transaksi:
                # Cek apakah ini pesanan milik user yang sedang login?
                if transaksi['pembeli'] == user_login:
                    # Ambil data dari riwayat
                    barang = transaksi['barang']
                    jumlah = transaksi['qty']
                    total_harga = transaksi['total']
                    status = transaksi['status']
                    # Tampilkan: Nama (xJunlah) | Total | Status
                    print(f"- {barang} (x{jumlah}) | Total: Rp {total_harga} | Status: [{status}]")
                    ada_pesanan = True
            if ada_pesanan == False:
                print(">> Belum ada pesanan.")

        elif pilih == "4":
            print("\n--- KIRIM LAPORAN ---")
            keluhan_user = input("Tuliskan keluhan Anda: ")
            # Buat pesan baru (Dictionary)
            pesan_baru = {
                "pengirim": user_login,
                "pesan": keluhan_user,
                "jawaban": "Belum dibalas"
            }
            inbox_laporan.append(pesan_baru)
            print(">> Laporan berhasil dikirim ke Admin.")
        elif pilih == "0":
            break


# ============================
# 9. PROGRAM UTAMA
# ============================
if __name__ == "__main__":
    while True:
        print("\n=== REKINDLE APP ===")
        print("1. Login | 2. Register | 3. Exit")
        p = input("Pilih: ")
        
        if p == "1":
            role,user = login()
            if role == "admin": 
                menu_admin()
            elif role == "pembeli": 
                menu_pembeli(user)
        elif p == "2":
            register()
        elif p == "3":
            break
