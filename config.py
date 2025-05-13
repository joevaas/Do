
### `config.py`

This file will contain the bot's configuration settings and load the environment variables from the `.env` file.

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Crunchyroll Credentials
CR_EMAIL = os.getenv('CR_EMAIL')
CR_PASSWORD = os.getenv('CR_PASSWORD')

# Optional: L3 Bearer Token for Crunchyroll (if you're using this instead of cookies)
L3_KEY = os.getenv('L3_KEY')

# Widevine BLOB and Key Paths (used for decryption)
WIDEVINE_BLOB_PATH = os.getenv('WIDEVINE_BLOB_PATH', "widevine/device_client_id_blob")
WIDEVINE_KEY_PATH = os.getenv('WIDEVINE_KEY_PATH', "widevine/device_private_key")

# Download Directory (where downloaded files will be stored)
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', "downloads")

# Metadata Tag to help with naming downloaded files
METADATA_TAG = os.getenv('METADATA_TAG', "crunchyroll_download")
