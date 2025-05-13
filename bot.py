import os
import subprocess
import uuid
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, CR_EMAIL, CR_PASSWORD, DOWNLOAD_DIR, METADATA_TAG, WIDEVINE_BLOB_PATH, WIDEVINE_KEY_PATH

# Ensure the downloads directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to handle Crunchyroll login
def login_to_crunchyroll():
    cookies_file = os.path.join(DOWNLOAD_DIR, "cookies.txt")
    if os.path.exists(cookies_file):
        return cookies_file
    
    try:
        login_command = [
            "yt-dlp",
            "--username", CR_EMAIL,
            "--password", CR_PASSWORD,
            "--write-info-json",
            "--cookies", cookies_file,
            "https://www.crunchyroll.com"
        ]
        subprocess.run(login_command, check=True)
        print("Login successful. Cookies saved.")
        return cookies_file
    except subprocess.CalledProcessError as e:
        print(f"Login failed: {e}")
        return None

# Progress hook function to capture and update download status
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] else 0
        speed = d.get('speed', 0) / (1024 * 1024)  # Convert speed to MB/s
        eta = d.get('eta', 0)  # ETA in seconds
        file_name = d.get('filename', "Unknown")
        
        # Formatting the download progress bar
        progress_bar = "■" * int(percent // 10) + "□" * (10 - int(percent // 10))
        
        # Display download progress
        progress_message = (
            f"🎬 {file_name} Download Started...\n"
            f"{progress_bar}\n\n"
            f"🔗 Size: {d['total_bytes'] / (1024 * 1024):.2f} MB | {d['downloaded_bytes'] / (1024 * 1024):.2f} MB\n"
            f"⏳ Done: {percent:.2f}%\n"
            f"🚀 Speed: {speed:.2f} MB/s\n"
            f"⏰ ETA: {eta}s"
        )

        # Update the bot message with the current progress
        if hasattr(progress_hook, 'current_message_id'):
            progress_hook.current_message.edit_text(progress_message)
        else:
            progress_hook.current_message = d['update'].message.reply_text(progress_message)

# /dl command
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /dl <Crunchyroll URL>")
        return

    url = context.args[0]
    task_id = str(uuid.uuid4())[:8]
    output_template = f"{DOWNLOAD_DIR}/{METADATA_TAG}-%(title)s.%(ext)s"

    # Ensure we are logged in to Crunchyroll
    cookies_file = login_to_crunchyroll()
    if not cookies_file:
        await update.message.reply_text("❌ Failed to authenticate with Crunchyroll. Please check credentials.")
        return

    # yt-dlp command with Widevine decryption support and authentication using cookies
    command = [
        "yt-dlp",
        "--external-downloader", "aria2c",
        "--output", output_template,
        "--merge-output-format", "mkv",
        "--no-playlist",
        "--cookies", cookies_file,  # Use the cookies file for authentication
        "--downloader-args", f"ffmpeg_i:-client_id_blob {WIDEVINE_BLOB_PATH} -private_key {WIDEVINE_KEY_PATH}",
        "--progress",  # Enable progress display
        "--quiet",  # Make it quieter for processing, will rely on the custom progress hook
        url
    ]

    # Send an initial message that download has started
    initial_message = await update.message.reply_text(f"📥 Download Started: `{task_id}`\nURL: {url}", parse_mode='Markdown')

    # Set the message object for progress hook to update
    progress_hook.current_message = initial_message

    # Run the download in a separate task to avoid blocking
    async def run_download():
        try:
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
            await update.message.reply_text(f"✅ Download complete for `{task_id}`", parse_mode='Markdown')
        except subprocess.CalledProcessError as e:
            await update.message.reply_text(f"❌ Download failed: {str(e)}", parse_mode='Markdown')

    context.application.create_task(run_download())

# Main bot setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("dl", dl))
    print("🤖 Bot is running...")
    app.run_polling()
