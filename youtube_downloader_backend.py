"""
YouTube Downloader Backend
Core functionality without GUI dependencies
"""

import yt_dlp
import json
import re
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime


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
        return any(re.match(pattern, url) for pattern in cls.YOUTUBE_PATTERNS)

    @classmethod
    def is_playlist(cls, url: str) -> bool:
        """Check if URL is a YouTube playlist"""
        return 'playlist?list=' in url


class DownloadManager:
    """Manages YouTube downloads using yt-dlp"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.current_download = None
        self.is_downloading = False

    def download(
        self,
        url: str,
        category: str,
        progress_callback: Optional[Callable] = None,
        completion_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ):
        """Download video(s) from YouTube"""

        def download_thread():
            try:
                self.is_downloading = True
                download_path = self.config_manager.get_category_path(category)

                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
                    'outtmpl': str(download_path / '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'progress_hooks': [self._create_progress_hook(progress_callback)],
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
                    info = ydl.extract_info(url, download=True)

                    # Get downloaded file info
                    if 'entries' in info:
                        # Playlist
                        video_count = len(info['entries'])
                        result_msg = f"✓ Downloaded {video_count} videos to {category}"
                    else:
                        # Single video
                        result_msg = f"✓ Downloaded: {info.get('title', 'video')} to {category}"

                    if completion_callback:
                        completion_callback(result_msg)

            except Exception as e:
                error_msg = f"Download failed: {str(e)}"
                if error_callback:
                    error_callback(error_msg)

            finally:
                self.is_downloading = False

        # Start download in separate thread
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()

    def _create_progress_hook(self, callback: Optional[Callable]):
        """Create a progress hook for yt-dlp"""
        def hook(d):
            if callback and d['status'] == 'downloading':
                try:
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

                        callback(percentage, speed_str, eta_str)
                except:
                    pass
            elif callback and d['status'] == 'finished':
                callback(100, "Processing...", "")

        return hook
