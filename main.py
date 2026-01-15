import os
import telebot
from yt_dlp import YoutubeDL

# التوكن والبيانات
API_TOKEN = '7784033323:AAGY_o18u4_5_T7p9i4PqU6h_B7yR6pYf0s'
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def download_all(message):
    url = message.text
    if any(site in url for site in ["instagram.com", "facebook.com", "tiktok.com", "youtube.com", "youtu.be"]):
        sent_msg = bot.reply_to(message, "⏳ يتم الآن استخراج الفيديو بصيغة عالية الجودة...")
        
        ydl_opts = {
            # التعديل الجديد هنا للبحث عن أفضل صيغة متاحة
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'file_%(id)s.%(ext)s',
            'cookiefile': 'cookies.txt',
            'username': INSTA_USER,
            'password': INSTA_PASS,
            'quiet': True,
            'no_warnings': True,
            # إضافة User-Agent حديث جداً
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extract_flat': False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # التأكد من وجود الملف وإرساله
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        if filename.lower().endswith(('.mp4', '.mkv', '.mov')):
                            bot.send_video(message.chat.id, f)
                        else:
                            bot.send_photo(message.chat.id, f)
                    os.remove(filename) 
                
                bot.delete_message(message.chat.id, sent_msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ حدث عطل فني: إنستغرام يرفض الطلب حالياً.\nجرب رابطاً آخر أو تأكد أن الحساب عام.", message.chat.id, sent_msg.message_id)

bot.polling(non_stop=True) # أضفنا non_stop لمنع التوقف
