"""Configs for neural network"""

import os

# DIRECTORY INFORMATION
TEST_NAME = "FirstTest"
ROOT_DIR = "ChromaGAN/"
DATA_DIR = os.path.join(ROOT_DIR, "SAMPLE_IMGS/")
OUT_DIR = os.path.join(ROOT_DIR, "SAMPLE_IMGS/reconstructed")
MODEL_DIR = os.path.join(ROOT_DIR, "MODEL/")
LOG_DIR = os.path.join(ROOT_DIR, "LOGS/")

TRAIN_DIR = "train"  # UPDATE
TEST_DIR = "gray"  # UPDATE

# DATA INFORMATION
IMAGE_SIZE = 224
BATCH_SIZE = 1


# TRAINING INFORMATION
PRETRAINED = "modelPretrained.h5"  # UPDATE
NUM_EPOCHS = 5
