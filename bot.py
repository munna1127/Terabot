import os
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

API_URL = "https://terabridge-api-bz8z.onrender.com/api/resolve"
API_KEY = os.getenv("API_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 TeraBox Downloader Bot\n\n"
        "TeraBox link bhejo, main file details aur download link de dunga."
    )


async def resolve_terabox(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if "terabox" not in url.lower():
        await update.message.reply_text(
            "❌ Sirf TeraBox link bhejo."
        )
        return


    msg = await update.message.reply_text(
        "⏳ Link process ho raha hai..."
    )


    try:

        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "url": url
        }


        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )


        data = response.json()


        if data.get("status") != "success":

            await msg.edit_text(
                "❌ File resolve nahi hui."
            )
            return


        file = data["files"][0]


        filename = file.get("filename", "Unknown")
        size = file.get("size_mb", "Unknown")
        download = file.get("dlink")

        thumbnail = file.get(
            "thumbnails",
            {}
        ).get("url1")


        text = f"""
✅ File Found

📁 Name:
{filename}

📦 Size:
{size} MB
"""


        buttons = [
            [
                InlineKeyboardButton(
                    "⬇️ Download",
                    url=download
                )
            ]
        ]


        await msg.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


    except Exception as e:

        await msg.edit_text(
            f"⚠️ Error:\n{e}"
        )



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "TeraBox link bhejo aur wait karo."
    )



def main():

    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        return

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            resolve_terabox
        )
    )


    print("🤖 Bot Started")

    app.run_polling()



if __name__ == "__main__":
    main()
