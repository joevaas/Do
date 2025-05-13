# Use a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the working directory
COPY . .

# Expose the port (for webhooks if you're using one)
EXPOSE 80

# Set environment variables from .env
COPY .env .env

# Run bot.py when the container starts
CMD ["python", "bot.py"]
