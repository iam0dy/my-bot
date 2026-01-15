import os
import telebot
from yt_dlp import YoutubeDL

# بيانات البوت والحساب
API_TOKEN = 'ضع_توكن_بوتك_هنا' # تأكد من وضع التوكن الخاص بك
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def download_and_send(message):
    url = message.text
    if "instagram.com" in url or "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "⏳ جارٍ التحميل... قد يستغرق الأمر ثواني.")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_file.%(ext)s',
            'username': INSTA_USER,
            'password': INSTA_PASS,
            'quiet': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                with open(filename, 'rb') as f:
                    if filename.endswith(('.mp4', '.mkv', '.mov')):
                        bot.send_video(message.chat.id, f)
                    else:
                        bot.send_photo(message.chat.id, f)
                
                os.remove(filename) # حذف الملف بعد الإرسال لتوفير المساحة
                bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ: {str(e)}", message.chat.id, msg.message_id)

bot.polling()
