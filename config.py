import os

# Crunchyroll Credentials
CR_EMAIL = os.getenv('CR_EMAIL', 'your_email@example.com')
CR_PASSWORD = os.getenv('CR_PASSWORD', 'your_password')

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_telegram_bot_token')

# Path for Crunchyroll cookies (if used)
COOKIES_PATH = os.getenv('COOKIES_PATH', 'cookies.txt')

# Default settings
UPLOAD_FORMAT = 'video'  # 'video' or 'file'
METADATA_TAG = 'CrunchyBot'

# Downloads directory
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')
