#!/usr/bin/env python3
"""
YouTube Downloader GUI - Enhanced Version
A modern, feature-rich YouTube downloader with category-based organization
Built with CustomTkinter and yt-dlp
"""

import customtkinter as ctk
from pathlib import Path
from datetime import datetime
import sys
import re
import subprocess
import platform
from tkinter import messagebox
import threading

# Import backend functionality
from youtube_downloader_backend import ConfigManager, URLValidator, DownloadManager, VideoInfo


class PlaylistConfirmDialog(ctk.CTkToplevel):
    """Dialog to confirm playlist downloads"""

    def __init__(self, parent, video_info: VideoInfo):
        super().__init__(parent)

        self.result = False
        self.video_info = video_info

        # Configure window
        self.title("Playlist Detected")
        self.geometry("400x200")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # Content
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon and message
        title_label = ctk.CTkLabel(
            main_frame,
            text="📝 Playlist Detected",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        message_label = ctk.CTkLabel(
            main_frame,
            text=f"This playlist contains {video_info.playlist_count} videos.\n\n"
                 f"Playlist: {video_info.title[:50]}...\n\n"
                 f"Do you want to download all videos?",
            font=ctk.CTkFont(size=12)
        )
        message_label.pack(pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            fg_color="gray",
            width=120
        )
        cancel_btn.pack(side="left", expand=True, padx=5)

        download_btn = ctk.CTkButton(
            button_frame,
            text=f"Download All ({video_info.playlist_count})",
            command=self._on_download,
            width=180
        )
        download_btn.pack(side="right", expand=True, padx=5)

    def _on_cancel(self):
        self.result = False
        self.destroy()

    def _on_download(self):
        self.result = True
        self.destroy()


class YouTubeDownloaderGUI:
    """Main GUI Application - Enhanced Version"""

    def __init__(self):
        # Initialize managers
        self.config_manager = ConfigManager()
        self.download_manager = DownloadManager(self.config_manager)

        # Download queue
        self.download_queue = []
        self.current_video_title = ""

        # Set CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x800")

        # Initialize UI
        self._create_ui()

    def _create_ui(self):
        """Create the enhanced user interface"""

        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title with version
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = ctk.CTkLabel(
            header_frame,
            text="YouTube Downloader Pro",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(side="left")

        version_label = ctk.CTkLabel(
            header_frame,
            text="v2.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.pack(side="left", padx=(10, 0))

        # URL Input Section (now supports multiple URLs)
        url_frame = ctk.CTkFrame(main_frame)
        url_frame.pack(fill="both", expand=True, pady=(0, 15))

        url_header = ctk.CTkFrame(url_frame, fg_color="transparent")
        url_header.pack(fill="x", padx=10, pady=(10, 5))

        url_label = ctk.CTkLabel(
            url_header,
            text="YouTube URLs (one per line):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        url_label.pack(side="left")

        # Helper buttons
        paste_btn = ctk.CTkButton(
            url_header,
            text="📋 Paste",
            command=self._paste_urls,
            width=80,
            height=28
        )
        paste_btn.pack(side="right", padx=(5, 0))

        clear_btn = ctk.CTkButton(
            url_header,
            text="🗑️ Clear",
            command=self._clear_urls,
            width=80,
            height=28,
            fg_color="gray"
        )
        clear_btn.pack(side="right")

        # Textbox for multiple URLs
        self.url_textbox = ctk.CTkTextbox(
            url_frame,
            height=120,
            font=ctk.CTkFont(size=12)
        )
        self.url_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Settings Row: Category and Quality
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=(0, 15))

        # Category Selection (left side)
        category_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        category_container.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        category_label = ctk.CTkLabel(
            category_container,
            text="Category:",
            font=ctk.CTkFont(size=14)
        )
        category_label.pack(anchor="w", pady=(0, 5))

        categories = list(self.config_manager.config["categories"].keys())
        self.category_var = ctk.StringVar(value=self.config_manager.config["default_category"])

        self.category_dropdown = ctk.CTkOptionMenu(
            category_container,
            variable=self.category_var,
            values=categories,
            height=40
        )
        self.category_dropdown.pack(fill="x")

        # Quality Selection (right side)
        quality_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_container.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        quality_label = ctk.CTkLabel(
            quality_container,
            text="Quality:",
            font=ctk.CTkFont(size=14)
        )
        quality_label.pack(anchor="w", pady=(0, 5))

        self.quality_var = ctk.StringVar(value="720p")
        qualities = ["360p", "480p", "720p", "1080p", "Best"]

        self.quality_dropdown = ctk.CTkOptionMenu(
            quality_container,
            variable=self.quality_var,
            values=qualities,
            height=40
        )
        self.quality_dropdown.pack(fill="x")

        # Time Segment Section (Optional - Collapsible)
        segment_frame = ctk.CTkFrame(main_frame)
        segment_frame.pack(fill="x", pady=(0, 15))

        segment_label = ctk.CTkLabel(
            segment_frame,
            text="⏱️ Time Segment (Optional):",
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

        # Action Buttons Row
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))

        self.download_btn = ctk.CTkButton(
            action_frame,
            text="⬇️ Download",
            command=self._start_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.download_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.cancel_btn = ctk.CTkButton(
            action_frame,
            text="⏹️ Cancel",
            command=self._cancel_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.cancel_btn.pack(side="left", fill="x", expand=True, padx=(5, 5))

        self.open_folder_btn = ctk.CTkButton(
            action_frame,
            text="📁 Open Folder",
            command=self._open_download_folder,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="gray",
            hover_color="darkgray"
        )
        self.open_folder_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Current Download Info
        current_frame = ctk.CTkFrame(main_frame)
        current_frame.pack(fill="x", pady=(0, 15))

        current_label = ctk.CTkLabel(
            current_frame,
            text="Current Download:",
            font=ctk.CTkFont(size=14)
        )
        current_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.current_video_label = ctk.CTkLabel(
            current_frame,
            text="No active download",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.current_video_label.pack(anchor="w", padx=10, pady=(0, 5))

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

        status_header = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_header.pack(fill="x", padx=10, pady=(10, 5))

        status_label = ctk.CTkLabel(
            status_header,
            text="Activity Log:",
            font=ctk.CTkFont(size=14)
        )
        status_label.pack(side="left")

        clear_log_btn = ctk.CTkButton(
            status_header,
            text="Clear Log",
            command=self._clear_log,
            width=80,
            height=25,
            fg_color="gray"
        )
        clear_log_btn.pack(side="right")

        self.status_text = ctk.CTkTextbox(status_frame, height=150)
        self.status_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._log("✨ Welcome to YouTube Downloader Pro!")
        self._log(f"📁 Downloads location: {self.config_manager.config['download_base_path']}")
        self._log("💡 Tip: Paste multiple URLs (one per line) for batch downloads")

    def _log(self, message: str):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert("end", f"[{timestamp}] {message}\n")
        self.status_text.see("end")

    def _clear_log(self):
        """Clear the activity log"""
        self.status_text.delete("1.0", "end")
        self._log("📋 Log cleared")

    def _paste_urls(self):
        """Paste URLs from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_textbox.delete("1.0", "end")
            self.url_textbox.insert("1.0", clipboard_content)
            self._log("📋 URLs pasted from clipboard")
        except:
            self._log("❌ Could not paste from clipboard")

    def _clear_urls(self):
        """Clear URL textbox"""
        self.url_textbox.delete("1.0", "end")

    def _open_download_folder(self):
        """Open the downloads folder in file manager"""
        category = self.category_var.get()
        folder_path = self.config_manager.get_category_path(category)

        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(folder_path)])
            elif platform.system() == "Windows":
                subprocess.run(["explorer", str(folder_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(folder_path)])
            self._log(f"📁 Opened folder: {folder_path}")
        except Exception as e:
            self._log(f"❌ Could not open folder: {e}")

    def _update_progress(self, percentage: float, speed: str, eta: str):
        """Update progress bar and label"""
        self.progress_bar.set(percentage / 100)
        self.progress_label.configure(
            text=f"{percentage:.1f}% • Speed: {speed} • ETA: {eta}"
        )

    def _update_current_video(self, title: str):
        """Update current video title"""
        if title and title != self.current_video_title:
            self.current_video_title = title
            # Truncate long titles
            display_title = title[:80] + "..." if len(title) > 80 else title
            self.current_video_label.configure(
                text=f"⬇️ {display_title}",
                text_color="white"
            )

    def _start_download(self):
        """Start the download process"""
        urls_text = self.url_textbox.get("1.0", "end").strip()

        # Validate URLs
        if not urls_text:
            self._log("❌ Error: Please enter at least one URL")
            return

        urls = URLValidator.extract_urls(urls_text)

        if not urls:
            self._log("❌ Error: No valid YouTube URLs found")
            self._log("   Make sure URLs start with youtube.com or youtu.be")
            return

        if self.download_manager.is_downloading:
            self._log("❌ Download already in progress")
            return

        # Get parameters
        category = self.category_var.get()
        quality = self.quality_var.get()
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
        self._log(f"🔍 Found {len(urls)} URL(s) to download")
        self._log(f"📂 Category: {category} | 🎬 Quality: {quality}")

        # Check for playlists and confirm
        for url in urls:
            if URLValidator.is_playlist(url):
                # Get playlist info
                self._log(f"📝 Checking playlist info...")
                info = self.download_manager.get_video_info(url)

                if info and info.is_playlist:
                    # Show confirmation dialog
                    dialog = PlaylistConfirmDialog(self.root, info)
                    self.root.wait_window(dialog)

                    if not dialog.result:
                        self._log(f"❌ Playlist download cancelled by user")
                        return
                    else:
                        self._log(f"✓ Confirmed: Will download {info.playlist_count} videos from playlist")

        # Start downloads
        self.download_queue = urls.copy()
        self._process_next_download(category, quality, start_time, end_time)

    def _process_next_download(self, category, quality, start_time, end_time):
        """Process the next URL in the queue"""
        if not self.download_queue:
            self._log("✅ All downloads complete!")
            self.download_btn.configure(state="normal", text="⬇️ Download")
            self.cancel_btn.configure(state="disabled")
            self.current_video_label.configure(text="No active download", text_color="gray")
            return

        url = self.download_queue.pop(0)
        remaining = len(self.download_queue)

        if remaining > 0:
            self._log(f"⬇️ Starting download ({remaining} remaining in queue)...")
        else:
            self._log(f"⬇️ Starting download...")

        # Disable download button, enable cancel
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting download...")

        # Start download
        self.download_manager.download(
            url=url,
            category=category,
            quality=quality,
            progress_callback=self._update_progress,
            completion_callback=lambda msg: self._on_download_complete(
                msg, category, quality, start_time, end_time
            ),
            error_callback=lambda msg: self._on_download_error(
                msg, category, quality, start_time, end_time
            ),
            info_callback=self._update_current_video,
            start_time=start_time,
            end_time=end_time
        )

    def _on_download_complete(self, message: str, category, quality, start_time, end_time):
        """Handle download completion"""
        self._log(message)
        self.progress_bar.set(1.0)

        # Process next in queue
        if self.download_queue:
            self._process_next_download(category, quality, start_time, end_time)
        else:
            self.download_btn.configure(state="normal", text="⬇️ Download")
            self.cancel_btn.configure(state="disabled")
            self.current_video_label.configure(text="No active download", text_color="gray")
            self._log("🎉 All downloads finished!")

    def _on_download_error(self, message: str, category, quality, start_time, end_time):
        """Handle download error"""
        self._log(f"❌ {message}")

        # Continue with next in queue even if one fails
        if self.download_queue:
            self._process_next_download(category, quality, start_time, end_time)
        else:
            self.download_btn.configure(state="normal", text="⬇️ Download")
            self.cancel_btn.configure(state="disabled")
            self.progress_bar.set(0)
            self.progress_label.configure(text="Download failed")
            self.current_video_label.configure(text="No active download", text_color="gray")

    def _cancel_download(self):
        """Cancel current download"""
        if self.download_manager.is_downloading:
            self.download_manager.cancel_download()
            self.download_queue.clear()  # Clear queue
            self._log("🛑 Download cancelled by user")
            self.cancel_btn.configure(state="disabled")
            self.download_btn.configure(state="normal", text="⬇️ Download")
            self.current_video_label.configure(text="No active download", text_color="gray")

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = YouTubeDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()
