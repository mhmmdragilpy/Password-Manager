import os
import json
import getpass
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Nama file untuk konfigurasi dan data
CONFIG_FILE = 'config.json'
DATA_FILE = 'data.enc'

def derive_key(password: str, salt: bytes) -> bytes:
    """Mendapatkan kunci enkripsi dari password dan salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def hash_password(password: str, salt: bytes) -> str:
    """Membuat hash dari password menggunakan salt."""
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return pwd_hash.hex()

def initialize():
    """Menginisialisasi password manager: membuat master password dan file config."""
    print("--- Inisialisasi Password Manager ---")
    if os.path.exists(CONFIG_FILE):
        print("[!] File konfigurasi sudah ada. Inisialisasi dibatalkan.")
        return

    # Meminta Master Password dengan aman (input tidak akan terlihat)
    password = getpass.getpass("Buat Master Password baru: ")
    password_confirm = getpass.getpass("Konfirmasi Master Password: ")

    if password != password_confirm:
        print("[!] Password tidak cocok. Silakan coba lagi.")
        return

    # Membuat salt acak untuk keamanan
    salt = os.urandom(16)
    
    # Membuat hash dari master password
    master_password_hash = hash_password(password, salt)
    
    # Menyimpan konfigurasi
    config_data = {
        'salt': salt.hex(),
        'master_password_hash': master_password_hash
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f)

    # Membuat file data kosong yang akan dienkripsi
    with open(DATA_FILE, 'wb') as f:
        f.write(b'') # File kosong awal

    print("\n[+] Inisialisasi berhasil!")
    print(f"[*] File konfigurasi '{CONFIG_FILE}' dan file data '{DATA_FILE}' telah dibuat.")
    print("[!] Ingat Master Password Anda baik-baik. Jika lupa, data tidak bisa dipulihkan.")

def main():
    # Untuk sementara, kita hanya akan memanggil fungsi init
    # Di langkah selanjutnya kita akan menambahkan parser argumen
    initialize()

if __name__ == '__main__':
    main()