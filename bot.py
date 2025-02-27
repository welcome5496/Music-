import telebot
import os
import yt_dlp
import re

# Replace with your Telegram Bot Token
TOKEN = "7995739639:AAHwFkfjrh6-RZTCBV793imNmMDe6hn-GGo"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Function to sanitize filenames (remove special characters)
def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)  # Removes invalid filename characters

# Function to download audio by song name and save with proper name
def download_audio(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': '%(title)s.%(ext)s'  # Saves file with song name
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        song_title = info['entries'][0]['title']
        clean_title = clean_filename(song_title)  # Clean filename
        filename = f"{clean_title}.mp3"  # Save as MP3
        return filename, song_title

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 Send a song name to download the MP3!")

# Handle Song Name Search
@bot.message_handler(func=lambda message: True)
def get_audio(message):
    song_query = message.text
    bot.send_message(message.chat.id, f"🔍 Searching for: {song_query}")

    try:
        filename, song_title = download_audio(song_query)
        with open(filename, "rb") as audio:
            bot.send_audio(message.chat.id, audio, caption=f"Here is your song: {song_title} 🎶")
        os.remove(filename)  # Delete after sending
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

bot.polling()
