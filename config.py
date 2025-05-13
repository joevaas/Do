import os
from dotenv import load_dotenv

BOT_TOKEN = os.getenv("7848338633:AAF7YnentA7-1TfS54N1YMWaGFRgkDWuG0M")

# Load environment variables from .env file
load_dotenv()

# Crunchyroll Credentials
CR_EMAIL = os.getenv('CR_EMAIL')
CR_PASSWORD = os.getenv('CR_PASSWORD')

# Optional: L3 Bearer Token for Crunchyroll (if you're using this instead of cookies)
L3_KEY = os.getenv('L3_KEY')

# Widevine BLOB and Key Paths (used for decryption)
WIDEVINE_BLOB_PATH = os.getenv('WIDEVINE_BLOB_PATH', "widevine/device_client_id_blob")
WIDEVINE_KEY_PATH = os.getenv('WIDEVINE_KEY_PATH', "widevine/device_private_key")

# Directory paths for downloads and cookies
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', "downloads")
COOKIES_DIR = os.getenv('COOKIES_DIR', "cookies")

# Metadata Tag to help with naming downloaded files
METADATA_TAG = os.getenv('METADATA_TAG', "crunchyroll_download")
