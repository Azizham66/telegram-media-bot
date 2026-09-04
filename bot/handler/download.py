import asyncio
import os
import logging
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ContextTypes
from yt_dlp.utils import DownloadError

from bot.config import DOWNLOAD_DIR, MAX_FILE_SIZE_MB

LOG = logging.getLogger(__name__)
USER_WAIT_KEY = 'waiting_for_url'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def _ydl_get_info_sync(url: str, ydl_opts: dict) -> dict:
    """
    Synchronous function to get video info using yt_dlp.
    """
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)
    
def _ydl_download_sync(url: str, ydl_opts: dict) -> str:
    """
    Synchronous function to download video using yt_dlp.
    Returns the path to the downloaded file.
    """
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

async def start_download(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text("Checking the URL and preparing to download...")
    
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        info = await asyncio.to_thread(_ydl_get_info_sync, url, ydl_opts)
        await update.message.reply_text(f"Found: {info.get('title', '(unknown title)')}. Starting download...")
    except Exception as e:
        LOG.error(f"Error occurred while checking URL: {e}")
        await update.message.reply_text("An error occurred while checking the URL.")
        context.user_data.pop(USER_WAIT_KEY, None)
        return
    
    filesize = info.get('filesize') or info.get('filesize_approx') or 0
    if filesize > MAX_FILE_SIZE_MB * 1024 * 1024:
        await update.message.reply_text(f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.")
        context.user_data.pop(USER_WAIT_KEY, None)
        return
    
    await update.message.reply_text("Starting the download, this may take a while...")

    try:
        file_path = await asyncio.to_thread(_ydl_download_sync, url, ydl_opts)
    except DownloadError as e:
        LOG.error(f"Download failed: {e}")
        await update.message.reply_text("Download failed. Please try again later.")
        context.user_data.pop(USER_WAIT_KEY, None)
        return
    except Exception as e:
        LOG.error(f"Unexpected error during download: {e}")
        await update.message.reply_text("An unexpected error occurred during the download.")
        context.user_data.pop(USER_WAIT_KEY, None)
        return
    
    if not os.path.exists(file_path):
        await update.message.reply_text("Download completed, but the file was not found.")
        context.user_data.pop(USER_WAIT_KEY, None)
        return
    
    try:
        await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        await update.message.reply_text("File sent")
    except Exception as e:
        LOG.error(f"Failed to send the file: {e}")
        await update.message.reply_text("Failed to send the file. Please try again later.")
    finally:
        try:
            os.remove(file_path)
        except Exception as e:
            LOG.error(f"Failed to delete the file {file_path}: {e}")
        context.user_data.pop(USER_WAIT_KEY, None)

