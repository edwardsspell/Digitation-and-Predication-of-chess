
import base64
import numpy as np
import io
import os
from pathlib import Path
from PIL import Image

from keras.applications.mobilenet_v2 import preprocess_input as prein_mobilenet
from keras.applications.xception import preprocess_input as prein_xception
from keras.engine.saving import load_model
import onnxruntime

from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS
import werkzeug

from digitization.predict_board import load_image
from digitization.test_predict_board import predict_board
from AlphaBeta import *

import chess
import chess.svg
import cairosvg
from stockfish import Stockfish

stockfish = Stockfish("stockfish.exe")

app = Flask(__name__)
CORS(app)

MODEL_PATH_KERAS = "selected_models/Xception_last.h5"
IMG_SIZE_KERAS = 299
PRE_INPUT_KERAS = prein_xception

MODEL_PATH_ONNX = "selected_models/Xception_last.onnx"
IMG_SIZE_ONNX = 299
PRE_INPUT_ONNX = prein_xception


# MODEL_PATH_ONNX = "selected_models/MobileNetV2_0p5_all.onnx"
# IMG_SIZE_ONNX = 224
# PRE_INPUT_ONNX = prein_mobilenet



# model = load_model(MODEL_PATH_KERAS)


# def obtain_pieces_probs(pieces):
#     predictions = []
#     for piece in pieces:
#         piece_img = load_image(piece, IMG_SIZE_KERAS, PRE_INPUT_KERAS)
#         predictions.append(model.predict(piece_img)[0])
#     return predictions


sess = onnxruntime.InferenceSession(MODEL_PATH_ONNX)

def obtain_pieces_probs(pieces):
    predictions = []
    for piece in pieces:
        piece_img = load_image(piece, IMG_SIZE_ONNX, PRE_INPUT_ONNX)
        predictions.append(
            sess.run(None, {sess.get_inputs()[0].name: piece_img})[0][0])
    return predictions

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route("/digitize", methods=["POST"])
def predict():
    imagefile = request.files['image']
    print(imagefile)
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    img = Image.open(imagefile)
    img=img.rotate(270,expand=True).save("androidFlask.jpg")

    fen = predict_board("androidFlask.jpg", "BL",
                     obtain_pieces_probs)

    return(fen)
    #png generate
    # board = chess.Board(fen)
    # img = chess.svg.board(board)
    # svgPath = Path("predictions/digital.svg")
    # pngPath = Path("predictions/digital.png")
    # f = open(svgPath, "w")
    # f.write(img)
    # f.close()
    # print(fen)
    # cairosvg.svg2png(
    # url=str(svgPath), write_to=str(pngPath))
    # encodedPng = get_response_image(str(pngPath))

    # response = {
    #     'prediction': fen,
    #     'ImageBytes': encodedPng
    # }    
    # return jsonify(response)

@app.route("/predict",methods=["POST"])
def home():
    fend = request.form['FEN']
    board = chess.Board(fend)
    fensp = fend.split(" ")
    stockfish.set_fen_position(fend)
    move = stockfish.get_best_move()
    move = chess.Move.from_uci(str(move))
    board.push(move)
    fen2=board.fen().split(" ")
    print(board.fen())
    return(fen2[0])
    # if(fensp[1]=='b'):
    #     move = minimaxRoot(3,board,True)
    #     move = chess.Move.from_uci(str(move))
    #     board.push(move)
    #     fen2=board.fen().split(" ")
    #     print(board.fen())
    #     return(fen2[0]) 
    # if(fensp[1]=='w'):
    #     move = minimaxRoot(3,board,True)
    #     move = chess.Move.from_uci(str(move))
    #     board.push(move)
    #     fen2=board.fen().split(" ")
    #     print(board.fen())
    #     return(fen2[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
