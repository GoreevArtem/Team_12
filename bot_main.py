"""Module with bot logic"""

import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from config_bot import Config
from utils import Utils
from implementations.sender_update_implementation import SenderUpdateImplementation
from db_helper import DB_Helper

conf = Config()
db_helper = DB_Helper()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 100000000000
COMMAND_CLEAN = "Clean history"
COMMAND_LAST = "Last colored photo"
COMMAND_HISTORY = "All colored photos"


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""

    buttons = [
        [
            KeyboardButton("/help"),
            KeyboardButton(COMMAND_HISTORY),
            KeyboardButton(COMMAND_LAST),
            KeyboardButton(COMMAND_CLEAN),
        ]
    ]
    name = update.message.chat.first_name
    update.message.reply_text(f"Hello, {name}!")
    update.message.reply_text(
        "Submit a black and white picture to make it in color!\n"
        "I can only work with photos!",
        reply_markup=ReplyKeyboardMarkup(buttons),
    )


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    text = update.message.text
    chat_id = update.message.chat_id
    if text == COMMAND_HISTORY:
        urls = db_helper.get_all_urls(chat_id)
        reply = "\n".join(urls) if urls is not None else "Your history is clean!"
        update.message.reply_text(reply)
    elif text == COMMAND_LAST:
        url = db_helper.get_last_url(chat_id)
        reply = url if url is not None else "Your history is clean!"
        update.message.reply_text(reply)
    elif text == COMMAND_CLEAN:
        db_helper.clean_history(chat_id)
        update.message.reply_text("Done!")
    else:
        update.message.reply_text(
            "I can only work with photos!\n"
            "Submit a black and white picture to make it in color!"
        )


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}")


def process_image(update, file):
    """Image processing with neural network"""
    file_path = Utils.process_image(
        file, update.message.chat_id, SenderUpdateImplementation(update)
    )
    if not file_path:
        return
    with open(file_path, "rb") as file_stream:
        update.message.reply_photo(file_stream)
    url = Utils.save_image(file_path)
    db_helper.add_or_update_url(update.message.chat_id, url)
    Utils.clean_all_dirs()


def process_normal_image(update: Update, context: CallbackContext):
    """Simple photo processing with neural network"""
    file = update.message.photo[-1].get_file()
    process_image(update, file)


def process_doc_image(update: Update, context: CallbackContext):
    """Document photo processing with neural network"""
    doc_type = str(update.message["document"].mime_type)
    if doc_type.startswith("image"):
        file = context.bot.get_file(update.message.document)
        process_image(update, file)
    else:
        update.message.reply_text("Sorry, I can work only with photos!")


def main():
    """Start bot and config it"""
    updater = Updater(conf.properties["token"], use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # image processing
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, process_normal_image))

    # image doc processing
    updater.dispatcher.add_handler(MessageHandler(Filters.document, process_doc_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    logger.info("Start Bot")
    main()
