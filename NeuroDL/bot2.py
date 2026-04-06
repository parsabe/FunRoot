import yt_dlp
import sys
import os

def download_instagram_video(url):
    # Path to your cookies file. Make sure it is in the same folder as this script.
    # If your file is literally named "cookies .txt" with a space, change the string below to match exactly.
    cookie_file = 'cookies.txt' 
    
    # Quick check to ensure the script can actually see your cookies file
    if not os.path.exists(cookie_file):
        print(f"⚠️ Warning: '{cookie_file}' not found in the current directory.")
        print("The download might still fail. Please ensure the file is named correctly and in the right folder.\n")

    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(uploader)s_%(id)s.%(ext)s',
        'quiet': False,
        'no_warnings': True,
        
        # 👇 THIS IS THE NEW LINE 👇
        'cookiefile': cookie_file, 
    }

    try:
        print(f"Connecting to Instagram to download: {url}")
        print("Using cookies for authentication...")
        print("Please wait, this might take a moment depending on the video size...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Download completed successfully!")
        
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Download failed. Error details:\n{e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred:\n{e}")

if __name__ == "__main__":
    print("--- Instagram High-Quality Video Downloader (Authenticated) ---")
    
    # Get the URL from the user
    user_url = input("Paste the Instagram URL here: ").strip()
    
    if not user_url:
        print("No URL provided. Exiting.")
        sys.exit()
        
    download_instagram_video(user_url)