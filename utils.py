import os
from datetime import datetime

from ChromaGAN.SOURCE import config_model
from ChromaGAN.SOURCE.img_process import ImgProcess
from interfaces.sender_interface import SenderInterface

MAX_FILE_SIZE = 100000000000
img_process = ImgProcess()


class Utils:
    """Class with utils"""

    def __init__(self):
        pass

    @staticmethod
    def download_image_from_file(file, chat_id):
        """Download image"""
        file_name = f"{chat_id}_{datetime.now().timestamp()}"
        file.download(
            f"{os.path.join(config_model.DATA_DIR, config_model.TEST_DIR)}/{file_name}.jpg"
        )
        return file.file_size, file_name

    @staticmethod
    def clear_dir(file_dir):
        """Clean directory"""
        for filename in os.listdir(file_dir):
            filepath = os.path.join(file_dir, filename)
            os.remove(filepath)

    @staticmethod
    def process_image(file, chat_id, sender: SenderInterface):
        """Process an image and sent to user"""
        file_size, file_name = Utils.download_image_from_file(file, chat_id)
        if file_size > MAX_FILE_SIZE:
            sender.send_message("Sorry, your photo is too big!")
        else:
            sender.send_message("Wait, your image is processed!")
            img_process.sample_images()
            file_path = f"{config_model.OUT_DIR}/{file_name}.jpg"
            return file_path
        return None

    @staticmethod
    def clean_all_dirs():
        """Cleans dirs with black-and-white and reconstructed photos"""
        Utils.clear_dir(config_model.OUT_DIR)
        Utils.clear_dir(os.path.join(config_model.DATA_DIR, config_model.TEST_DIR))
