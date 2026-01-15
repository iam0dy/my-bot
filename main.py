import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import yt_dlp

# Get token from environment variable (set in Koyeb dashboard)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# yt-dlp options for best quality
ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "merge_output_format": "mp4",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
}

async def download_media(url: str) -> str:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Send me a link from Instagram, TikTok, YouTube, Twitter, or Facebook!")

@dp.message_handler()
async def handle_url(message: types.Message):
    url = message.text.strip()
    try:
        file_path = await download_media(url)
        await bot.send_document(message.chat.id, InputFile(file_path))
        os.remove(file_path)
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)