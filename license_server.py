from flask import Flask, request, jsonify

app = Flask(__name__)

# Contoh database lisensi sederhana (bisa diganti dengan database asli)
from datetime import datetime, timedelta
licenses = {
    # license_key: {"hardware_id": "", "active": True/False, "expired_date": "YYYY-MM-DD"}
    "ABC123": {"hardware_id": "1234567890", "active": True, "expired_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')},
    "DEF456": {"hardware_id": "", "active": False, "expired_date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
}

@app.route('/check_license', methods=['GET'])
def check_license_get():
    return '<h2>Gunakan metode POST untuk memeriksa lisensi.</h2>', 200

@app.route('/check_license', methods=['POST'])
def check_license():
    data = request.get_json()
    license_key = data.get('license_key')
    hardware_id = data.get('hardware_id')
    lic = licenses.get(license_key)
    if lic and lic["active"]:
        # Cek expired
        expired_date = lic.get("expired_date")
        if expired_date:
            try:
                expired_dt = datetime.strptime(expired_date, '%Y-%m-%d')
                if datetime.now() > expired_dt:
                    return jsonify({"valid": False, "reason": "expired"})
            except Exception:
                return jsonify({"valid": False, "reason": "invalid_expired_date"})
        # Jika hardware_id belum terisi, daftarkan hardware_id pertama kali
        if not lic["hardware_id"]:
            lic["hardware_id"] = hardware_id
            return jsonify({"valid": True})
        # Jika hardware_id cocok, izinkan
        if lic["hardware_id"] == hardware_id:
            return jsonify({"valid": True})
    return jsonify({"valid": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
