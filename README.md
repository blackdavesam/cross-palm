# YouTube Downloader GUI

A modern, lightweight YouTube downloader with a clean interface built with CustomTkinter and yt-dlp.

## Features

- ✅ **YouTube-only downloads** - Validates URLs to ensure YouTube sources only
- 📁 **Category-based organization** - Six preset categories (History, Math, Home Improvement, Coding, Music, Entertainment)
- 🎬 **720p MP4 default** - H.264/AAC codec for QuickTime compatibility
- 📝 **Playlist support** - Download entire playlists with progress tracking
- ⏱️ **Video segments** - Download specific time ranges from videos
- 💾 **Persistent settings** - Config saved in JSON for your preferences
- 🎨 **Modern UI** - Clean, intuitive interface with real-time progress feedback

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- FFmpeg (for video processing)

### macOS Installation

1. **Install FFmpeg** (if not already installed):
```bash
brew install ffmpeg
```

2. **Clone or download this repository**

3. **Install Python dependencies**:
```bash
pip3 install -r requirements.txt
```

## Usage

### Running the Application

```bash
python3 youtube_downloader.py
```

### Quick Start

1. **Paste a YouTube URL** - Single videos, playlists, or shorts
2. **Select a category** - Choose from preset categories or they'll auto-organize
3. **Optional: Set time segment** - Download only a portion of the video (format: HH:MM:SS)
4. **Click Download** - Watch the progress and check the status log

### Examples

**Download a full video:**
- URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Category: `Music`
- Leave time segments blank

**Download a video segment:**
- URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Category: `Music`
- Start time: `00:01:30`
- End time: `00:03:45`

**Download a playlist:**
- URL: `https://www.youtube.com/playlist?list=PLxxxxxxxx`
- Category: `Coding`
- All videos will be downloaded to the Coding folder

## Configuration

The app creates a `config.json` file on first run with:

```json
{
  "download_base_path": "~/Downloads/YouTube",
  "categories": {
    "History": "History",
    "Math": "Math",
    "Home Improvement": "Home Improvement",
    "Coding": "Coding",
    "Music": "Music",
    "Entertainment": "Entertainment"
  },
  "default_category": "Entertainment",
  "default_quality": "720p",
  "default_format": "mp4"
}
```

You can edit this file to customize download paths and categories.

## Download Location

By default, videos are saved to:
```
~/Downloads/YouTube/
├── History/
├── Math/
├── Home Improvement/
├── Coding/
├── Music/
└── Entertainment/
```

## Technical Details

- **Video Quality**: 720p MP4 (H.264 video, AAC audio)
- **Codec**: Optimized for QuickTime and universal playback
- **Format Fallback**: If 720p unavailable, downloads best available quality
- **Playlist Handling**: Downloads each video individually with progress tracking
- **Threading**: Non-blocking downloads with real-time progress updates

## Troubleshooting

### "Command not found: python3"
- Make sure Python 3 is installed: `python3 --version`
- On some systems, use `python` instead of `python3`

### "No module named 'customtkinter'"
- Install dependencies: `pip3 install -r requirements.txt`

### "FFmpeg not found"
- Install FFmpeg: `brew install ffmpeg` (macOS)
- Verify installation: `ffmpeg -version`

### Download fails with "Video unavailable"
- Check if the video is private or region-locked
- Verify the URL is correct and accessible in your browser

### Progress bar not updating
- This is normal for small files that download quickly
- Progress updates work best with larger files (>10MB)

## License

MIT License - Feel free to use and modify as needed!

## Credits

Built with:
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful YouTube download engine
