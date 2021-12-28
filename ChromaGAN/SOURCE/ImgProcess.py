import os
import sys

import cv2
import numpy as np
from tensorflow.keras.models import load_model

import ChromaGAN.SOURCE.config_model as config
import ChromaGAN.SOURCE.dataClass as data


class ImgProcess:

    def __init__(self):
        save_path = os.path.join(config.MODEL_DIR, config.PRETRAINED)
        self.colorizationModel = load_model(save_path)

    def deprocess(self, imgs):
        imgs = imgs * 255
        imgs[imgs > 255] = 255
        imgs[imgs < 0] = 0
        return imgs.astype(np.uint8)

    def reconstruct_no(self, batchX, predictedY):
        result = np.concatenate((batchX, predictedY), axis=2)
        result = cv2.cvtColor(result, cv2.COLOR_Lab2BGR)
        return result

    def sample_images(self, concatenate=False):
        test_data = data.DATA(config.TEST_DIR)
        assert config.BATCH_SIZE <= test_data.size, "The batch size should be smaller or equal to the number of testing images --> modify it in config_bot.py"
        total_batch = int(test_data.size / config.BATCH_SIZE)
        for b in range(total_batch):
            # batchX, batchY,  filelist  = test_data.generate_batch()
            try:
                batchX, batchY, filelist, original, labimg_oritList = test_data.generate_batch()
            except Exception as e:
                sys.stderr.write("Failed to generate batch: {}\n".format(e))
                continue
            predY, _ = self.colorizationModel.predict(
                np.tile(batchX, [1, 1, 1, 3]))
            for i in range(config.BATCH_SIZE):
                originalResult = original[i]
                height, width, channels = originalResult.shape
                predictedAB = cv2.resize(self.deprocess(predY[i]),
                                         (width, height))
                labimg_ori = np.expand_dims(labimg_oritList[i], axis=2)
                predResult = self.reconstruct_no(self.deprocess(labimg_ori),
                                                 predictedAB)
                save_path = os.path.join(config.OUT_DIR, filelist[i])
                if concatenate:
                    result_img = np.concatenate((predResult, originalResult))
                else:
                    result_img = predResult
                if not cv2.imwrite(save_path, result_img):
                    print("Failed to save " + save_path)
                print("Batch " + str(b) + "/" + str(total_batch))
