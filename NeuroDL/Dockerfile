# Use an official, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install FFmpeg (Required by yt-dlp to merge video/audio and extract mp3)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy your requirements file and install the Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your files into the container (bot.py, cookies.txt, etc.)
COPY . .

# Tell Docker to run your bot when the container starts
CMD ["python", "bot.py"]