import asyncio
import json
from typing import Final
from pathlib import Path
import sys

bot_dir = Path(__file__).resolve().parent
repo_root = bot_dir.parent
for path in (repo_root, bot_dir):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN
from command_registry import register_handlers

BOT_HANDLE: Final = "@media_d3l_bot"

bot_application = Application.builder().token(BOT_TOKEN).build()
register_handlers(bot_application)

_application_started = False
_application_lock = asyncio.Lock()


async def _start_application() -> None:
    global _application_started

    if _application_started:
        return

    async with _application_lock:
        if not _application_started:
            await bot_application.initialize()
            await bot_application.start()
            _application_started = True


async def app(scope, receive, send):
    if scope.get("type") != "http":
        return

    if scope.get("method") == "GET":
        body = b"Telegram bot is running"
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain; charset=utf-8")],
        })
        await send({"type": "http.response.body", "body": body})
        return

    if scope.get("method") != "POST":
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain; charset=utf-8")],
        })
        await send({"type": "http.response.body", "body": b"Method not allowed"})
        return

    request_body = b""
    while True:
        message = await receive()
        request_body += message.get("body", b"")
        if not message.get("more_body", False):
            break

    try:
        update_data = json.loads(request_body)
        await _start_application()
        update = Update.de_json(update_data, bot_application.bot)
        await bot_application.process_update(update)
    except Exception:
        await send({
            "type": "http.response.start",
            "status": 400,
            "headers": [(b"content-type", b"text/plain; charset=utf-8")],
        })
        await send({"type": "http.response.body", "body": b"Invalid update"})
        return

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain; charset=utf-8")],
    })
    await send({"type": "http.response.body", "body": b"OK"})


if __name__ == "__main__":
    bot_application.run_polling()