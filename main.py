import os
import yt_dlp
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- نظام البقاء مستيقظاً (Flask) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running with Cookie Support! ✅"

def run():
    # تأكد أن المنفذ هنا يطابق المنفذ في Koyeb (8080)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
TOKEN = "7257387654:AAG5FnKHZn4sVCvNg5_BQxmbhJ8eRqafeWs"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return
    
    msg = await update.message.reply_text("جاري التحليل والتحميل باستخدام 'نظام الهوية'... ⏳")
    video_filename = f"vid_{update.message.message_id}.mp4"
    
    # إعدادات yt-dlp المتقدمة مع دعم الكوكيز
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': video_filename,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # التحقق من وجود ملف الكوكيز في المستودع
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("✅ تم العثور على ملف الكوكيز واستخدامه.")
    else:
        print("⚠️ لم يتم العثور على cookies.txt، سيتم التحميل كزائر.")

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        if os.path.exists(video_filename):
            with open(video_filename, 'rb') as video:
                await update.message.reply_video(video)
        else:
            await msg.edit_text("تعذر العثور على الفيديو. تأكد أن الرابط متاح للعامة.")
            
    except Exception as e:
        error_msg = str(e)
        if "sign in" in error_msg.lower() or "login required" in error_msg.lower():
            await msg.edit_text("❌ الموقع يطلب تسجيل دخول. يرجى تحديث ملف cookies.txt.")
        else:
            await msg.edit_text(f"حدث خطأ: {error_msg}")
            
    finally:
        if os.path.exists(video_filename):
            os.remove(video_filename)
        try:
            await msg.delete()
        except:
            pass

if __name__ == '__main__':
    print("🚀 بدء تشغيل البوت بنظام الكوكيز...")
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    application.run_polling()
