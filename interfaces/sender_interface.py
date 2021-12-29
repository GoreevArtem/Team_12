from abc import ABC, abstractmethod


class SenderInterface(ABC):
    """Interface for sending messages and photos"""

    @abstractmethod
    def send_message(self, message):
        """Method to send message"""

    @abstractmethod
    def send_photo(self, photo):
        """Method to send photo"""
