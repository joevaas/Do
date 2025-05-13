# Use a lightweight version of Python 3
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files into the container
COPY . .

# Install python-dotenv for handling environment variables
RUN pip install python-dotenv

# Expose a port (not necessary for Telegram bot, but can be useful for debugging)
EXPOSE 5000

# Run the bot
CMD ["python", "bot.py"]
