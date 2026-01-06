# Quick Start Guide - YouTube Downloader

Get up and running in 5 minutes! 🚀

## macOS Installation (3 commands)

```bash
# 1. Install FFmpeg
brew install ffmpeg

# 2. Install Python dependencies
pip3 install customtkinter yt-dlp

# 3. Run the app
python3 youtube_downloader.py
```

## First Download

1. **Copy a YouTube URL**
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Paste it in the app**
   - The URL field is at the top

3. **Choose a category**
   - History, Math, Home Improvement, Coding, Music, or Entertainment

4. **Click Download**
   - Watch the progress bar
   - Check the status log for updates

5. **Find your video**
   - Default location: `~/Downloads/YouTube/[Category]/`

## Common Use Cases

### Download a Tutorial Playlist

```
URL: https://www.youtube.com/playlist?list=PLxxxxxxxxxx
Category: Coding
Time segment: Leave blank
```

All videos download automatically to `~/Downloads/YouTube/Coding/`

### Download Just the Good Part

```
URL: https://www.youtube.com/watch?v=xxxxx
Category: Entertainment
Start time: 00:02:15
End time: 00:05:30
```

Downloads only minutes 2:15 to 5:30 of the video

### Download Music Videos

```
URL: https://www.youtube.com/watch?v=xxxxx
Category: Music
Time segment: Leave blank
```

Perfect quality for QuickTime and Apple devices

## That's It!

Need more details? Check:
- `README.md` - Full documentation
- `MAC_SETUP_GUIDE.md` - Detailed macOS instructions

## Pro Tips

- **Playlists**: Just paste the playlist URL, all videos download automatically
- **Quality**: Default is 720p MP4 (perfect for most uses)
- **Organization**: Videos auto-organize into category folders
- **Segments**: Great for extracting specific parts of lectures or tutorials

Happy downloading! 🎬
