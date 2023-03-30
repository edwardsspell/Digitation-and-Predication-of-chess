
import time

from digitization.fen import list_to_board, board_to_fen, compare_fen
from digitization.infer_pieces import infer_chess_pieces
from digitization.predict_board import detect_input_board, obtain_individual_pieces


def predict_board(board_path, a1_pos, obtain_pieces_probs):
    
    total_time = 0

    start = time.perf_counter()
    detect_input_board(board_path)
    elapsed_time = time.perf_counter() - start
    total_time += elapsed_time
    print(f"time detecting the input board: {elapsed_time}")

    start = time.perf_counter()
    pieces = obtain_individual_pieces(board_path)
    elapsed_time = time.perf_counter() - start
    total_time += elapsed_time
    print(f"time obtaining the individual pieces: {elapsed_time}")

    start = time.perf_counter()
    pieces_probs = obtain_pieces_probs(pieces)
    elapsed_time = time.perf_counter() - start
    total_time += elapsed_time
    print(f"time predicting probabilities: {elapsed_time}")

    start = time.perf_counter()
    predictions = infer_chess_pieces(pieces_probs, a1_pos)
    elapsed_time = time.perf_counter() - start
    total_time += elapsed_time
    print(f"time inferring chess pieces: {elapsed_time}")

    start = time.perf_counter()
    board = list_to_board(predictions)
    fen = board_to_fen(board)
    elapsed_time = time.perf_counter() - start
    total_time += elapsed_time
    print(f"time converting to fen notation: {elapsed_time}")

    print(f"total time: {total_time}")

    return fen


