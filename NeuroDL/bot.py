import os
import yt_dlp
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# 1. Setup Logging - VERY IMPORTANT: Look here for the YouTube Login Code!
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 NeuroDL Active. Send me a YouTube, Instagram, or TikTok link!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        await update.message.reply_text("❌ Please send a valid URL.")
        return
    context.user_data['current_url'] = url
    keyboard = [[InlineKeyboardButton("🎥 Video", callback_data='video'),
                 InlineKeyboardButton("🎵 Audio", callback_data='audio')]]
    await update.message.reply_text("Choose Format:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    url = context.user_data.get('current_url')
    
    if not url:
        await query.edit_message_text("❌ Session expired. Send the link again.")
        return

    await query.edit_message_text(f"⏳ Processing {choice} request...")

    # Define absolute paths for cookies
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ig_cookies = os.path.join(base_dir, 'instagram_cookies.txt')

    # 2. Universal Base Configuration
    ydl_opts = {
        'outtmpl': os.path.join(base_dir, 'temp_dl_%(id)s.%(ext)s'),
        'ffmpeg_location': '/usr/bin/', # Pointing to the directory
        'quiet': False,
        'no_warnings': False,
    }

    # 3. Platform Specific Logic
    if 'youtube.com' in url or 'youtu.be' in url:
        # YOUTUBE OAUTH2 STRATEGY
        ydl_opts.update({
            'username': 'oauth2',
            'password': '',
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android'],
                    'player_skip_bundle_url': True,
                }
            }
        })
    elif 'instagram.com' in url:
        # INSTAGRAM ANDROID SPOOF STRATEGY
        if os.path.exists(ig_cookies):
            ydl_opts['cookiefile'] = ig_cookies
        
        ydl_opts.update({
            'user_agent': 'Instagram 322.0.0.35.105 Android (33/13; 480dpi; 1080x2213; ZTE; Nubia Red Magic 8 Pro; aurora; qcom; en_US; 568340173)',
            'extractor_args': {
                'instagram': {
                    'include_dash': True,
                    'include_hls': True,
                }
            }
        })

    # 4. Format Logic (H.264/AAC for iOS & Windows Compatibility)
    if choice == 'video':
        ydl_opts['format'] = 'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[ext=mp4]/best'
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

            # Ensure we have the right extension after merging
            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]
                if os.path.exists(f"{base}.mp4"): filename = f"{base}.mp4"
                elif os.path.exists(f"{base}.mkv"): filename = f"{base}.mkv"

            if choice == 'audio' and not filename.endswith('.mp3'):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        await query.edit_message_text("📤 Uploading to Telegram...")
        with open(filename, 'rb') as file:
            if choice == 'video':
                await context.bot.send_video(chat_id=query.message.chat_id, video=file, supports_streaming=True)
            else:
                await context.bot.send_audio(chat_id=query.message.chat_id, audio=file)
        await query.edit_message_text("✅ Done!")

    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")
        logging.error(f"DOWNLOAD ERROR: {e}")
    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("NeuroDL is running...")
    app.run_polling()

if __name__ == "__main__":
    main()