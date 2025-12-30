# YouTube Downloader Pro v2.0

A modern, feature-rich YouTube downloader with a beautiful interface built with CustomTkinter and yt-dlp.

## ✨ New in v2.0

- 🔗 **Batch Downloads** - Paste multiple URLs at once
- 📝 **Playlist Confirmation** - Warns before downloading playlists with video count
- 🎬 **Quality Selector** - Choose from 360p, 480p, 720p, 1080p, or Best
- ⏹️ **Cancel Downloads** - Stop downloads anytime
- 📁 **Quick Access** - Open downloads folder with one click
- 📋 **Paste & Clear** - Helper buttons for easy URL management
- 🎯 **Current Video Display** - See what's downloading in real-time
- 🚫 **Mix/Radio Filter** - Automatically rejects YouTube auto-generated mixes
- 📊 **Download Queue** - Batch process multiple videos sequentially

## Features

### Core Functionality
- ✅ **YouTube-only downloads** - Validates URLs to ensure YouTube sources only
- 📁 **Category-based organization** - Six preset categories (History, Math, Home Improvement, Coding, Music, Entertainment)
- 🎬 **Multiple quality options** - 360p, 480p, 720p, 1080p, or Best available
- 📝 **Playlist support** - Download entire playlists with confirmation dialog
- ⏱️ **Video segments** - Download specific time ranges from videos
- 💾 **Persistent settings** - Config saved in JSON for your preferences
- 🎨 **Modern UI** - Clean, intuitive dark-themed interface

### User Experience
- 🔗 **Batch processing** - Add multiple URLs (one per line) and download sequentially
- 📋 **Clipboard integration** - Paste button for easy URL entry
- 🗑️ **Quick clear** - Clear URLs and logs with one click
- 📂 **Direct folder access** - Open download folder from the app
- ⏹️ **Cancelable** - Stop downloads mid-process
- 📊 **Real-time feedback** - Live progress, speed, ETA, and current video title
- 🔔 **Smart warnings** - Playlist confirmation prevents accidental bulk downloads

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- FFmpeg (for video processing)

### macOS Installation

1. **Install FFmpeg**:
```bash
brew install ffmpeg
```

2. **Install Python** (if using system Python causes issues):
```bash
brew install python-tk@3.11
```

3. **Clone or download this repository**

4. **Install Python dependencies**:
```bash
pip3 install -r requirements.txt
```

Or manually:
```bash
pip3 install customtkinter yt-dlp
```

## Usage

### Running the Application

**Easiest way - Double-click:**
```
Double-click "YouTube Downloader.command"
```

**Or from Terminal:**
```bash
# If you have Homebrew Python 3.11:
python3.11 youtube_downloader.py

# Or with system Python:
python3 youtube_downloader.py
```

### Quick Start Guide

#### Single Video Download
1. Paste a YouTube URL in the text box
2. Select quality (720p recommended)
3. Choose a category
4. Click **Download**

#### Batch Download Multiple Videos
1. Paste multiple URLs, **one per line**:
   ```
   https://www.youtube.com/watch?v=video1
   https://www.youtube.com/watch?v=video2
   https://www.youtube.com/watch?v=video3
   ```
2. Select quality and category
3. Click **Download**
4. Videos download one after another

#### Playlist Download
1. Paste a playlist URL
2. A confirmation dialog shows the video count
3. Click **Download All** to proceed or **Cancel** to skip
4. All videos download to your chosen category

#### Video Segment Download
1. Paste a video URL
2. Set **Start time**: `00:01:30` (1 minute, 30 seconds)
3. Set **End time**: `00:03:45` (3 minutes, 45 seconds)
4. Only that segment downloads

### UI Guide

**Top Section:**
- 📋 **Paste** button - Pastes URLs from clipboard
- 🗑️ **Clear** button - Clears the URL box
- Text area - Enter URLs (one per line for batch downloads)

**Settings:**
- **Category** dropdown - Where to save files
- **Quality** dropdown - Video quality (360p - Best)

