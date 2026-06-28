"""
ربات تلگرام برای Cloudflare Worker - Webhook Version
فایل اصلی برای استفاده با Workers
"""

import json
import logging
from typing import Dict, Any
from telegram import Update
from telegram.ext import Application
from handlers import handle_update
from config import TELEGRAM_TOKEN

logger = logging.getLogger(__name__)

# ایجاد اپلیکیشن تک‌بار
app = None


async def initialize_app():
    """
    اولین‌بار اپلیکیشن را ایجاد کن
    """
    global app
    if app is None:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
    return app


async def handle_webhook(request_body: Dict[str, Any]) -> Dict[str, Any]:
    """
    مدیریت Webhook درخواست‌های تلگرام

    Args:
        request_body: بدنه درخواست از تلگرام

    Returns:
        جواب JSON برای تلگرام
    """
    try:
        # تبدیل درخواست به Update
        update = Update.de_json(request_body, app.bot)

        if update is None:
            logger.warning("Update نامعتبر دریافت شد")
            return {"ok": False, "error": "Invalid update"}

        logger.info(f"Update دریافت شد: {update.update_id}")

        # مدیریت Update
        result = await handle_update(update)

        return {"ok": True, "result": result}

    except Exception as e:
        logger.error(f"خطا در Webhook: {e}", exc_info=True)
        return {"ok": False, "error": str(e)}


async def set_webhook(webhook_url: str, secret_token: str) -> bool:
    """
    Webhook را تنظیم کن

    Args:
        webhook_url: آدرس Webhook (مثلاً https://example.com/webhook)
        secret_token: رمز محرمانه برای تایید

    Returns:
        True اگر موفق باشد
    """
    try:
        await app.bot.set_webhook(
            url=webhook_url,
            secret_token=secret_token,
            allowed_updates=['message', 'callback_query', 'inline_query']
        )
        logger.info(f"✅ Webhook تنظیم شد: {webhook_url}")
        return True
    except Exception as e:
        logger.error(f"خطا در تنظیم Webhook: {e}")
        return False


async def delete_webhook() -> bool:
    """
    Webhook را حذف کن

    Returns:
        True اگر موفق باشد
    """
    try:
        await app.bot.delete_webhook()
        logger.info("✅ Webhook حذف شد")
        return True
    except Exception as e:
        logger.error(f"خطا در حذف Webhook: {e}")
        return False


async def get_webhook_info() -> Dict[str, Any]:
    """
    اطلاعات Webhook را دریافت کن

    Returns:
        فرهنگ اطلاعات Webhook
    """
    try:
        webhook_info = await app.bot.get_webhook_info()
        return webhook_info.to_dict()
    except Exception as e:
        logger.error(f"خطا در دریافت اطلاعات Webhook: {e}")
        return {}
