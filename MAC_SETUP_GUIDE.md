# YouTube Downloader - Mac Setup Guide

Complete setup instructions for macOS users.

## Prerequisites

- macOS 10.14 (Mojave) or later
- Python 3.7+ (comes pre-installed on modern Macs, or use Homebrew)
- Terminal access

## Step-by-Step Installation

### 1. Install Homebrew (if not already installed)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3 (if needed)

Check if Python 3 is installed:

```bash
python3 --version
```

If not installed or version is below 3.7:

```bash
brew install python
```

### 3. Install FFmpeg

FFmpeg is required for video processing:

```bash
brew install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

### 4. Download the YouTube Downloader

Navigate to where you want to install the app:

```bash
cd ~/Downloads
# Or clone/download the repository
```

### 5. Install Python Dependencies

From the project directory:

```bash
pip3 install -r requirements.txt
```

Or install manually:

```bash
pip3 install customtkinter yt-dlp
```

### 6. Make the Script Executable (Optional)

```bash
chmod +x youtube_downloader.py
```

## Running the Application

### Method 1: Using Python

```bash
python3 youtube_downloader.py
```

### Method 2: Direct Execution (if made executable)

```bash
./youtube_downloader.py
```

### Method 3: Create an App Launcher (Advanced)

You can create an Automator application:

1. Open **Automator** (found in Applications/Utilities)
2. Select **Application** as the document type
3. Add a **Run Shell Script** action
4. Set the shell to `/bin/bash`
5. Add this script (adjust path to your location):

```bash
cd /path/to/youtube_downloader
python3 youtube_downloader.py
```

6. Save as "YouTube Downloader" in your Applications folder

## Usage Examples

### Download a Single Video

1. Launch the app
2. Paste URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. Select category: **Music**
4. Click **Download**

### Download a Playlist

1. Paste playlist URL: `https://www.youtube.com/playlist?list=PLxxxxxx`
2. Select category: **Coding**
3. Click **Download**
4. All videos will be downloaded to `~/Downloads/YouTube/Coding/`

### Download a Video Segment

1. Paste video URL
2. Set **Start time**: `00:01:30`
3. Set **End time**: `00:03:45`
4. Select category
5. Click **Download**

## Default Download Location

Videos are saved to:

```
~/Downloads/YouTube/
├── History/
├── Math/
├── Home Improvement/
├── Coding/
├── Music/
└── Entertainment/
```

## Customizing Settings

Edit `config.json` (created on first run):

```json
{
  "download_base_path": "/Users/yourname/Movies/YouTube",
  "categories": {
    "History": "History",
    "Math": "Math",
    "Home Improvement": "Home Improvement",
    "Coding": "Coding",
    "Music": "Music",
    "Entertainment": "Entertainment",
    "Custom": "My Custom Folder"
  },
  "default_category": "Entertainment",
  "default_quality": "720p",
  "default_format": "mp4"
}
```

## Troubleshooting

### "Python not found"

Make sure Python 3 is installed:

```bash
brew install python
```

Then use `python3` instead of `python`.

### "Module not found: customtkinter"

Install dependencies:

```bash
pip3 install customtkinter yt-dlp
```

If you get permission errors, try:

```bash
pip3 install --user customtkinter yt-dlp
```

### "FFmpeg not found" or "Postprocessor failed"

Install or reinstall FFmpeg:

```bash
brew install ffmpeg
```

Verify it's in your PATH:

```bash
which ffmpeg
```

### "Permission denied" when running the script

Make the script executable:

```bash
chmod +x youtube_downloader.py
```

### Application window doesn't appear

- Make sure you're running from Terminal, not via SSH
- Check if other GUI applications can run
- Try running with Python directly: `python3 youtube_downloader.py`

### Download is slow

- This depends on your internet connection
- YouTube may throttle download speeds
- Try downloading during off-peak hours

### Video format not compatible with QuickTime

The app is configured to download H.264/AAC format for maximum compatibility. If you still have issues:

1. Update QuickTime Player
2. Try opening with VLC (install via: `brew install --cask vlc`)
3. The video file should have `.mp4` extension

## Performance Tips

### Speed up downloads

- Close other bandwidth-intensive applications
- Connect via Ethernet instead of Wi-Fi
- Download one video at a time for faster speeds

### Save disk space

- The default 720p setting is a good balance
- Edit `config.json` to change default quality
- Manually delete old videos from the download folders

## Security & Privacy

- This app only communicates with YouTube
- No data is collected or sent to third parties
- Your download history is stored locally only
- Config file contains only local paths and preferences

## Keyboard Shortcuts (when app is focused)

- **Cmd+Q**: Quit application
- **Cmd+V**: Paste into URL field (when focused)
- **Tab**: Navigate between fields
- **Enter**: Start download (when URL field is focused)

## Uninstalling

To remove the application:

1. Delete the application folder
2. Delete download folders (if desired): `~/Downloads/YouTube/`
3. Delete config file: `rm config.json`
4. Uninstall Python packages (optional):

```bash
pip3 uninstall customtkinter yt-dlp
```

## Getting Help

If you encounter issues:

1. Check the status log in the app window
2. Review this troubleshooting guide
3. Verify all prerequisites are installed
4. Check yt-dlp GitHub for known issues

## Updates

To update yt-dlp to the latest version:

```bash
pip3 install --upgrade yt-dlp
```

## Legal Notice

- Only download videos you have permission to download
- Respect copyright and content creator rights
- This tool is for personal use only
- Review YouTube's Terms of Service

Enjoy your YouTube Downloader! 🎬
