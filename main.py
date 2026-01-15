import os
import telebot
from flask import Flask
from threading import Thread
from yt_dlp import YoutubeDL

# --- إعدادات السيرفر (Public/Private Handling) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running Securely!"

def run_web():
    # بورت 8080 هو المطلوب لمنصة Koyeb
    app.run(host='0.0.0.0', port=8080)

# --- إعدادات البوت والتوكن الجديد ---
NEW_API_TOKEN = '7257387654:AAH6VJthFkSgkcskOPl03wc-b7fQPGV8cUg'
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(NEW_API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if any(site in url for site in ["instagram.com", "youtube.com", "youtu.be", "tiktok.com"]):
        sent_msg = bot.reply_to(message, "⏳ جاري التحميل باستخدام الهوية الرقمية...")
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt', # الملف الذي رفعته سابقاً
            'username': INSTA_USER,
            'password': INSTA_PASS,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            if not os.path.exists('downloads'): os.makedirs('downloads')
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                with open(filename, 'rb') as f:
                    bot.send_document(message.chat.id, f)
                
                os.remove(filename)
                bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ عذراً، حدث خطأ: {str(e)}", message.chat.id, sent_msg.message_id)

# --- تشغيل البوت مع نظام الاستمرارية ---
if __name__ == "__main__":
    # تشغيل خادم الويب في الخلفية لجعل البوت Public ومستقر
    t = Thread(target=run_web)
    t.start()
    
    print("Bot is starting with the new Token...")
    # نظام infinity_polling يمنع توقف البوت عند حدوث أخطاء بسيطة
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
