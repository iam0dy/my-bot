import os
import telebot
from yt_dlp import YoutubeDL

# البيانات التي استخرجناها من محادثتنا
API_TOKEN = '7784033323:AAGY_o18u4_5_T7p9i4PqU6h_B7yR6pYf0s'
INSTA_USER = 'jordenjr56'
INSTA_PASS = 'kBi77w4*2X5&LEC'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def download_all_media(message):
    url = message.text
    # فحص إذا كان الرابط من مواقع التواصل المدعومة
    if any(site in url for site in ["instagram.com", "facebook.com", "tiktok.com", "youtube.com", "youtu.be", "twitter.com"]):
        sent_msg = bot.reply_to(message, "⏳ جارٍ معالجة الرابط وتحميل المحتوى (صور/فيديو/ستوري)...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'file_%(id)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # استخدام ملف الكوكيز الذي رفعته من Firefox
            'username': INSTA_USER,       # زيادة تأكيد بالحساب الوهمي
            'password': INSTA_PASS,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # إرسال الملف بناءً على نوعه
                with open(filename, 'rb') as f:
                    if filename.endswith(('.mp4', '.mkv', '.mov', '.webm')):
                        bot.send_video(message.chat.id, f)
                    else:
                        bot.send_photo(message.chat.id, f)
                
                # تنظيف المساحة بحذف الملف بعد الإرسال
                os.remove(filename) 
                bot.delete_message(message.chat.id, sent_msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ فشل التحميل. تأكد من أن الرابط عام وليس لحساب خاص.\nالسبب: {str(e)}", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط صحيح من (إنستغرام، يوتيوب، تيك توك، إلخ...)")

bot.polling()
