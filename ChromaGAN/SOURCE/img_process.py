"""Module for image processing"""

import os
import sys

import cv2
import numpy as np
from tensorflow.keras.models import load_model

import ChromaGAN.SOURCE.config_model as config
import ChromaGAN.SOURCE.data_сlass as data


def deprocess(imgs):
    """From [0,1] -> [0,255]"""
    imgs = imgs * 255
    imgs[imgs > 255] = 255
    imgs[imgs < 0] = 0
    return imgs.astype(np.uint8)


def reconstruct(batch_x, predicted_y, file_list):
    """Concat original image with result,
    convert into BGR channel and save it"""
    result = reconstruct_no(batch_x, predicted_y)
    save_results_path = os.path.join(config.OUT_DIR, config.TEST_NAME)
    if not os.path.exists(save_results_path):
        os.makedirs(save_results_path)
    save_path = os.path.join(save_results_path, file_list + "_reconstructed.jpg")
    cv2.imwrite(save_path, result)
    return result


def reconstruct_no(batch_x, predicted_y):
    """Concat original image with result and convert into BGR channel"""
    result = np.concatenate((batch_x, predicted_y), axis=2)
    result = cv2.cvtColor(result, cv2.COLOR_Lab2BGR)
    return result


class ImgProcess:
    """Class for sampling images"""

    def __init__(self):
        save_path = os.path.join(config.MODEL_DIR, config.PRETRAINED)
        self.colorization_model = load_model(save_path)

    def sample_images(self, concatenate=False):
        """Colorize image"""
        test_data = data.DATA(config.TEST_DIR)
        assert (
            config.BATCH_SIZE <= test_data.size
        ), ("The batch size should be smaller or equal to "
            "the number of testing images --> modify it in config_bot.py")
        total_batch = int(test_data.size / config.BATCH_SIZE)
        for _ in range(total_batch):
            # batchX, batchY,  filelist  = test_data.generate_batch()
            try:
                (
                    batch_x,
                    _,
                    filelist,
                    original,
                    labimg_orit_list,
                ) = test_data.generate_batch()
            except Exception as e:
                sys.stderr.write(f"Failed to generate batch: {e}\n")
                continue
            pred_y, _ = self.colorization_model.predict(np.tile(batch_x, [1, 1, 1, 3]))
            for i in range(config.BATCH_SIZE):
                original_result = original[i]
                height, width, _ = original_result.shape
                predicted_ab = cv2.resize(deprocess(pred_y[i]), (width, height))
                labimg_ori = np.expand_dims(labimg_orit_list[i], axis=2)
                pred_result = reconstruct_no(deprocess(labimg_ori), predicted_ab)
                save_path = os.path.join(config.OUT_DIR, filelist[i])
                if concatenate:
                    result_img = np.concatenate((pred_result, original_result))
                else:
                    result_img = pred_result
                if not cv2.imwrite(save_path, result_img):
                    print("Failed to save " + save_path)
