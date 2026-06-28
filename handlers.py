"""
مدیریت دستورات و پیام‌های تلگرام
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from downloader import downloader
from config import MESSAGES, QUALITIES

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    دستور /start
    """
    user = update.effective_user
    logger.info(f"کاربر {user.id} ربات را شروع کرد")

    await update.message.reply_text(
        MESSAGES['welcome'],
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    دستور /help
    """
    await update.message.reply_text(
        MESSAGES['help'],
        parse_mode='Markdown'
    )


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    مدیریت لینک‌های ارسالی
    """
    user = update.effective_user
    message_text = update.message.text
    user_id = user.id

    logger.info(f"کاربر {user_id} لینک ارسال کرد: {message_text}")

    # بررسی معتبر بودن URL
    if not downloader.is_valid_youtube_url(message_text):
        await update.message.reply_text(MESSAGES['invalid_url'])
        return

    # ذخیره URL و نوع دانلود
    context.user_data['current_url'] = message_text
    context.user_data['download_type'] = 'video'

    # دریافت اطلاعات ویدیو
    status_msg = await update.message.reply_text(MESSAGES['processing'])

    video_info = downloader.get_video_info(message_text)

    if not video_info:
        await status_msg.edit_text(MESSAGES['error'])
        return

    # نمایش اطلاعات ویدیو
    info_text = f"""
📺 **{video_info['title']}**

👤 **آپلودکننده:** {video_info['uploader']}
⏱ **مدت:** {format_duration(video_info['duration'])}
👁 **بازدید:** {format_number(video_info['view_count'])}
    """.strip()

    # ایجاد دکمه‌های کیفیت
    keyboard = []
    for quality_name in QUALITIES.keys():
        keyboard.append([
            InlineKeyboardButton(
                quality_name,
                callback_data=f"quality_{quality_name}"
            )
        ])

    # اضافه کردن دکمه صدا
    keyboard.append([
        InlineKeyboardButton("🎵 دانلود صدا", callback_data="quality_audio")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await status_msg.edit_text(
        info_text + '\n\n' + MESSAGES['select_quality'],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def quality_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    مدیریت انتخاب کیفیت
    """
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if 'current_url' not in context.user_data:
        await query.edit_message_text("❌ URL یافت نشد! لطفاً دوباره تلاش کنید.")
        return

    url = context.user_data['current_url']
    quality = query.data.replace('quality_', '')

    # نمایش پیام در حال دانلود
    processing_msg = await query.edit_message_text(MESSAGES['downloading'])

    try:
        if quality == 'audio':
            # دانلود صدا
            logger.info(f"کاربر {user_id} صدا دانلود می‌کند")
            filepath = downloader.download_audio(url)
        else:
            # دانلود ویدیو
            logger.info(f"کاربر {user_id} ویدیو با کیفیت {quality} دانلود می‌کند")
            filepath = downloader.download_video(url, quality)

        if filepath:
            # دانلود موفق
            file_size = downloader.get_file_size_mb(filepath)
            success_msg = f"{MESSAGES['success']}\n📦 اندازه: {file_size:.2f}MB"

            await processing_msg.edit_text(success_msg)

            # ارسال فایل
            logger.info(f"ارسال فایل به کاربر {user_id}")
            with open(filepath, 'rb') as file:
                if quality == 'audio':
                    await query.message.reply_audio(file)
                else:
                    await query.message.reply_video(file)

        else:
            # دانلود ناموفق
            await processing_msg.edit_text(MESSAGES['error'])
            logger.error(f"دانلود ناموفق برای کاربر {user_id}")

    except Exception as e:
        logger.error(f"خطا در دانلود: {e}")
        await processing_msg.edit_text(f"{MESSAGES['error']}\n\n❌ {str(e)}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    دستور /status
    """
    status_text = """
📊 **وضعیت سیستم:**

✅ ربات فعال است
✅ دانلودر آماده است
✅ اتصال برقرار است

برای شروع یک لینک یوتیوب ارسال کنید.
    """.strip()

    await update.message.reply_text(status_text, parse_mode='Markdown')


def format_duration(seconds: int) -> str:
    """
    تبدیل ثانیه به فرمت قابل خواندن

    Args:
        seconds: تعداد ثانیه

    Returns:
        فرمت شده مدت زمان
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_number(num: int) -> str:
    """
    تبدیل عدد به فرمت قابل خواندن

    Args:
        num: عدد

    Returns:
        فرمت شده عدد
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    مدیریت خطاهای کلی
    """
    logger.error(f"خطا: {context.error}")

    if update:
        try:
            await update.message.reply_text(
                "❌ خطایی رخ داد! لطفاً با مدیر تماس بگیرید."
            )
        except Exception as e:
            logger.error(f"نتوانست پیام خطا ارسال شود: {e}")
