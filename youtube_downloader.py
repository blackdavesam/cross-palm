#!/usr/bin/env python3
"""
YouTube Downloader GUI
A modern, lightweight YouTube downloader with category-based organization
Built with CustomTkinter and yt-dlp
"""

import customtkinter as ctk
from pathlib import Path
from datetime import datetime
import sys
import re

# Import backend functionality
from youtube_downloader_backend import ConfigManager, URLValidator, DownloadManager


class YouTubeDownloaderGUI:
    """Main GUI Application"""

    def __init__(self):
        # Initialize managers
        self.config_manager = ConfigManager()
        self.download_manager = DownloadManager(self.config_manager)

        # Set CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader")
        self.root.geometry("800x700")

        # Initialize UI
        self._create_ui()

    def _create_ui(self):
        """Create the user interface"""

        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="YouTube Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # URL Input Section
        url_frame = ctk.CTkFrame(main_frame)
        url_frame.pack(fill="x", pady=(0, 15))

        url_label = ctk.CTkLabel(url_frame, text="YouTube URL:", font=ctk.CTkFont(size=14))
        url_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            height=40
        )
        self.url_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Category Selection
        category_frame = ctk.CTkFrame(main_frame)
        category_frame.pack(fill="x", pady=(0, 15))

        category_label = ctk.CTkLabel(category_frame, text="Category:", font=ctk.CTkFont(size=14))
        category_label.pack(anchor="w", padx=10, pady=(10, 5))

        categories = list(self.config_manager.config["categories"].keys())
        self.category_var = ctk.StringVar(value=self.config_manager.config["default_category"])

        self.category_dropdown = ctk.CTkOptionMenu(
            category_frame,
            variable=self.category_var,
            values=categories,
            height=40
        )
        self.category_dropdown.pack(fill="x", padx=10, pady=(0, 10))

        # Time Segment Section (Optional)
        segment_frame = ctk.CTkFrame(main_frame)
        segment_frame.pack(fill="x", pady=(0, 15))

        segment_label = ctk.CTkLabel(
            segment_frame,
            text="Time Segment (Optional):",
            font=ctk.CTkFont(size=14)
        )
        segment_label.pack(anchor="w", padx=10, pady=(10, 5))

        time_inputs_frame = ctk.CTkFrame(segment_frame, fg_color="transparent")
        time_inputs_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Start time
        start_frame = ctk.CTkFrame(time_inputs_frame, fg_color="transparent")
        start_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))

        start_label = ctk.CTkLabel(start_frame, text="Start (HH:MM:SS):", font=ctk.CTkFont(size=12))
        start_label.pack(anchor="w")

        self.start_time_entry = ctk.CTkEntry(
            start_frame,
            placeholder_text="00:00:30",
            height=35
        )
        self.start_time_entry.pack(fill="x", pady=(5, 0))

        # End time
        end_frame = ctk.CTkFrame(time_inputs_frame, fg_color="transparent")
        end_frame.pack(side="left", expand=True, fill="x", padx=(5, 0))

        end_label = ctk.CTkLabel(end_frame, text="End (HH:MM:SS):", font=ctk.CTkFont(size=12))
        end_label.pack(anchor="w")

        self.end_time_entry = ctk.CTkEntry(
            end_frame,
            placeholder_text="00:05:00",
            height=35
        )
        self.end_time_entry.pack(fill="x", pady=(5, 0))

        # Download Button
        self.download_btn = ctk.CTkButton(
            main_frame,
            text="Download",
            command=self._start_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.download_btn.pack(fill="x", pady=(0, 15))

        # Progress Section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=(0, 15))

        progress_label = ctk.CTkLabel(progress_frame, text="Progress:", font=ctk.CTkFont(size=14))
        progress_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(padx=10, pady=(0, 10))

        # Status/Log Section
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="both", expand=True)

        status_label = ctk.CTkLabel(status_frame, text="Status:", font=ctk.CTkFont(size=14))
        status_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.status_text = ctk.CTkTextbox(status_frame, height=150)
        self.status_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._log("Welcome to YouTube Downloader!")
        self._log(f"Downloads will be saved to: {self.config_manager.config['download_base_path']}")

    def _log(self, message: str):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert("end", f"[{timestamp}] {message}\n")
        self.status_text.see("end")

    def _update_progress(self, percentage: float, speed: str, eta: str):
        """Update progress bar and label"""
        self.progress_bar.set(percentage / 100)
        self.progress_label.configure(text=f"{percentage:.1f}% - Speed: {speed} - ETA: {eta}")

    def _start_download(self):
        """Start the download process"""
        url = self.url_entry.get().strip()

        # Validate URL
        if not url:
            self._log("❌ Error: Please enter a URL")
            return

        if not URLValidator.is_valid_youtube_url(url):
            self._log("❌ Error: Please enter a valid YouTube URL")
            self._log("   Supported: youtube.com/watch, youtu.be, playlists, shorts")
            return

        if self.download_manager.is_downloading:
            self._log("❌ Download already in progress")
            return

        # Get parameters
        category = self.category_var.get()
        start_time = self.start_time_entry.get().strip() or None
        end_time = self.end_time_entry.get().strip() or None

        # Validate time format if provided
        time_pattern = r'^\d{1,2}:\d{2}:\d{2}$'
        if start_time and not re.match(time_pattern, start_time):
            self._log("❌ Error: Invalid start time format. Use HH:MM:SS")
            return
        if end_time and not re.match(time_pattern, end_time):
            self._log("❌ Error: Invalid end time format. Use HH:MM:SS")
            return

        # Log download start
        self._log(f"⬇️ Starting download...")
        self._log(f"   URL: {url}")
        self._log(f"   Category: {category}")
        if start_time or end_time:
            segment_info = f"   Segment: {start_time or '00:00:00'} to {end_time or 'end'}"
            self._log(segment_info)

        if URLValidator.is_playlist(url):
            self._log("   📝 Playlist detected - downloading all videos")

        # Disable download button
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting download...")

        # Start download
        self.download_manager.download(
            url=url,
            category=category,
            progress_callback=self._update_progress,
            completion_callback=self._on_download_complete,
            error_callback=self._on_download_error,
            start_time=start_time,
            end_time=end_time
        )

    def _on_download_complete(self, message: str):
        """Handle download completion"""
        self._log(message)
        self.download_btn.configure(state="normal", text="Download")
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="Download complete!")

        # Clear URL entry for next download
        self.url_entry.delete(0, "end")

    def _on_download_error(self, message: str):
        """Handle download error"""
        self._log(f"❌ {message}")
        self.download_btn.configure(state="normal", text="Download")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Download failed")

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = YouTubeDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()
