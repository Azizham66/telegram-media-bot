from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


WAITING_FOR_URL = 0

keyboard = [[
    InlineKeyboardButton("Send URL", callback_data='send_url'),
    InlineKeyboardButton("Creator", url='https://t.me/az1zx21')
]]

reply_markup = InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm Media DL Bot, send me a media link and I'll download it for you.", reply_markup=reply_markup)
    
    
async def handle_url_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer() # Acknowledge the callback query
    """
    Prompt the user to send the URL and wait for their response. You can set a state or flag to indicate that the bot is waiting for the URL.
    """
    context.user_data['waiting_for_url'] = True
    await query.edit_message_text("Please send the URL you want to download.")
    
    