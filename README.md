# Crunchyroll Downloader Bot

This is a Telegram bot that allows you to download anime episodes from Crunchyroll.

## Setup

### Prerequisites

- Python 3.10+ or Docker
- Telegram bot token
- Crunchyroll login credentials (email and password)
- Optional: L3 Key (for advanced features)

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/crunchyroll-downloader-bot.git
    cd crunch-roller-downloader-bot
    ```

2. Install dependencies:

    If you're using Python:

    ```bash
    pip install -r requirements.txt
    ```

    Or use Docker (recommended for deployment):

    ```bash
    docker build -t crunch-roller-bot .
    docker run -d crunch-roller-bot
    ```

### Configuration

1. Create a `.env` file with your **Crunchyroll** credentials and **Telegram Bot Token**:

    ```env
    BOT_TOKEN=your_telegram_bot_token
    CR_EMAIL=your_crunchyroll_email
    CR_PASSWORD=your_crunchyroll_password
    L3_KEY=your_l3_key_here  # Optional, only needed if using L3 authentication
    ```

### Running the Bot

Once everything is set up, you can run the bot with:

```bash
python bot.py
