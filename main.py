import os
import telebot
from flask import Flask
from threading import Thread
from yt_dlp import YoutubeDL

# إعداد خادم ويب بسيط لإبقاء البوت يعمل 24 ساعة على Koyeb
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# البيانات النهائية الخاصة بك
TOKEN = '7257387654:AAH6VJthFkSgkcskOPl03wc-b7fQPGV8cUg'
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text
    if any(site in url for site in ["instagram.com", "youtube.com", "youtu.be", "tiktok.com"]):
        sent_msg = bot.reply_to(message, "⏳ جاري التحميل (فيديو/صور/ستوري)...")
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt', # يستخدم الملف الذي رفعته سابقاً
            'username': INSTA_USER,
            'password': INSTA_PASS,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            if not os.path.exists('downloads'): os.makedirs('downloads')
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # معالجة الألبومات والستوريات المتعددة
                files = [ydl.prepare_filename(e) for e in info.get('entries', [info])]
                
                for filename in files:
                    if os.path.exists(filename):
                        with open(filename, 'rb') as f:
                            if filename.lower().endswith(('.mp4', '.mkv', '.mov')):
                                bot.send_video(message.chat.id, f)
                            else:
                                bot.send_photo(message.chat.id, f)
                        os.remove(filename)
                
                bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ خطأ: تأكد أن الرابط عام.\n{str(e)}", message.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
