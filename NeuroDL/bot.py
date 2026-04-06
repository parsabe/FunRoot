import os
import yt_dlp
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube, Instagram, or TikTok link!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        await update.message.reply_text("Please send a valid URL.")
        return

    context.user_data['current_url'] = url
    keyboard = [[InlineKeyboardButton("🎥 Video", callback_data='video'),
                 InlineKeyboardButton("🎵 Audio", callback_data='audio')]]
    
    await update.message.reply_text("What format would you like?", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    url = context.user_data.get('current_url')
    
    if not url:
        await query.edit_message_text("Session expired. Please send the link again.")
        return

    await query.edit_message_text(f"⏳ Downloading {choice}... This might take a minute.")

    # Optimized configuration
    ydl_opts = {
        'outtmpl': 'temp_download_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': '/usr/bin/ffmpeg', # Verified from your terminal output
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web_safari']
            }
        }
    }

    # Cookie Routing
    if 'instagram.com' in url:
        ydl_opts['cookiefile'] = 'instagram_cookies.txt'
    elif 'youtube.com' in url or 'youtu.be' in url:
        ydl_opts['cookiefile'] = 'youtube_cookies.txt'

    # Format Logic
    if choice == 'video':
        # Forces high quality MP4 that includes audio
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4'
    else:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if choice == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        await query.edit_message_text("📤 Uploading to Telegram...")
        
        with open(filename, 'rb') as file:
            if choice == 'video':
                await context.bot.send_video(chat_id=query.message.chat_id, video=file)
            else:
                await context.bot.send_audio(chat_id=query.message.chat_id, audio=file)
        
        await query.edit_message_text("✅ Done!")

    except Exception as e:
        await query.edit_message_text(f"❌ An error occurred: {str(e)}")
        
    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()