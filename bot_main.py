import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, \
    MessageHandler, Updater

from config_bot import Config
from utils import Utils
from implementations.SenderUpdateImplementation import \
    SenderUpdateImplementation

MAX_FILE_SIZE = 100000000000
conf = Config()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    name = update.message.chat.first_name
    update.message.reply_text(f"Hello {name}")
    update.message.reply_text(
        "Submit a black and white picture to make it in color!\n"
        "I can only work with photos!")


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(
        f'I can only work with photos!\n'
        f'Submit a black and white picture to make it in color!')


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def process_image(update: Update, context: CallbackContext):
    file = update.message.photo[-1].get_file()
    Utils.process_image(file, update.message.chat_id,
                        SenderUpdateImplementation(update))


def main():
    updater = Updater(conf.properties['token'], use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # image processing
    updater.dispatcher.add_handler(
        MessageHandler(Filters.photo, process_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
