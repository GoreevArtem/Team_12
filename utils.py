"""Module with utils"""
import os

import aiohttp

from ChromaGAN.SOURCE import config_model
from ChromaGAN.SOURCE.img_process import ImgProcess
from config_bot import Config
from interfaces.sender_interface import SenderInterface

MAX_FILE_SIZE = 100000000000
UPLOAD_POST = "https://api.imgbb.com/1/upload"

img_process = ImgProcess()
config = Config()


class Utils:
    """Class with utils"""

    def __init__(self):
        pass

    @staticmethod
    def clear_dir(file_dir):
        """Clean directory"""
        for filename in os.listdir(file_dir):
            filepath = os.path.join(file_dir, filename)
            os.remove(filepath)

    @staticmethod
    async def process_image(file_name, file_size, sender: SenderInterface):
        """Process an image and sent to user"""
        if file_size > MAX_FILE_SIZE:
            await sender.send_message("Sorry, your photo is too big!")
        else:
            await sender.send_message("Wait, your image is processed!")
            img_process.sample_images()
            file_path = f"{config_model.OUT_DIR}/{file_name}.jpg"
            return file_path
        return None

    @staticmethod
    def clean_all_dirs():
        """Cleans dirs with black-and-white and reconstructed photos"""
        Utils.clear_dir(config_model.OUT_DIR)
        Utils.clear_dir(os.path.join(config_model.DATA_DIR, config_model.TEST_DIR))

    @staticmethod
    async def save_image(file_path):
        """Saves image on image hosting"""
        with open(file_path, "rb") as image:
            async with aiohttp.ClientSession() as session:
                params = {"key": config.properties["key_image_api"]}
                async with session.post(
                    UPLOAD_POST, params=params, data={"image": image}
                ) as response:
                    json_dict = await response.json()
                    return json_dict["data"]["url"]
