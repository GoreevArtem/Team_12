"""Module with bot logic"""
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from ChromaGAN.SOURCE import config_model
from config_bot import Config
from db_helper import DB_Helper
from implementations.sender_message_implementation import SenderMessageImplementation
from ping import get_statistics
from utils import Utils

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

buttons = [
    [
        KeyboardButton("/help"),
        KeyboardButton("/ping_yandex"),
        KeyboardButton(COMMAND_HISTORY),
        KeyboardButton(COMMAND_LAST),
        KeyboardButton(COMMAND_CLEAN),
    ]
]
reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)


async def start(message: types.Message):
    """Send a message when the command /start is issued."""
    name = message.chat.first_name
    await message.reply(f"Hello, {name}!")
    await message.reply(
        "Submit a black and white picture to make it in color!\n"
        "I can only work with photos!",
        reply_markup=reply_keyboard,
    )


async def ping_yandex(message: types.Message):
    """Ping yandex and return statistics"""
    await get_statistics("yandex.ru", 10, SenderMessageImplementation(message))


async def echo(message: types.Message):
    """Echo the user message."""
    text = message.text
    chat_id = message.chat.id
    if text == COMMAND_HISTORY:
        urls = await db_helper.get_all_urls(chat_id)
        repl = "\n".join(urls) if urls is not None else "Your history is clean!"
        await message.answer(repl)
    elif text == COMMAND_LAST:
        url = await db_helper.get_last_url(chat_id)
        repl = url if url is not None else "Your history is clean!"
        await message.answer(repl)
    elif text == COMMAND_CLEAN:
        await db_helper.clean_history(chat_id)
        await message.answer("Done!")
    else:
        await message.answer(
            "I can only work with photos!\n"
            "Submit a black and white picture to make it in color!",
            reply_markup=reply_keyboard,
        )


async def error(update, exception):
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {exception}")


async def download_file(message: types.Message, file):
    """Download file from telegram"""
    file_name = f"{message.chat.id}_{datetime.now().timestamp()}"
    file_path = (
        f"{os.path.join(config_model.DATA_DIR, config_model.TEST_DIR)}/{file_name}.jpg"
    )
    await message.bot.download_file(file.file_path, file_path)
    return file_name, file.file_size


async def process_image(message: types.Message, file):
    """Image processing with neural network"""
    file_name, file_size = await download_file(message, file)
    file_path = await Utils.process_image(
        file_name, file_size, SenderMessageImplementation(message)
    )
    if not file_path:
        return
    with open(file_path, "rb") as file_stream:
        await message.reply_photo(file_stream, reply_markup=reply_keyboard)
    url = Utils.save_image(file_path)
    await db_helper.add_or_update_url(message.chat.id, url)
    Utils.clean_all_dirs()


async def process_normal_image(message: types.Message):
    """Simple photo processing with neural network"""
    file = await message.photo[-1].get_file()
    await process_image(message, file)


async def process_doc_image(message: types.Message):
    """Document photo processing with neural network"""
    doc_type = str(message["document"].mime_type)
    if doc_type.startswith("image"):
        file = await message.bot.get_file(message.document.file_id)
        await process_image(message, file)
    else:
        await message.reply("Sorry, I can work only with photos!")


def main():
    """Start bot and config it"""
    bot = Bot(token=conf.properties["token"])
    dispatcher = Dispatcher(bot)

    # on different commands - answer in Telegram
    dispatcher.register_message_handler(start, CommandStart())

    # ping yandex and get statistics
    dispatcher.register_message_handler(ping_yandex, Command(("ping_yandex",)))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.register_message_handler(echo)

    # log all errors
    dispatcher.register_errors_handler(error)

    # image processing
    dispatcher.register_message_handler(
        process_normal_image, content_types=types.ContentTypes.PHOTO
    )

    # image doc processing
    dispatcher.register_message_handler(
        process_doc_image, content_types=types.ContentTypes.DOCUMENT
    )

    # Start the Bot
    executor.start_polling(dispatcher)


if __name__ == "__main__":
    logger.info("Start Bot")
    main()
