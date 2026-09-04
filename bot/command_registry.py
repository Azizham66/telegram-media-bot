from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handler.start import start, handle_url_button
from handler.url_handler import url_message_handler
from handler.download import start_download


def register_handlers(app):
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(handle_url_button, pattern='^send_url$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, url_message_handler))