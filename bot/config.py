# bot/config.py (suggested)
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required in environment")

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
if os.getenv("VERCEL") and not os.path.isabs(DOWNLOAD_DIR):
    DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "telegram-media-bot")
try:
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
except ValueError:
    MAX_FILE_SIZE_MB = 100
DEFAULT_YT_DLP_FORMAT = os.getenv("DEFAULT_YT_DLP_FORMAT", "bestaudio/best")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")