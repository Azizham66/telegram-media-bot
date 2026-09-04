from typing import Final
from pathlib import Path
import sys

bot_dir = Path(__file__).resolve().parent
repo_root = bot_dir.parent
for path in (repo_root, bot_dir):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from telegram.ext import Application
from config import BOT_TOKEN
from command_registry import register_handlers

BOT_HANDLE: Final = "@media_d3l_bot"

app = Application.builder().token(BOT_TOKEN).build()


if __name__ == "__main__":
    register_handlers(app)
    app.run_polling()