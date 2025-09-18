import requests
import subprocess
import uuid
import sys

# Konfigurasi
LICENSE_SERVER_URL = "http://127.0.0.1:5000"  # Ganti dengan URL server Anda
LICENSE_KEY = "MASUKKAN-LICENSE-KEY-DISINI"  # Ganti dengan license key user
EXE_PATH = "kpu_nik_checkerok.exe"  # Nama file exe asli

# Ambil hardware id unik (bisa diganti sesuai kebutuhan)
def get_hardware_id():
    return str(uuid.getnode())

# Cek lisensi ke server
def check_license():
    hardware_id = get_hardware_id()
    try:
        response = requests.post(LICENSE_SERVER_URL, json={
            "license_key": LICENSE_KEY,
            "hardware_id": hardware_id
        }, timeout=10)
        if response.status_code == 200 and response.json().get("valid"):
            return True
        else:
            print("Lisensi tidak valid atau sudah dinonaktifkan.")
            return False
    except Exception as e:
        print(f"Gagal menghubungi server lisensi: {e}")
        return False

def main():
    if check_license():
        # Jalankan exe asli
        try:
            subprocess.run([EXE_PATH] + sys.argv[1:])
        except Exception as e:
            print(f"Gagal menjalankan aplikasi: {e}")
    else:
        print("Akses ditolak.")

if __name__ == "__main__":
    main()
