#!/bin/bash

# Get inputs from the command line
URL=$1
FORMAT=$2 # 'video' or 'audio'

# Basic validation
if [ -z "$URL" ]; then
    echo "❌ Error: Please provide a URL."
    echo "Usage: ./downloader.sh <URL> [video|audio]"
    exit 1
fi

# Default to video if no format is provided
if [ -z "$FORMAT" ]; then
    FORMAT="video"
fi

# --- SMART COOKIE ROUTING ---
COOKIE_ARGS=""
if [[ "$URL" == *"instagram.com"* ]]; then
    COOKIE_ARGS="--cookies instagram_cookies.txt"
elif [[ "$URL" == *"youtube.com"* || "$URL" == *"youtu.be"* ]]; then
    COOKIE_ARGS="--cookies youtube_cookies.txt"
fi

# Set up the output filename template
OUTPUT_TEMPLATE="temp_download_%(id)s.%(ext)s"

echo "⏳ Downloading $FORMAT... This might take a minute."

# Execute yt-dlp based on the requested format
if [ "$FORMAT" == "video" ]; then
    yt-dlp \
        --quiet --no-warnings \
        --extractor-args "youtube:player_client=ios,android,web_safari" \
        $COOKIE_ARGS \
        -f "bestvideo+bestaudio/b/best" \
        --merge-output-format mp4 \
        -o "$OUTPUT_TEMPLATE" \
        "$URL"
        
elif [ "$FORMAT" == "audio" ]; then
    yt-dlp \
        --quiet --no-warnings \
        --extractor-args "youtube:player_client=ios,android,web_safari" \
        $COOKIE_ARGS \
        -f "bestaudio/best" \
        --extract-audio \
        --audio-format mp3 \
        --audio-quality 192K \
        -o "$OUTPUT_TEMPLATE" \
        "$URL"
else
    echo "❌ Invalid format. Please specify 'video' or 'audio'."
    exit 1
fi

echo "✅ Download complete!"