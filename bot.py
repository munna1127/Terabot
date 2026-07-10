import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

BOT_TOKEN = "YOUR_BOT_TOKEN"
API_KEY = "Aryan123@API"
API_URL = "https://terabridge-api-bz8z.onrender.com/api/resolve"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a TeraBox link."
    )


async def resolve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "terabox" not in text and "1024terabox" not in text:
        await update.message.reply_text("❌ Send a valid TeraBox link.")
        return

    msg = await update.message.reply_text("⏳ Resolving...")

    try:
        r = requests.get(
            API_URL,
            headers={"X-API-Key": API_KEY},
            params={
                "url": text,
                "mode": "stream"
            },
            timeout=120,
        )

        data = r.json()

        if data.get("status") != "success":
            await msg.edit_text("❌ Failed.")
            return

        file = data["files"][0]

        caption = f"""
🎬 <b>{file['filename']}</b>

📦 Size: {file['size_mb']} MB

"""

        kb = [
            [
                InlineKeyboardButton("▶ Watch", url=file["stream_url"]),
                InlineKeyboardButton("⬇ Download", url=file["dlink"]),
            ]
        ]

        thumb = file["thumbnails"]["url3"]

        await update.message.reply_photo(
            photo=thumb,
            caption=caption,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(kb),
        )

        await msg.delete()

    except Exception as e:
        await msg.edit_text(str(e))


def main():
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=120,
        write_timeout=120,
        pool_timeout=120,
    )

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resolve))

    print("Bot Started...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
