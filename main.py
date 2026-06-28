#!/usr/bin/env python3
"""
ربات دانلود یوتیوب - فایل اصلی
"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import TELEGRAM_TOKEN
from handlers import (
    start,
    help_command,
    handle_url,
    quality_callback,
    status,
    error_handler,
)

# تنظیم logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """
    تابع اصلی برای اجرای ربات
    """
    # ایجاد اپلیکیشن
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # اضافه کردن handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('status', status))

    # handler برای URL‌های دریافتی
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_url
    ))

    # handler برای دکمه‌های inline
    app.add_handler(CallbackQueryHandler(quality_callback, pattern='^quality_'))

    # error handler
    app.add_error_handler(error_handler)

    # شروع ربات
    logger.info("🚀 ربات شروع شد...")
    print("""
    ╔════════════════════════════════════════════╗
    ║     YouTube Downloader Bot شروع شد       ║
    ║                                            ║
    ║  🎥 ربات دانلود ویدیو یوتیوب             ║
    ║  ✅ آماده برای دریافت درخواست‌ها        ║
    ║                                            ║
    ║  برای توقف: Ctrl + C                     ║
    ╚════════════════════════════════════════════╝
    """)

    app.run_polling(allowed_updates=['message', 'callback_query'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 ربات توقف یافت")
        print("\n\n✅ ربات با موفقیت متوقف شد")
    except Exception as e:
        logger.error(f"❌ خطای کلی: {e}")
        print(f"\n❌ خطا: {e}")
