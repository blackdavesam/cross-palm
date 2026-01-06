#!/bin/bash
# YouTube Downloader Launcher
# Double-click this file to open the YouTube Downloader

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the script directory
cd "$SCRIPT_DIR"

# Check if dependencies are installed
if ! python3 -c "import customtkinter" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install customtkinter yt-dlp
fi

# Run the YouTube Downloader
echo "Starting YouTube Downloader..."
python3 youtube_downloader.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press any key to close..."
    read -n 1
fi
