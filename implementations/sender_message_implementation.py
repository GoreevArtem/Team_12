"""Sender aiogram interface implementation for bot"""

from aiogram import types
from interfaces.sender_interface import SenderInterface


class SenderMessageImplementation(SenderInterface):
    """Sender aiogram interface implementation for bot"""

    def __init__(self, message: types.Message):
        self.message = message

    async def send_message(self, to_send):
        """Method to send message"""
        await self.message.bot.send_message(self.message.chat.id, to_send)

    async def send_photo(self, photo):
        """Method to send photo"""
        await self.message.reply_photo(photo)
