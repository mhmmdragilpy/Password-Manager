import os
import json
import getpass
import hashlib
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Nama file untuk konfigurasi dan data
CONFIG_FILE = 'config.json'
DATA_FILE = 'data.enc'

# --- FUNGSI-FUNGSI UTAMA (HELPER FUNCTIONS) ---

def derive_key(password: str, salt: bytes) -> bytes:
    """Mendapatkan kunci enkripsi dari password dan salt."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def hash_password(password: str, salt: bytes) -> str:
    """Membuat hash dari password menggunakan salt."""
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return pwd_hash.hex()

def verify_master_password():
    """Memverifikasi master password dan mengembalikan kunci enkripsi jika benar."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        salt = bytes.fromhex(config['salt'])
        stored_hash = config['master_password_hash']
        
        password = getpass.getpass("Masukkan Master Password: ")
        input_hash = hash_password(password, salt)

        if input_hash == stored_hash:
            return derive_key(password, salt)
        else:
            print("[!] Master Password salah.")
            return None
    except FileNotFoundError:
        print("[!] File konfigurasi tidak ditemukan. Silakan jalankan 'init' terlebih dahulu.")
        return None

def load_data(key: bytes) -> dict:
    """Membaca dan mendekripsi data dari file."""
    try:
        with open(DATA_FILE, 'rb') as f:
            encrypted_data = f.read()
        
        if not encrypted_data:
            return {} # File kosong, belum ada data

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except FileNotFoundError:
        return {}

def save_data(data: dict, key: bytes):
    """Mengenkripsi dan menyimpan data ke file."""
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted_data)

# --- FUNGSI-FUNGSI PERINTAH (COMMAND FUNCTIONS) ---

def initialize():
    """Menginisialisasi password manager: membuat master password dan file config."""
    print("--- Inisialisasi Password Manager ---")
    if os.path.exists(CONFIG_FILE):
        print("[!] File konfigurasi sudah ada. Inisialisasi dibatalkan.")
        return

    password = getpass.getpass("Buat Master Password baru: ")
    password_confirm = getpass.getpass("Konfirmasi Master Password: ")

    if password != password_confirm:
        print("[!] Password tidak cocok. Silakan coba lagi.")
        return

    salt = os.urandom(16)
    master_password_hash = hash_password(password, salt)
    
    config_data = {'salt': salt.hex(), 'master_password_hash': master_password_hash}
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f)

    with open(DATA_FILE, 'wb') as f:
        f.write(b'') 

    print("\n[+] Inisialisasi berhasil! Ingat Master Password Anda baik-baik.")

def add_password(key: bytes):
    """Menambahkan password baru."""
    print("\n--- Tambah Password Baru ---")
    service = input("Nama Layanan (misal: google): ")
    username = input(f"Username/Email untuk {service}: ")
    password = getpass.getpass(f"Password untuk {service}: ")

    data = load_data(key)
    data[service] = {'username': username, 'password': password}
    save_data(data, key)
    print(f"\n[+] Password untuk '{service}' berhasil disimpan.")

def get_password(key: bytes, service: str):
    """Mengambil password untuk layanan tertentu."""
    data = load_data(key)
    if service in data:
        entry = data[service]
        print(f"\n--- Detail untuk '{service}' ---")
        print(f"  Username: {entry['username']}")
        print(f"  Password: {entry['password']}")
    else:
        print(f"\n[!] Layanan '{service}' tidak ditemukan.")

def list_services(key: bytes):
    """Menampilkan semua layanan yang tersimpan."""
    data = load_data(key)
    if not data:
        print("\n[!] Belum ada password yang tersimpan.")
        return
    
    print("\n--- Daftar Layanan Tersimpan ---")
    for service in data.keys():
        print(f"- {service}")

# --- BAGIAN UTAMA (MAIN) ---
def main():
    parser = argparse.ArgumentParser(description="Password Manager Sederhana via Command-Line.")
    subparsers = parser.add_subparsers(dest='command', help='Perintah yang tersedia')

    # Perintah 'init'
    subparsers.add_parser('init', help='Inisialisasi password manager.')
    
    # Perintah 'add'
    subparsers.add_parser('add', help='Tambah password baru.')

    # Perintah 'get'
    get_parser = subparsers.add_parser('get', help='Lihat password untuk layanan tertentu.')
    get_parser.add_argument('service', help='Nama layanan yang ingin dilihat.')

    # Perintah 'list'
    subparsers.add_parser('list', help='Lihat semua layanan yang tersimpan.')

    args = parser.parse_args()

    if args.command == 'init':
        initialize()
    elif args.command in ['add', 'get', 'list']:
        key = verify_master_password()
        if key:
            if args.command == 'add':
                add_password(key)
            elif args.command == 'get':
                get_password(key, args.service)
            elif args.command == 'list':
                list_services(key)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()