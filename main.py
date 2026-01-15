import os
import telebot
import time
from flask import Flask
from threading import Thread
from yt_dlp import YoutubeDL

# إعداد سيرفر الويب لإبقاء البوت نشطاً على Koyeb
app = Flask('')
@app.route('/')
def home(): return "Bot is Online with New Token!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- التوكن الجديد الذي قدمته ---
TOKEN = '7257387654:AAGEXWSq-LvtCv0kIHX1biFye8zebf5IdlA'
bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if "http" not in url: return

    sent_msg = bot.reply_to(message, "⏳ جاري التحليل والتحميل...")
    
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt', # الملف الموجود في GitHub
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
                bot.send_document(message.chat.id, f)
            
            os.remove(filename)
            bot.delete_message(message.chat.id, sent_msg.message_id)

    except Exception as e:
        err_msg = str(e).lower()
        # --- نظام تشخيص أخطاء الكوكيز ---
        if "cookie" in err_msg or "login" in err_msg or "403" in err_msg:
            response = "⚠️ **تنبيه بخصوص الكوكيز:**\n"
            response += "يبدو أن ملف `cookies.txt` انتهت صلاحيته أو غير صالح.\n"
            response += "💡 **الحل:** قم باستخراج ملف كوكيز جديد من Firefox وارفع ملفاً جديداً لـ GitHub بنفس الاسم."
        elif "video formats" in err_msg:
            response = "❌ **خطأ:** إنستغرام يمنع الوصول. قد يكون الحساب خاصاً (Private) أو الكوكيز لا تدعم هذا الرابط."
        else:
            response = f"❌ **حدث خطأ:**\n`{str(e)[:100]}`"
        
        bot.edit_message_text(response, message.chat.id, sent_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    # تشغيل خادم الويب
    Thread(target=run_web).start()
    
    # تنظيف الجلسات القديمة لكسر الـ Conflict 409
    print("Stopping old sessions and starting with new token...")
    bot.remove_webhook()
    time.sleep(2) 
    
    bot.infinity_polling(skip_pending=True)
