import os
from flask import Flask
from threading import Thread
import telebot
from yt_dlp import YoutubeDL

# إعداد خادم ويب بسيط لإبقاء الخدمة تعمل على Koyeb
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run(): app.run(host='0.0.0.0', port=8080)

# بيانات البوت والحساب
API_TOKEN = '7784033323:AAGY_o18u4_5_T7p9i4PqU6h_B7yR6pYf0s'
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def download_all(message):
    url = message.text
    if "instagram.com" in url or "youtube.com" in url:
        sent_msg = bot.reply_to(message, "⏳ جارٍ التحميل باستخدام ملف التعريف...")
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt',
            'username': INSTA_USER,
            'password': INSTA_PASS,
            'outtmpl': 'file_%(id)s.%(ext)s',
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                with open(filename, 'rb') as f:
                    bot.send_document(message.chat.id, f)
                os.remove(filename)
                bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ: {str(e)}", message.chat.id, sent_msg.message_id)

# تشغيل الخادم والبوت معاً
Thread(target=run).start()
bot.infinity_polling(timeout=10, long_polling_timeout=5)
