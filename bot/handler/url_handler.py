from telegram import Update
from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from handler.download import start_download

def is_valid_ytdlp_url(url: str) -> bool:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.extract_info(url, download=False)
            return True
        except DownloadError:
            return False
    
async def url_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle URL by verifying it's a valid ytdlp URL
    """
    if not context.user_data.get('waiting_for_url'):
        await update.message.reply_text('Please click "Send URL" button or send /url command first.')
        return
    
    text = update.message.text
    if not is_valid_ytdlp_url(text):
        await update.message.reply_text(f"Invalid URL, Please try again: {text}")    
        return
    
    await start_download(update, context, text)