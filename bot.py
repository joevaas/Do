import os import subprocess import uuid from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes from config import ( BOT_TOKEN, CR_EMAIL, CR_PASSWORD, DOWNLOAD_DIR, METADATA_TAG, WIDEVINE_BLOB_PATH, WIDEVINE_KEY_PATH, COOKIES_DIR )

Ensure required directories exist

os.makedirs(DOWNLOAD_DIR, exist_ok=True) os.makedirs(COOKIES_DIR, exist_ok=True)

Function to log into Crunchyroll and save cookies

def login_to_crunchyroll(): cookies_file = os.path.join(COOKIES_DIR, "cookies.txt") if os.path.exists(cookies_file): return cookies_file

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

/start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "👋 Welcome to Crunchyroll Downloader Bot!\n\n" "Use:\n/dl <Crunchyroll Video URL>\n" "Ensure your account has access to the video.", parse_mode='Markdown' )

/dl command

async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE): if not context.args: await update.message.reply_text("Usage: /dl <Crunchyroll URL>") return

url = context.args[0]
task_id = str(uuid.uuid4())[:8]
output_basename = f"{METADATA_TAG}-{task_id}"
encrypted_file = os.path.join(DOWNLOAD_DIR, output_basename + ".mp4")
decrypted_file = os.path.join(DOWNLOAD_DIR, output_basename + "-decrypted.mp4")

cookies_file = login_to_crunchyroll()
if not cookies_file:
    await update.message.reply_text("❌ Login failed. Check your credentials.")
    return

msg = await update.message.reply_text(f"📥 Starting download for `{task_id}`...", parse_mode="Markdown")

# Download encrypted stream with yt-dlp
try:
    subprocess.run([
        "yt-dlp",
        "--allow-unplayable-formats",
        "--no-playlist",
        "--cookies", cookies_file,
        "-o", encrypted_file,
        url
    ], check=True)
except subprocess.CalledProcessError as e:
    await update.message.reply_text(f"❌ yt-dlp failed: {e}")
    return

# Extract key using Widevine device files
try:
    await msg.edit_text("🔑 Extracting decryption key...")
    pssh_cmd = ["mp4dump", encrypted_file, "|", "grep", "pssh"]
    result = subprocess.run("mp4dump \"{}\" | grep pssh".format(encrypted_file), shell=True, capture_output=True, text=True)
    pssh_line = result.stdout.strip()
    pssh_value = pssh_line.split('data: ')[1] if 'data:' in pssh_line else None
    if not pssh_value:
        await update.message.reply_text("❌ Failed to extract PSSH from the video.")
        return

    key_result = subprocess.run([
        "wvd", "--pssh", pssh_value,
        "--client_id", WIDEVINE_BLOB_PATH,
        "--private_key", WIDEVINE_KEY_PATH
    ], capture_output=True, text=True, check=True)

    key_line = key_result.stdout.strip().split('\n')[-1]
    if ':' not in key_line:
        await update.message.reply_text("❌ Failed to retrieve decryption key.")
        return
    decryption_key = key_line.strip()
except Exception as e:
    await update.message.reply_text(f"❌ Key extraction failed: {e}")
    return

# Decrypt using mp4decrypt
try:
    await msg.edit_text("🔐 Decrypting video...")
    subprocess.run([
        "mp4decrypt", "--key", decryption_key, encrypted_file, decrypted_file
    ], check=True)
except subprocess.CalledProcessError as e:
    await update.message.reply_text(f"❌ Decryption failed: {e}")
    return

# Upload video
await msg.edit_text("✅ Uploading decrypted video...")
await update.message.reply_video(video=open(decrypted_file, 'rb'), caption=f"🎞️ `{task_id}`", parse_mode="Markdown")

Start the bot

if name == "main": app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("dl", dl)) print("🤖 Bot is running...") app.run_polling()

