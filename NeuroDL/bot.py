import os
import yt_dlp
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Load the environment variables
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

    keyboard = [
        [
            InlineKeyboardButton("🎥 Video", callback_data='video'),
            InlineKeyboardButton("🎵 Audio", callback_data='audio')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("What format would you like?", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    url = context.user_data.get('current_url')
    
    if not url:
        await query.edit_message_text("Session expired. Please send the link again.")
        return

    await query.edit_message_text(f"⏳ Downloading {choice}... This might take a minute.")

    # Base configuration for yt-dlp
    ydl_opts = {
        'outtmpl': 'temp_download_%(id)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web']
            }
        }
    }


    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
    else:
        print("WARNING: cookies.txt not found in the container!")


    # --- FORMAT LOGIC ---
    if choice == 'video':
        if 'instagram.com' in url:
            # ULTIMATE INSTAGRAM FIX: Force the pre-merged single file
            ydl_opts['format'] = 'best' 
        else:
            # YouTube gets the high-quality merge treatment
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    filename = None
    try:
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Update filename if audio post-processor changed the extension
            if choice == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        await query.edit_message_text("📤 Uploading to Telegram...")
        
        # Upload to Telegram
        with open(filename, 'rb') as file:
            if choice == 'video':
                await context.bot.send_video(chat_id=query.message.chat_id, video=file)
            else:
                await context.bot.send_audio(chat_id=query.message.chat_id, audio=file)
        
        await query.edit_message_text("✅ Done!")

    except Exception as e:
        await query.edit_message_text(f"❌ An error occurred: {str(e)}")
        
    finally:
        # ALWAYS clean up
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
    