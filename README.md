# Password Manager Sederhana (Offline & Terenkripsi) 🔐

A simple, command-line based password manager built with Python to demonstrate data security concepts.

---
## ⚠️ Peringatan Penting

Proyek ini dibuat **HANYA** untuk tujuan edukasi dan portofolio. **JANGAN GUNAKAN APLIKASI INI UNTUK MENYIMPAN PASSWORD ASLI ANDA.** Aplikasi ini tidak memiliki semua fitur keamanan dan audit yang dimiliki oleh password manager profesional.

---
## 📝 Deskripsi Proyek

Aplikasi ini adalah sebuah password manager offline yang berjalan di terminal. Semua data yang Anda simpan dienkripsi menggunakan kunci yang berasal dari sebuah **Master Password**. Ini memastikan bahwa hanya Anda yang bisa mengakses data password yang tersimpan.

---
## ✨ Fitur Utama

* **Master Password Aman**: Menggunakan **hashing** dengan **salt** (PBKDF2) untuk melindungi Master Password.
* **Enkripsi Data**: Semua data layanan (username, password) dienkripsi menggunakan algoritma **AES** melalui library `cryptography`.
* **Manajemen Data**:
    * `init`: Membuat Master Password dan menginisialisasi penyimpanan.
    * `add`: Menambahkan data login baru untuk sebuah layanan.
    * `get`: Mengambil dan mendekripsi data login untuk layanan tertentu.
    * `list`: Menampilkan semua layanan yang datanya sudah tersimpan.

---
## 🛡️ Konsep Keamanan yang Diterapkan

1.  **Hashing Master Password**: Master password tidak pernah disimpan sebagai teks biasa. Sebaliknya, hash-nya yang disimpan menggunakan algoritma PBKDF2, yang sangat tahan terhadap serangan *brute-force*.
2.  **Salting**: Salt acak yang unik dibuat untuk setiap pengguna, yang secara signifikan meningkatkan keamanan hash dan melindunginya dari serangan *rainbow table*.
3.  **Key Derivation**: Kunci enkripsi untuk data dibuat dari Master Password dan salt. Ini berarti kunci enkripsi tidak disimpan secara langsung di disk.
4.  **Enkripsi AES**: Data password dienkripsi menggunakan standar industri AES, memastikan kerahasiaannya saat disimpan di file.

---
## 💻 Teknologi yang Digunakan

* **Bahasa Pemrograman**: Python 3
* **Library Utama**:
    * `cryptography`: Untuk semua fungsi enkripsi, dekripsi, dan derivasi kunci.
    * `hashlib`: Untuk proses hashing Master Password.
    * `getpass`: Untuk menerima input password secara aman tanpa menampilkannya di layar.
    * `json`: Untuk menyimpan data konfigurasi.

---
## 🚀 Cara Menjalankan

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/mhmmdragilpy]
    cd Password-Manager
    ```

2.  **Instalasi Dependensi**
    ```bash
    pip install cryptography
    ```

3.  **Inisialisasi**
    Jalankan perintah ini untuk pertama kali untuk membuat Master Password Anda.
    ```bash
    python manager.py init
    ```

4.  **Penggunaan (Contoh)**
    *(Fitur ini akan ditambahkan pada langkah selanjutnya)*
    ```bash
    # Menambah password baru
    python manager.py add

    # Melihat password
    python manager.py get google
    ```

---
## 📬 Kontak

* **Nama Anda**: Muhammad Ragil
* **Email**: mhmmdragilpy@gmail.com
* **GitHub**: [https://github.com/mhmmdragilpy](https://github.com/mhmmdragilpy)