# 🎥 YouTube Downloader Bot

یک ربات تلگرام حرفه‌ای برای دانلود فیلم‌ها و آهنگ‌های یوتیوب

---

## 🌟 ویژگی‌ها

- ✅ دانلود ویدیو‌های یوتیوب با کیفیت بالا
- ✅ دانلود آهنگ (فقط صدا)
- ✅ انتخاب کیفیت دلخواه
- ✅ دانلود لیست پخش
- ✅ رابط کاربری ساده و سریع
- ✅ پشتیبانی از چندین زبان
- ✅ مدیریت دانلود‌های همزمان

---

## 📋 پیش‌نیازها

- Python 3.8+
- pip (مدیر بسته Python)
- Token ربات تلگرام
- اتصال اینترنت

---

## 🚀 نصب و راه‌اندازی

### 1. کلون کردن رپوزیتوری

```bash
git clone https://github.com/rebowijuco150-sys/YouTube-downloader.git
cd YouTube-downloader
```

### 2. ایجاد محیط مجازی

```bash
python -m venv venv
source venv/bin/activate  # در Linux/Mac
# یا
venv\Scripts\activate  # در Windows
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 4. تنظیم متغیرهای محیط

یک فایل `.env` ایجاد کنید:

```env
TELEGRAM_TOKEN=your_bot_token_here
DOWNLOAD_PATH=./downloads
```

### 5. اجرای ربات

```bash
python main.py
```

---

## 📦 وابستگی‌های مورد نیاز

```
python-telegram-bot==20.0
yt-dlp==2023.11.16
requests==2.31.0
python-dotenv==1.0.0
```

---

## 💻 نحوه استفاده

### روی تلگرام:

1. ربات را شروع کنید: `/start`
2. یک لینک یوتیوب را ارسال کنید
3. کیفیت دلخواه را ان��خاب کنید
4. منتظر دانلود باشید
5. فایل آماده دریافت است! 📥

### دستورات:

```
/start - شروع ربات
/help - کمک و راهنمایی
/download <URL> - دانلود ویدیو
/audio <URL> - دانلود فقط صدا
/playlist <URL> - دانلود لیست پخش
/status - وضعیت دانلود
```

---

## 🔧 تنظیمات

فایل `config.py`:

```python
# کیفیت‌های دستیاب
QUALITIES = ['720p', '480p', '360p', '240p']

# اندازه‌ی حداکثر فایل
MAX_FILE_SIZE = 2000  # MB

# تایم‌اوت دانلود
DOWNLOAD_TIMEOUT = 300  # ثانیه
```

---

## 📁 ساختار پروژه

```
YouTube-downloader/
├── main.py                 # فایل اصلی ربات
├── config.py              # تنظیمات
├── downloader.py          # منطق دانلود
├── handlers.py            # کنترل‌کننده‌های تلگرام
├── requirements.txt       # وابستگی‌ها
├── .env.example          # نمونه متغیرهای محیط
└── README.md             # این فایل
```

---

## 🔐 امنیت

- ✅ توکن ربات در فایل `.env` ذخیره شود (هرگز در کد نیست)
- ✅ حذف خودکار فایل‌های دانلود شده پس از 24 ساعت
- ✅ محدودیت سرعت برای جلوگیری از سوء استفاده
- ✅ بررسی نامعتبر بودن لینک‌های یوتیوب

---

## 🐛 حل مشکلات

### مشکل: خطای "Invalid Token"
**حل**: توکن خود را در فایل `.env` بررسی کنید

### مشکل: ویدیو دانلود نمی‌شود
**حل**: اتصال اینترنت را بررسی کنید یا yt-dlp را بروزرسانی کنید:
```bash
pip install --upgrade yt-dlp
```

### مشکل: خطای حافظه
**حل**: فایل‌های دانلود‌شده را پاک کنید یا `MAX_FILE_SIZE` را کاهش دهید

---

## 📊 آمار و درخواست‌های API

ربات از API‌های زیر استفاده می‌کند:
- **Telegram Bot API** - برای ارتباط با تلگرام
- **YouTube** - برای دریافت اطلاعات ویدیو
- **yt-dlp** - برای دانلود ویدیو

---

## 🤝 مشارکت

اگر می‌خواهید کمک کنید:

1. این رپوزیتوری را Fork کنید
2. یک شاخه جدید ایجاد کنید: `git checkout -b feature/amazing-feature`
3. تغییرات را Commit کنید: `git commit -m 'Add amazing feature'`
4. Push کنید: `git push origin feature/amazing-feature`
5. یک Pull Request باز کنید

---

## 📄 مجوز

این پروژه تحت مجوز **MIT License** منتشر شده است.

---

## 📞 تماس و پشتیبانی

- **مسائل**: [GitHub Issues](https://github.com/rebowijuco150-sys/YouTube-downloader/issues)
- **پیشنهادات**: [GitHub Discussions](https://github.com/rebowijuco150-sys/YouTube-downloader/discussions)

---

## ⭐ اگر این پروژه برایتان مفید بود، ستاره بدهید!

```
https://github.com/rebowijuco150-sys/YouTube-downloader
```

---

**ساخته شده با ❤️ توسط [rebowijuco150-sys](https://github.com/rebowijuco150-sys)**
