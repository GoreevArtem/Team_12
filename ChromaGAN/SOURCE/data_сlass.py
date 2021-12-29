import os
import numpy as np
import cv2
import ChromaGAN.SOURCE.config_model as config


class DATA:
    """Class with data/dataset"""

    def __init__(self, dirname):
        self.dir_path = os.path.join(config.DATA_DIR, dirname)
        self.filelist = os.listdir(self.dir_path)
        self.batch_size = config.BATCH_SIZE
        self.size = len(self.filelist)
        self.data_index = 0

    def read_img(self, filename):
        """Read image from memory, reshape it and discolor"""
        img = cv2.imread(filename, 3)
        labimg = cv2.cvtColor(
            cv2.resize(img, (config.IMAGE_SIZE, config.IMAGE_SIZE)), cv2.COLOR_BGR2Lab
        )
        labimg_ori = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        return (
            np.reshape(labimg[:, :, 0], (config.IMAGE_SIZE, config.IMAGE_SIZE, 1)),
            labimg[:, :, 1:],
            img,
            labimg_ori[:, :, 0],
        )

    def generate_batch(self):
        """Batch generating"""
        batch = []
        labels = []
        filelist = []
        labimg_orit_list = []
        original_list = []
        for _ in range(self.batch_size):
            filename = os.path.join(self.dir_path, self.filelist[self.data_index])
            filelist.append(self.filelist[self.data_index])
            greyimg, colorimg, original, labimg_ori = self.read_img(filename)
            batch.append(greyimg)
            labels.append(colorimg)
            original_list.append(original)
            labimg_orit_list.append(labimg_ori)
            self.data_index = (self.data_index + 1) % self.size
        batch = np.asarray(batch) / 255  # values between 0 and 1
        labels = np.asarray(labels) / 255  # values between 0 and 1
        original_list = np.asarray(original_list)
        labimg_orit_list = np.asarray(labimg_orit_list) / 255  # values between 0 and 1
        return batch, labels, filelist, original_list, labimg_orit_list
