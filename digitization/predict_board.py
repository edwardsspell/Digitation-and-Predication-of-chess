
import glob
import os
import re
import shutil
import time

import cv2
import numpy as np
import onnxruntime
from keras.engine.saving import load_model
from keras.preprocessing import image



from digitization.detectboard.detect_board import detect, compute_corners
from digitization.fen import list_to_board, board_to_fen
from digitization.infer_pieces import infer_chess_pieces
from digitization.split_board import split_square_board_image


def load_image(img_path, img_size, preprocess_func):
    img = image.load_img(img_path, target_size=(img_size, img_size))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    return preprocess_func(img_tensor)


def detect_input_board(board_path, board_corners=None):
    
    input_image = cv2.imread(board_path)
    head, tail = os.path.split(board_path)
    tmp_dir = os.path.join(head, "tmp/")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    image_object = detect(input_image, os.path.join(head, "tmp", tail),
                          board_corners)
    board_corners, _ = compute_corners(image_object)
    return board_corners


def obtain_individual_pieces(board_path):

    head, tail = os.path.split(board_path)
    tmp_dir = os.path.join(head, "tmp/")
    pieces_dir = os.path.join(tmp_dir, "pieces/")
    os.mkdir(pieces_dir)
    split_square_board_image(os.path.join(tmp_dir, tail), "", pieces_dir)
    return sorted(glob.glob(pieces_dir + "/*.jpg"))


