from abc import ABC, abstractmethod


class SenderInterface(ABC):
    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def send_photo(self, photo):
        pass