**Time Segment (Optional):**
- Start/End times in HH:MM:SS format
- Leave blank to download full videos

**Action Buttons:**
- ⬇️ **Download** - Start downloading
- ⏹️ **Cancel** - Stop current download (enabled during download)
- 📁 **Open Folder** - Opens the download folder in Finder

**Progress:**
- Shows current video name
- Progress bar with percentage, speed, and ETA
- Activity log with timestamps

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

Click **📁 Open Folder** to view your downloads instantly!

## Configuration

The app creates a `config.json` file on first run:

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

Edit this file to:
- Change default download location
- Add custom categories
- Set default quality and category

## Technical Details

- **Video Quality**: Configurable (360p, 480p, 720p, 1080p, or Best)
- **Codec**: H.264 video, AAC audio (optimized for QuickTime)
- **Format**: MP4 (universal compatibility)
- **Playlist Handling**: Individual video downloads with progress tracking
- **Mix/Radio Protection**: Automatically filters out YouTube auto-generated playlists
- **Threading**: Non-blocking downloads with real-time UI updates
- **Cancellation**: Graceful cancel support mid-download

## Troubleshooting

### Blank Window on Launch

**Solution**: Use Homebrew Python instead of system Python
```bash
brew install python-tk@3.11
python3.11 youtube_downloader.py
```

### "No module named 'customtkinter'"

**Solution**: Install dependencies
```bash
pip3 install -r requirements.txt
```

### "FFmpeg not found"

**Solution**: Install FFmpeg
```bash
brew install ffmpeg
```

### Download Fails with "Video unavailable"

- Check if the video is private or region-locked
- Verify the URL is correct
- Try a different quality setting

### Accidentally Started Downloading a Huge Playlist

- Click the **⏹️ Cancel** button immediately
- The download will stop and clear the queue
- Next version will confirm playlists before starting (already implemented in v2.0!)

### Progress Bar Not Updating

- Normal for very small/fast downloads
- Works best with larger files (>10MB)
- Progress updates every few seconds

## Pro Tips

### Batch Downloading
Paste multiple URLs at once for unattended downloads:
```
https://www.youtube.com/watch?v=tutorial1
https://www.youtube.com/watch?v=tutorial2
https://www.youtube.com/watch?v=tutorial3
```
All videos download sequentially!

### Quality Selection
- **360p**: Small files, mobile viewing
- **480p**: Standard quality, saves space
- **720p**: HD, best balance (recommended)
- **1080p**: Full HD, larger files
- **Best**: Maximum available quality

### Time Segments
Extract specific parts of long videos:
- Lectures: Download only the relevant section
- Music videos: Skip intros/outros
- Tutorials: Get just the part you need

### Organize Downloads
Use categories to keep everything organized:
- **History**: Documentary videos
- **Math**: Khan Academy tutorials
- **Coding**: Programming courses
- **Music**: Music videos and concerts
- **Entertainment**: Everything else

## Keyboard Shortcuts

When the app is focused:
- **Cmd+V**: Paste into URL field
- **Cmd+Q**: Quit application
- **Tab**: Navigate between fields

## What's New in Each Version

### v2.0 (Current)
- Multi-URL batch downloads
- Playlist confirmation dialog
- Quality selector (360p-Best)
- Cancel button
- Open folder button
- Paste/Clear helper buttons
- Current video display
- Mix/radio playlist filter
- Enhanced error messages

### v1.0
- Initial release
- Single URL downloads
- 720p MP4 default
- Category organization
- Time segment support
- Basic progress tracking

## Credits

Built with:
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful YouTube download engine
- [FFmpeg](https://ffmpeg.org/) - Video processing

## License

MIT License - Feel free to use and modify as needed!

## Support

Having issues? Check:
1. This README's troubleshooting section
2. The activity log in the app for specific errors
3. Ensure all prerequisites are installed correctly

---

Made with ❤️ for easy YouTube downloading
