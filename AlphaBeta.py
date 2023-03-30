import chess
import sunfish
import math
import random
import sys
import MinMax
from flask import Flask
import werkzeug
from flask import request
app = Flask(__name__)

def minimaxRoot(depth, board,isMaximizing):
    possibleMoves = board.legal_moves
    #print(possibleMoves)
    #print(list(possibleMoves))
    bestMove = -9999
    bestMoveFinal = None
    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
        board.pop()
        if( value > bestMove):
            # print("Best score: " ,str(bestMove))
            # print("Best move: ",str(bestMoveFinal))
            bestMove = value
            bestMoveFinal = move
    return bestMoveFinal

def minimax(depth, board, alpha, beta, is_maximizing):
    if(depth == 0):
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if(is_maximizing):
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove


def calculateMove(board):
    possible_moves = board.legal_moves
    if(len(possible_moves) == 0):
        return("No more possible moves...Game Over")
        sys.exit()
    bestMove = None
    bestValue = -9999
    n = 0
    for x in possible_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        boardValue = -evaluation(board)
        board.pop()
        if(boardValue > bestValue):
            bestValue = boardValue
            bestMove = move

    return bestMove

def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    return value

@app.route('/predict',methods=["POST"])
def home():
    fen = request.form['FEN']
    board = chess.Board(fen)
    fensp = fen.split(" ")
    if(fensp[1]=='b'):
        move = minimaxRoot(3,board,True)
        move = chess.Move.from_uci(str(move))
        board.push(move)
        fen2=board.fen().split(" ")
        print(board.fen())
        return(fen2[0]) 
    if(fensp[1]=='w'):
        move = minimaxRoot(3,board,True)
        move = chess.Move.from_uci(str(move))
        board.push(move)
        fen2=board.fen().split(" ")
        print(board.fen())
        return(fen2[0])   

@app.route('/', methods = ['POST'])
def handle_request():
    imagefile = request.files['image']
    print(imagefile)
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    return "Image Uploaded Successfully"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
