"""
ماژول دانلود یوتیوب
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import yt_dlp
from config import (
    DOWNLOAD_PATH,
    MAX_FILE_SIZE,
    DOWNLOAD_TIMEOUT,
    AUDIO_FORMAT,
    VIDEO_FORMAT,
)

logger = logging.getLogger(__name__)


class YouTubeDownloader:
    """کلاس برای دانلود ویدیو‌های یوتیوب"""

    def __init__(self):
        self.download_path = Path(DOWNLOAD_PATH)
        self.download_path.mkdir(parents=True, exist_ok=True)

    def is_valid_youtube_url(self, url: str) -> bool:
        """
        بررسی معتبر بودن URL یوتیوب

        Args:
            url: آدرس یوتیوب

        Returns:
            True اگر معتبر باشد، False در غیر اینصورت
        """
        youtube_domains = [
            'youtube.com',
            'youtu.be',
            'youtube-nocookie.com',
        ]
        return any(domain in url.lower() for domain in youtube_domains)

    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        دریافت اطلاعات ویدیو

        Args:
            url: آدرس یوتیوب

        Returns:
            فرهنگ اطلاعات ویدیو یا None در صورت خطا
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': DOWNLOAD_TIMEOUT,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'is_playlist': 'entries' in info,
                    'entries_count': len(info.get('entries', [])),
                }
        except Exception as e:
            logger.error(f"خطا در دریافت اطلاعات: {e}")
            return None

    def download_video(
        self,
        url: str,
        quality: str = '720p',
        progress_hook=None
    ) -> Optional[str]:
        """
        دانلود ویدیو یوتیوب

        Args:
            url: آدرس یوتیوب
            quality: کیفیت دلخواه (مثلاً '720p')
            progress_hook: تابع برای نمایش پیشرفت

        Returns:
            مسیر فایل دانلود‌شده یا None در صورت خطا
        """
        try:
            # استخراج عدد کیفیت
            quality_num = quality.replace('p', '')

            ydl_opts = {
                'format': f'best[height<={quality_num}]/best',
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': DOWNLOAD_TIMEOUT,
                'http_chunk_size': 10485760,  # 10MB chunks
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': VIDEO_FORMAT,
                    }
                ],
            }

            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"شروع دانلود: {url} - کیفیت: {quality}")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # بررسی اندازه فایل
                if os.path.exists(filename):
                    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
                    if file_size_mb > MAX_FILE_SIZE:
                        os.remove(filename)
                        logger.warning(f"فایل بیش از حد بزرگ: {file_size_mb}MB")
                        return None

                logger.info(f"دانلود موفق: {filename}")
                return filename

        except Exception as e:
            logger.error(f"خطا در دانلود ویدیو: {e}")
            return None

    def download_audio(self, url: str, progress_hook=None) -> Optional[str]:
        """
        دانلود صدای ویدیو یوتیوب

        Args:
            url: آدرس یوتیوب
            progress_hook: تابع برای نمایش پیشرفت

        Returns:
            مسیر فایل دانلود‌شده یا None در صورت خطا
        """
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': DOWNLOAD_TIMEOUT,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'audio_format': AUDIO_FORMAT,
                        'audio_quality': '192',
                    }
                ],
            }

            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"شروع دانلود صدا: {url}")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                logger.info(f"دانلود صدا موفق: {filename}")
                return filename

        except Exception as e:
            logger.error(f"خطا در دانلود صدا: {e}")
            return None

    def cleanup_old_files(self, hours: int = 24):
        """
        حذف فایل‌های قدیمی

        Args:
            hours: حذف فایل‌های بیشتر از این ساعت
        """
        import time
        current_time = time.time()
        cutoff_time = current_time - (hours * 3600)

        for filepath in self.download_path.glob('*'):
            if filepath.is_file():
                if os.path.getmtime(filepath) < cutoff_time:
                    try:
                        os.remove(filepath)
                        logger.info(f"فایل قدیمی حذف شد: {filepath}")
                    except Exception as e:
                        logger.error(f"خطا در حذف فایل: {e}")

    def get_file_size_mb(self, filepath: str) -> float:
        """
        دریافت اندازه فایل به مگابایت

        Args:
            filepath: مسیر فایل

        Returns:
            اندازه فایل به مگابایت
        """
        if os.path.exists(filepath):
            return os.path.getsize(filepath) / (1024 * 1024)
        return 0.0


# ایجاد نمونه global
downloader = YouTubeDownloader()
