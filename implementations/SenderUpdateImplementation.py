from interfaces.SenderInterface import SenderInterface
from telegram import Update


class SenderUpdateImplementation(SenderInterface):
    def __init__(self, update: Update):
        self.update = update

    def send_message(self, message):
        self.update.message.reply_text(message)

    def send_photo(self, photo):
        self.update.message.reply_photo(photo)
