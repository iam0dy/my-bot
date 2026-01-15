import os
import yt_dlp
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- نظام البقاء حياً ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "I am alive!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- التوكن الخاص بك ---
TOKEN = "7257387654:AAG5FnKHZn4sVCvNg5_BQxmbhJ8eRqafeWs"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return
    
    msg = await update.message.reply_text("جاري المعالجة... ⏳")
    video_filename = f"vid_{update.message.message_id}.mp4"
    
    # إعدادات متقدمة لتجاوز الحظر بدون كوكيز
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': video_filename,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        if os.path.exists(video_filename):
            with open(video_filename, 'rb') as video:
                await update.message.reply_video(video)
        else:
            await msg.edit_text("تعذر تحميل الفيديو، قد يكون الرابط خاصاً أو محمياً.")
            
    except Exception as e:
        await msg.edit_text(f"عذراً، واجه السيرفر قيوداً من الموقع. خطأ: {str(e)}")
    finally:
        # مسح الملف فوراً (نظام الممر)
        if os.path.exists(video_filename): 
            os.remove(video_filename)
        try:
            await msg.delete()
        except: pass

if __name__ == '__main__':
    print("🚀 البوت يعمل الآن...")
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
