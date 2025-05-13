import os
import subprocess
import uuid
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from config import CR_EMAIL, CR_PASSWORD, BOT_TOKEN, COOKIES_PATH, UPLOAD_FORMAT, METADATA_TAG, DOWNLOAD_DIR

# Download queue storage (task_id -> download task)
download_queue = {}

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# /dl command handler
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /dl [Crunchyroll URL]")
        return

    url = context.args[0]
    task_id = str(uuid.uuid4())[:8]
    file_output = f"{DOWNLOAD_DIR}/{METADATA_TAG}-%(title)s.%(ext)s"

    command = [
        "yt-dlp",
        "--cookies", COOKIES_PATH,
        "--output", file_output,
        "--merge-output-format", "mkv",
        "--no-playlist",
        url
    ]

    # Save task
    download_queue[task_id] = {
        "url": url,
        "user": update.effective_user.first_name,
        "status": "Queued"
    }

    await update.message.reply_text(f"📥 Task queued with ID `{task_id}`.\nDownloading: {url}", parse_mode='Markdown')

    # Run download in background
    async def run_download():
        download_queue[task_id]["status"] = "Downloading"
        try:
            subprocess.run(command, check=True)
            download_queue[task_id]["status"] = "Completed"
        except subprocess.CalledProcessError:
            download_queue[task_id]["status"] = "Failed"

    context.application.create_task(run_download())

# /queue command handler
async def queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not download_queue:
        await update.message.reply_text("✅ Queue is empty.")
        return
    message = "📋 *Download Queue:*\n"
    for tid, data in download_queue.items():
        message += f"- `{tid}`: {data['url']} | *{data['status']}*\n"
    await update.message.reply_text(message, parse_mode='Markdown')

# /cancel command handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /cancel [task_id]")
        return

    task_id = context.args[0]
    if task_id in download_queue:
        download_queue[task_id]["status"] = "Cancelled"
        await update.message.reply_text(f"❌ Task `{task_id}` marked as cancelled.", parse_mode='Markdown')
    else:
        await update.message.reply_text("⚠️ Task not found.")

# /set_upload_format command handler
async def set_upload_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global UPLOAD_FORMAT
    if not context.args or context.args[0] not in ['video', 'file']:
        await update.message.reply_text("Usage: /set_upload_format [video/file]")
        return
    UPLOAD_FORMAT = context.args[0]
    await update.message.reply_text(f"✅ Upload format set to `{UPLOAD_FORMAT}`.", parse_mode='Markdown')

# /metadata command handler
async def metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global METADATA_TAG
    if not context.args:
        await update.message.reply_text("Usage: /metadata [tag]")
        return
    METADATA_TAG = context.args[0]
    await update.message.reply_text(f"✅ Metadata tag set to `{METADATA_TAG}`", parse_mode='Markdown')

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🎬 *Crunchyroll Downloader Bot*\n\n"
        "/dl [URL] - Download anime from Crunchyroll\n"
        "/queue - Check current download queue\n"
        "/cancel [task_id] - Cancel a download task\n"
        "/set_upload_format [video/file] - Set upload format\n"
        "/metadata [name] - Set custom metadata tag"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

# Main setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dl", dl))
    app.add_handler(CommandHandler("queue", queue))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("set_upload_format", set_upload_format))
    app.add_handler(CommandHandler("metadata", metadata))

    print("🤖 Bot is running...")
    app.run_polling()
