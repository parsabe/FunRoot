import os
import yt_dlp
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Load the environment variables from the .env file
load_dotenv()

# Safely grab the token
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube, Instagram, or TikTok link!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Basic check to see if it looks like a link
    if "http" not in url:
        await update.message.reply_text("Please send a valid URL.")
        return

    # Store the URL in the user's session data
    context.user_data['current_url'] = url

    # Create the inline keyboard buttons
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
    await query.answer() # Acknowledge the button click
    
    choice = query.data
    url = context.user_data.get('current_url')
    
    if not url:
        await query.edit_message_text("Session expired. Please send the link again.")
        return

    await query.edit_message_text(f"⏳ Downloading {choice}... This might take a minute.")

    # Base configuration for yt-dlp
    ydl_opts = {
        'outtmpl': 'temp_download_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # THE ULTIMATE BYPASS: Pretend to be a mobile Safari browser to dodge bot-checks
        'extractor_args': {'youtube': ['player_client=web_safari,android']},
    }

    # --- SMART COOKIE ROUTING ---
    # Give yt-dlp the right keys for the right website
    if 'instagram.com' in url:
        ydl_opts['cookiefile'] = 'instagram_cookies.txt'
    elif 'youtube.com' in url or 'youtu.be' in url:
        ydl_opts['cookiefile'] = 'youtube_cookies.txt'

    # Adjust config based on what the user clicked
    if choice == 'video':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4' # Grabs the best pre-merged, Telegram-friendly video
    elif choice == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    filename = None
    try:
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # If it's audio, yt-dlp renames the file to .mp3 after downloading
            if choice == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        # Upload the file to Telegram
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
        # ALWAYS clean up: delete the file from the VPS so your storage doesn't get full
        if filename and os.path.exists(filename):
            os.remove(filename)

def main():
    # Start the bot
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()