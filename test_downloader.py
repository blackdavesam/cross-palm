#!/usr/bin/env python3
"""
Test script for YouTube Downloader backend functionality
Tests without GUI in headless environment
"""

import sys
import json
from pathlib import Path

# Import classes from backend module
sys.path.insert(0, str(Path(__file__).parent))
from youtube_downloader_backend import ConfigManager, URLValidator, DownloadManager


def test_config_manager():
    """Test ConfigManager functionality"""
    print("Testing ConfigManager...")

    # Create test config
    config_path = "test_config.json"
    config = ConfigManager(config_path)

    # Verify default config loaded
    assert "download_base_path" in config.config
    assert "categories" in config.config
    assert len(config.config["categories"]) == 6

    # Test category path generation
    history_path = config.get_category_path("History")
    assert "History" in str(history_path)

    # Test adding custom category
    config.add_category("Test Category", "TestFolder")
    assert "Test Category" in config.config["categories"]

    # Clean up
    Path(config_path).unlink(missing_ok=True)

    print("✓ ConfigManager tests passed")


def test_url_validator():
    """Test URLValidator functionality"""
    print("\nTesting URLValidator...")

    # Valid YouTube URLs
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
        "https://www.youtube.com/shorts/abc123",
        "www.youtube.com/watch?v=test123",
    ]

    for url in valid_urls:
        assert URLValidator.is_valid_youtube_url(url), f"Failed to validate: {url}"

    # Invalid URLs
    invalid_urls = [
        "https://vimeo.com/123456",
        "https://dailymotion.com/video/xyz",
        "not a url",
        "",
        "https://google.com"
    ]

    for url in invalid_urls:
        assert not URLValidator.is_valid_youtube_url(url), f"Incorrectly validated: {url}"

    # Test playlist detection
    assert URLValidator.is_playlist("https://www.youtube.com/playlist?list=PLtest")
    assert not URLValidator.is_playlist("https://www.youtube.com/watch?v=test")

    print("✓ URLValidator tests passed")


def test_download_manager():
    """Test DownloadManager initialization"""
    print("\nTesting DownloadManager...")

    config = ConfigManager("test_config.json")
    manager = DownloadManager(config)

    assert manager.config_manager is not None
    assert manager.is_downloading == False

    # Clean up
    Path("test_config.json").unlink(missing_ok=True)

    print("✓ DownloadManager initialization passed")


def test_config_persistence():
    """Test config file persistence"""
    print("\nTesting config persistence...")

    config_path = "test_persistence.json"

    # Create and save config
    config1 = ConfigManager(config_path)
    config1.config["default_category"] = "Music"
    config1.save_config()

    # Load config in new instance
    config2 = ConfigManager(config_path)
    assert config2.config["default_category"] == "Music"

    # Clean up
    Path(config_path).unlink(missing_ok=True)

    print("✓ Config persistence tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("YouTube Downloader Backend Tests")
    print("=" * 60)

    try:
        test_config_manager()
        test_url_validator()
        test_download_manager()
        test_config_persistence()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
