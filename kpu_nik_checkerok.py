import requests
import time
import random
from datetime import datetime
import os

class KPUChecker:
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        ]

    def get_random_headers(self):
        """Generate headers dengan user-agent yang dirotasi"""
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://cekdptonline.kpu.go.id",
            "referer": "https://cekdptonline.kpu.go.id/",
            "user-agent": random.choice(self.user_agents)
        }

    def read_nik_from_file(self, filename):
        """Baca NIK dari file teks"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                nik_list = [line.strip() for line in f if line.strip()]
            return nik_list
        except Exception as e:
            print(f"Error membaca file: {e}")
            return []

    def check_nik(self, nik):
        """Fungsi untuk mengecek NIK"""
        url = "https://cekdptonline.kpu.go.id/v2"
        
        try:
            headers = self.get_random_headers()
            
            payload = {
                "operationName": "findNikSidalih",
                "variables": {
                    "nik": nik,
                    "wilayah_id": 0,
                    "token": "default_token"
                },
                "query": "query findNikSidalih($nik: String!, $wilayah_id: Int!, $token: String!) { findNikSidalih(nik: $nik, wilayah_id: $wilayah_id, token: $token) { nama nik nkk } }"
            }

            response = self.session.post(
                url, 
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                
                # Cek jika data ditemukan
                if ('data' in result and result['data'] and 
                    result['data']['findNikSidalih'] and 
                    result['data']['findNikSidalih'].get('nama')):
                    return "VALID"
                else:
                    return "TIDAK_VALID"
            
            return "TIDAK_VALID"
                    
        except:
            return "GAGAL"

    def save_to_txt(self, nik_list, filename):
        """Simpan list NIK ke file TXT"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for nik in nik_list:
                    f.write(f"{nik}\n")
            print(f"✅ Disimpan: {filename} ({len(nik_list)} NIK)")
        except Exception as e:
            print(f"Error menyimpan {filename}: {e}")

    def process_nik_list(self, nik_list):
        """Proses semua NIK dan pisahkan hasilnya"""
        valid_nik = []
        invalid_nik = []
        total_nik = len(nik_list)
        
        print(f"📋 Memproses {total_nik} NIK...")
        print("=" * 50)
        
        for i, nik in enumerate(nik_list):
            print(f"🔍 Checking {i+1}/{total_nik}: {nik}", end=" - ")
            
            result = self.check_nik(nik)
            
            if result == "VALID":
                valid_nik.append(nik)
                print("✅ VALID")
            elif result == "TIDAK_VALID":
                invalid_nik.append(nik)
                print("❌ TIDAK VALID")
            else:
                invalid_nik.append(nik)
                print("⚠️  GAGAL (dimasukkan ke tidak valid)")
            
            # Delay antara request
            if i < total_nik - 1:
                time.sleep(1)  # Delay 1 detik antara request
        
        return valid_nik, invalid_nik

# Jalankan program
if __name__ == "__main__":
    checker = KPUChecker()
    
    # Baca NIK dari file
    input_file = "nik_list.txt"
    
    if not os.path.exists(input_file):
        print(f"❌ File {input_file} tidak ditemukan!")
        print("💡 Buat file nik_list.txt dengan isi:")
        print("3201150410000001")
        print("3201150410000002")
        print("3201150410000003")
        exit()
    
    nik_list = checker.read_nik_from_file(input_file)
    
    if not nik_list:
        print("❌ Tidak ada NIK yang ditemukan dalam file!")
        exit()
    
    print("🚀 Memulai pengecekan NIK...")
    print(f"⏰ Waktu mulai: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Proses semua NIK
    valid_nik, invalid_nik = checker.process_nik_list(nik_list)
    
    # Simpan hasil
    print("\n💾 Menyimpan hasil...")
    checker.save_to_txt(valid_nik, "nik_valid.txt")
    checker.save_to_txt(invalid_nik, "nik_tidak_valid.txt")
    
    # Tampilkan summary
    print("\n" + "=" * 50)
    print("📊 HASIL AKHIR:")
    print("=" * 50)
    print(f"✅ NIK VALID: {len(valid_nik)}")
    print(f"❌ NIK TIDAK VALID: {len(invalid_nik)}")
    print(f"📋 TOTAL: {len(valid_nik) + len(invalid_nik)}")
    print("=" * 50)
    print(f"⏰ Waktu selesai: {datetime.now().strftime('%H:%M:%S')}")
    print("\n🎉 Selesai! File yang dihasilkan:")
    print("   📄 nik_valid.txt")
    print("   📄 nik_tidak_valid.txt")
    
    # Tahan window agar tidak langsung tertutup
    input("\nTekan Enter untuk keluar...")