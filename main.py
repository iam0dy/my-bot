import os
import telebot
from flask import Flask
from threading import Thread
from yt_dlp import YoutubeDL
import time

# --- خادم الويب لإبقاء البوت نشطاً ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online and Checking Cookies!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- البيانات (تأكد من وضع التوكن الجديد هنا) ---
TOKEN = '7257387654:AAH6VJthFkSgkcskOPl03wc-b7fQPGV8cUg'
bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if "http" not in url: return

    sent_msg = bot.reply_to(message, "⏳ جاري فحص الرابط والتحقق من الهوية الرقمية...")
    
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt', 
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    try:
        if not os.path.exists('downloads'): os.makedirs('downloads')
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as f:
                if filename.lower().endswith(('.mp4', '.mkv', '.mov')):
                    bot.send_video(message.chat.id, f)
                else:
                    bot.send_photo(message.chat.id, f)
            
            os.remove(filename)
            bot.delete_message(message.chat.id, sent_msg.message_id)

    except Exception as e:
        error_str = str(e)
        # --- نظام تشخيص أخطاء الكوكيز ---
        if "cookies" in error_str.lower() or "login" in error_str.lower() or "403" in error_str:
            msg = "⚠️ **خطأ في الكوكيز (Cookies Error):**\n"
            msg += "يبدو أن ملف `cookies.txt` غير صالح أو انتهت صلاحيته.\n"
            msg += "💡 **الحل:** استخرج ملف كوكيز جديد من Firefox وارفع ملفاً جديداً لـ GitHub."
        elif "formats" in error_str.lower():
            msg = "❌ **خطأ في الصيغة:**\n"
            msg += "إنستغرام يمنع الوصول للفيديو. قد يكون الحساب خاصاً أو الكوكيز لا تعمل لهذا الحساب."
        else:
            msg = f"❌ **حدث خطأ غير متوقع:**\n`{error_str[:150]}`"
        
        bot.edit_message_text(msg, message.chat.id, sent_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    Thread(target=run_web).start()
    print("Starting bot...")
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
