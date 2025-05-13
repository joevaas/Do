# Crunchyroll Downloader Bot

This is a Telegram bot that allows users to download Crunchyroll episodes directly from Crunchyroll's website. It supports several features, including checking the download queue, cancelling tasks, and setting custom upload formats.

## Features

- `/dl [URL]` - Download anime from Crunchyroll
- `/queue` - Check current download queue
- `/cancel [task_id]` - Cancel a download task
- `/set_upload_format [video/file]` - Set upload format for downloads
- `/metadata [tag]` - Set custom metadata tag for downloaded videos

## Requirements

- **Python 3.8+**
- **yt-dlp** (for downloading videos)
- **python-telegram-bot** (for Telegram bot functionality)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/crunchyroll-bot.git
    cd crunchyroll-bot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Crunchyroll credentials:
   - Open `config.py` and add your **Crunchyroll email** and **password** as follows:

    ```python
    CR_EMAIL = "your_email@example.com"
    CR_PASSWORD = "your_password"
    ```

4. Set up your Telegram bot:
   - Create a bot with [BotFather](https://t.me/BotFather) on Telegram and get the bot token.
   - Replace `your_telegram_bot_token` in `config.py` with your bot token.

5. Run the bot:

    ```bash
    python bot.py
    ```

## Docker Setup

To run this bot in a Docker container:

1. Build the Docker image:

    ```bash
    docker build -t crunchyroll-bot .
    ```

2. Run the Docker container:

    ```bash
    docker run -d --env-file .env --name crunchyroll-bot crunchyroll-bot
    ```

## License

This project is licensed under the MIT License.
