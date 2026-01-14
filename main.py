import os
import yt_dlp
import asyncio
from flask import Flask # مكتبة جديدة سنثبتها
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- كود البقاء مستيقظاً ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "I am alive!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# -------------------------

TOKEN = "7257387654:AAG5FnKHZn4sVCvNg5_BQxmbhJ8eRqafeWs"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (نفس الكود السابق للتحميل)
    url = update.message.text
    if not url.startswith("http"): return
    msg = await update.message.reply_text("جاري التحميل من السيرفر السحابي... ⏳")
    video_filename = f"vid_{update.message.message_id}.mp4"
    try:
        ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': video_filename}
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        with open(video_filename, 'rb') as video:
            await update.message.reply_video(video)
    except Exception as e:
        await msg.edit_text(f"خطأ: {e}")
    finally:
        if os.path.exists(video_filename): os.remove(video_filename)
        await msg.delete()

if __name__ == '__main__':
    print("🚀 تشغيل سيرفر الويب والبوت...")
    keep_alive() # تشغيل ميزة البقاء مستيقظاً
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
