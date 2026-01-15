import os
import yt_dlp
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- 1. نظام Flask للبقاء مستيقظاً على منفذ 8080 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running! Port: 8080 ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. إعدادات البوت والتحميل ---
TOKEN = "7257387654:AAG5FnKHZn4sVCvNg5_BQxmbhJ8eRqafeWs"

async def download_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return
    
    status_msg = await update.message.reply_text("جاري فحص الرابط وتحميل المحتوى (فيديو/صور)... ⏳")
    
    # إعدادات yt-dlp لدعم الصور والفيديو والألبومات
    ydl_opts = {
        'format': 'best', # يختار أفضل جودة متاحة (سواء صورة أو فيديو)
        'outtmpl': f'down_{update.message.message_id}_%(tag)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.instagram.com/',
        'writethumbnail': True, # مهم لدعم الصور
    }

    # تفعيل الكوكيز تلقائياً إذا كان الملف موجوداً في GitHub
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("✅ تم تفعيل نظام الهوية (Cookies).")

    try:
        loop = asyncio.get_event_loop()
        # استخراج معلومات الرابط أولاً
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
        
        # البحث عن الملفات المحملة في المجلد الحالي
        files = [f for f in os.listdir('.') if f.startswith(f'down_{update.message.message_id}')]
        
        if not files:
            await status_msg.edit_text("❌ فشل التحميل. يرجى التأكد من تحديث ملف cookies.txt للحساب الوهمي.")
            return

        for file in files:
            with open(file, 'rb') as f:
                if file.endswith(('.mp4', '.mov', '.mkv')):
                    await update.message.reply_video(f)
                else:
                    await update.message.reply_photo(f)
            os.remove(file) # حذف الملف فوراً لتوفير المساحة

        await status_msg.delete()

    except Exception as e:
        error_text = str(e)
        if "login required" in error_text.lower() or "rate-limit" in error_text.lower():
            await status_msg.edit_text("❌ إنستغرام يطلب تسجيل دخول لرؤية هذا المحتوى. يرجى تحديث الكوكيز.")
        else:
            await status_msg.edit_text(f"حدث خطأ: {error_text[:100]}")
            
    finally:
        # تنظيف أي ملفات متبقية في حال حدوث خطأ
        for f in os.listdir('.'):
            if f.startswith(f'down_{update.message.message_id}'):
                os.remove(f)

if __name__ == '__main__':
    print("🚀 البوت انطلق...")
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_content))
    application.run_polling()
