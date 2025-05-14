import os
import subprocess
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import (
    BOT_TOKEN, CR_EMAIL, CR_PASSWORD, DOWNLOAD_DIR, METADATA_TAG,
    WIDEVINE_BLOB_PATH, WIDEVINE_KEY_PATH, COOKIES_DIR
)

# Ensure required directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(COOKIES_DIR, exist_ok=True)

# Function to log into Crunchyroll and save cookies
def login_to_crunchyroll():
    cookies_file = os.path.join(COOKIES_DIR, "cookies.txt")
    if os.path.exists(cookies_file):
        return cookies_file

    try:
        login_command = [
            "yt-dlp",
            "--username", CR_EMAIL,
            "--password", CR_PASSWORD,
            "--cookies", cookies_file,
            "--no-download",
            "https://www.crunchyroll.com"
        ]
        subprocess.run(login_command, check=True)
        print("Login successful. Cookies saved.")
        return cookies_file
    except subprocess.CalledProcessError as e:
        print(f"Login failed: {e}")
        return None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Crunchyroll Downloader Bot!\n\n"
        "Use:\n`/dl <Crunchyroll Video URL>`\n"
        "Ensure your account has access to the video.",
        parse_mode='Markdown'
    )

# /dl command
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /dl <Crunchyroll URL>")
        return

    url = context.args[0]
    task_id = str(uuid.uuid4())[:8]
    output_basename = f"{METADATA_TAG}-{task_id}"
    video_file = os.path.join(DOWNLOAD_DIR, output_basename + ".mp4")
    decrypted_file = os.path.join(DOWNLOAD_DIR, output_basename + "-decrypted.mp4")

    cookies_file = login_to_crunchyroll()
    if not cookies_file:
        await update.message.reply_text("❌ Login failed. Check your credentials.")
        return

    msg = await update.message.reply_text(f"📥 Starting download for `{task_id}`...", parse_mode="Markdown")

    try:
        subprocess.run([
            "yt-dlp",
            "--allow-unplayable-formats",
            "--no-playlist",
            "--cookies", cookies_file,
            "-o", video_file,
            url
        ], check=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ yt-dlp failed: {e}")
        return

    try:
        await msg.edit_text("🔐 Decrypting with mp4decrypt...")
        
        # Using WIDEVINE_BLOB_PATH and WIDEVINE_KEY_PATH for decryption
        subprocess.run([
            "mp4decrypt", 
            "--key", f"file:{WIDEVINE_KEY_PATH}",
            "--client_id_blob", WIDEVINE_BLOB_PATH,
            video_file, decrypted_file
        ], check=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Decryption failed: {e}")
        return

    await msg.edit_text("✅ Download and decryption complete.")
    await update.message.reply_video(video=open(decrypted_file, 'rb'), caption=f"🎞️ `{task_id}`", parse_mode="Markdown")

# Start the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dl", dl))
    print("🤖 Bot is running...")
    app.run_polling()
