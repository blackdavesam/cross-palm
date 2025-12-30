"""
YouTube Downloader Backend - Enhanced Version
Core functionality without GUI dependencies
"""

import yt_dlp
import json
import re
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List
from datetime import datetime
import urllib.request


class ConfigManager:
    """Manages application configuration and user preferences"""

    DEFAULT_CONFIG = {
        "download_base_path": str(Path.home() / "Downloads" / "YouTube"),
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

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._ensure_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            except json.JSONDecodeError:
                print("Config file corrupted, using defaults")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Save current configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def _ensure_directories(self):
        """Create download directories for all categories"""
        base_path = Path(self.config["download_base_path"])
        base_path.mkdir(parents=True, exist_ok=True)

        for category_folder in self.config["categories"].values():
            category_path = base_path / category_folder
            category_path.mkdir(exist_ok=True)

    def get_category_path(self, category: str) -> Path:
        """Get the full path for a category"""
        base_path = Path(self.config["download_base_path"])
        category_folder = self.config["categories"].get(category, category)
        return base_path / category_folder

    def add_category(self, name: str, folder: str):
        """Add a new category"""
        self.config["categories"][name] = folder
        self._ensure_directories()
        self.save_config()


class URLValidator:
    """Validates YouTube URLs"""

    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
        r'(?:https?://)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
    ]

    @classmethod
    def is_valid_youtube_url(cls, url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        url = url.strip()
        # Filter out Mix/Radio playlists
        if '&start_radio=' in url or '&list=RD' in url:
            return False
        return any(re.match(pattern, url) for pattern in cls.YOUTUBE_PATTERNS)

    @classmethod
    def is_playlist(cls, url: str) -> bool:
        """Check if URL is a YouTube playlist"""
        return 'playlist?list=' in url and '&start_radio=' not in url

    @classmethod
    def clean_url(cls, url: str) -> str:
        """Clean URL and remove unwanted parameters"""
        url = url.strip()
        # Remove radio/mix playlist parameters
        url = re.sub(r'&start_radio=\d+', '', url)
        url = re.sub(r'&list=RD[\w-]+', '', url)
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """Extract all valid YouTube URLs from text"""
        lines = text.strip().split('\n')
        urls = []
        for line in lines:
            line = line.strip()
            if line and cls.is_valid_youtube_url(line):
                urls.append(cls.clean_url(line))
        return urls


class VideoInfo:
    """Container for video information"""
    def __init__(self, url: str, title: str = "", thumbnail_url: str = "",
                 duration: int = 0, is_playlist: bool = False, playlist_count: int = 0):
        self.url = url
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.duration = duration
        self.is_playlist = is_playlist
        self.playlist_count = playlist_count


class DownloadManager:
    """Manages YouTube downloads using yt-dlp"""

    QUALITY_FORMATS = {
        "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best",
        "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
        "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "Best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    }

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.current_download = None
        self.is_downloading = False
        self.cancel_requested = False
        self.download_thread = None

    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if 'entries' in info:
                    # Playlist
                    return VideoInfo(
                        url=url,
                        title=info.get('title', 'Playlist'),
                        thumbnail_url=info.get('thumbnail', ''),
                        is_playlist=True,
                        playlist_count=len(list(info['entries']))
                    )
                else:
                    # Single video
                    return VideoInfo(
                        url=url,
                        title=info.get('title', 'Unknown'),
                        thumbnail_url=info.get('thumbnail', ''),
                        duration=info.get('duration', 0),
                        is_playlist=False
                    )
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def cancel_download(self):
        """Cancel the current download"""
        self.cancel_requested = True

    def download(
        self,
        url: str,
        category: str,
        quality: str = "720p",
        progress_callback: Optional[Callable] = None,
        completion_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        info_callback: Optional[Callable] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ):
        """Download video(s) from YouTube"""

        def download_thread():
            try:
                self.is_downloading = True
                self.cancel_requested = False
                download_path = self.config_manager.get_category_path(category)

                # Get quality format string
                format_str = self.QUALITY_FORMATS.get(quality, self.QUALITY_FORMATS["720p"])

                # Configure yt-dlp options
                ydl_opts = {
                    'format': format_str,
                    'outtmpl': str(download_path / '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'writethumbnail': True,  # Download thumbnail
                    'postprocessors': [
                        {
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        },
                        {
                            'key': 'EmbedThumbnail',  # Embed thumbnail in video
                        }
                    ],
                    'progress_hooks': [self._create_progress_hook(progress_callback, info_callback)],
                    'quiet': False,
                    'no_warnings': False,
                }

                # Add time segment options if provided
                if start_time or end_time:
                    postprocessor_args = []
                    if start_time:
                        postprocessor_args.extend(['-ss', start_time])
                    if end_time:
                        postprocessor_args.extend(['-to', end_time])

                    if postprocessor_args:
                        ydl_opts['postprocessor_args'] = {
                            'ffmpeg': postprocessor_args
                        }

                # Download the video(s)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Check for cancellation
                    if self.cancel_requested:
                        if error_callback:
                            error_callback("Download cancelled")
                        return

                    info = ydl.extract_info(url, download=True)

                    # Get downloaded file info
                    if 'entries' in info:
                        # Playlist
                        video_count = len([e for e in info['entries'] if e])
                        result_msg = f"✓ Downloaded {video_count} videos to {category}"
                    else:
                        # Single video
                        result_msg = f"✓ Downloaded: {info.get('title', 'video')} to {category}"

                    if completion_callback and not self.cancel_requested:
                        completion_callback(result_msg)

            except Exception as e:
                if not self.cancel_requested:
                    error_msg = f"Download failed: {str(e)}"
                    if error_callback:
                        error_callback(error_msg)

            finally:
                self.is_downloading = False
                self.cancel_requested = False

        # Start download in separate thread
        self.download_thread = threading.Thread(target=download_thread, daemon=True)
        self.download_thread.start()

    def _create_progress_hook(self, progress_callback: Optional[Callable],
                             info_callback: Optional[Callable]):
        """Create a progress hook for yt-dlp"""
        def hook(d):
            if self.cancel_requested:
                raise Exception("Download cancelled by user")

            if d['status'] == 'downloading':
                try:
                    # Send current video info
                    if info_callback:
                        filename = d.get('filename', '')
                        if filename:
                            title = Path(filename).stem
                            info_callback(title)

                    if progress_callback:
                        downloaded = d.get('downloaded_bytes', 0)
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                        if total > 0:
                            percentage = (downloaded / total) * 100
                            speed = d.get('speed', 0)
                            eta = d.get('eta', 0)

                            # Format speed
                            speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"

                            # Format ETA
                            eta_str = f"{eta}s" if eta else "N/A"

                            progress_callback(percentage, speed_str, eta_str)
                except:
                    pass
            elif d['status'] == 'finished':
                if progress_callback:
                    progress_callback(100, "Processing...", "")

        return hook
