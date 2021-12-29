from telegram import Update
from interfaces.sender_interface import SenderInterface


class SenderUpdateImplementation(SenderInterface):
    """Sender interface implementation for bot"""

    def __init__(self, update: Update):
        self.update = update

    def send_message(self, message):
        """Method to send message"""
        self.update.message.reply_text(message)

    def send_photo(self, photo):
        """Method to send photo"""
        self.update.message.reply_photo(photo)
