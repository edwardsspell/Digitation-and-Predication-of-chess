
import numpy as np

from digitization.fen import board_to_list, list_to_board, is_white_square, \
    fen_to_board

__PREDS_DICT = {0: 'B', 1: 'K', 2: 'N', 3: 'P', 4: 'Q', 5: 'R', 6: '_',
                7: 'b', 8: 'k', 9: 'n', 10: 'p', 11: 'q', 12: 'r'}

tpdict = {}
for key, val in __PREDS_DICT.items():
    tpdict.update({val: key})

__IDX_TO_PIECE = {0: 'B', 1: 'N', 2: 'P', 3: 'Q', 4: 'R',
                  5: 'b', 6: 'n', 7: 'p', 8: 'q', 9: 'r'}

__WHITE_PIECES = ('P', 'B', 'N', 'R', 'K', 'Q')
__BLACK_PIECES = ('p', 'b', 'n', 'r', 'k', 'q')


def __sort_pieces_list(_pieces_probs_sort):
   
    w_bishops = sorted(_pieces_probs_sort, key=lambda prob: prob[0][0],
                       reverse=True)
    w_knights = sorted(_pieces_probs_sort, key=lambda prob: prob[0][2],
                       reverse=True)
    # Pawns can't be in the first or last row
    w_pawns = sorted(_pieces_probs_sort[8:-8], key=lambda prob: prob[0][3],
                     reverse=True)
    w_queens = sorted(_pieces_probs_sort, key=lambda prob: prob[0][4],
                      reverse=True)
    w_rooks = sorted(_pieces_probs_sort, key=lambda prob: prob[0][5],
                     reverse=True)
    b_bishops = sorted(_pieces_probs_sort, key=lambda prob: prob[0][7],
                       reverse=True)
    b_knights = sorted(_pieces_probs_sort, key=lambda prob: prob[0][9],
                       reverse=True)
    # Pawns can't be in the first or last row
    b_pawns = sorted(_pieces_probs_sort[8:-8],
                     key=lambda prob: prob[0][10], reverse=True)
    b_queens = sorted(_pieces_probs_sort, key=lambda prob: prob[0][11],
                      reverse=True)
    b_rooks = sorted(_pieces_probs_sort, key=lambda prob: prob[0][12],
                     reverse=True)
    return [w_bishops, w_knights, w_pawns, w_queens, w_rooks, b_bishops,
            b_knights, b_pawns, b_queens, b_rooks]


def __max_piece(tops):
    
    value = tops[0][0][0]  # B
    idx = 0
    if tops[1][0][2] > value:  # N
        value = tops[1][0][2]
        idx = 1
    if tops[2][0][3] > value:  # P
        value = tops[2][0][3]
        idx = 2
    if tops[3][0][4] > value:  # Q
        value = tops[3][0][4]
        idx = 3
    if tops[4][0][5] > value:  # R
        value = tops[4][0][5]
        idx = 4
    if tops[5][0][7] > value:  # b
        value = tops[5][0][7]
        idx = 5
    if tops[6][0][9] > value:  # n
        value = tops[6][0][9]
        idx = 6
    if tops[7][0][10] > value:  # p
        value = tops[7][0][10]
        idx = 7
    if tops[8][0][11] > value:  # q
        value = tops[8][0][11]
        idx = 8
    if tops[9][0][12] > value:  # r
        # value = tops[9][0][12]
        idx = 9
    return idx


def __check_bishop(max_idx, tops, w_bishop_sq, b_bishop_sq):
    
    # If it is a bishop, check that there is at most one in each
    # square color
    if max_idx == 0:  # White bishop
        if is_white_square(tops[max_idx][1]):
            if not w_bishop_sq[0]:
                # We are going to set a white bishop in a white
                # square
                w_bishop_sq[0] = True
                return True
            return False
        if not w_bishop_sq[1]:
            # We are going to set a white bishop in a black square
            w_bishop_sq[1] = True
            return True
        return False
    elif max_idx == 5:  # Black bishop
        if is_white_square(tops[max_idx][1]):
            if not b_bishop_sq[0]:
                # We are going to set a black bishop in a white
                # square
                b_bishop_sq[0] = True
                return True
            return False
        if not b_bishop_sq[1]:
            # We are going to set a white bishop in a black square
            b_bishop_sq[1] = True
            return True
        return False

    return True  # If it's not a bishop, nothing to check


def infer_chess_pieces(pieces_probs, a1_pos):
    
    pieces_probs = board_to_list(list_to_board(pieces_probs, a1_pos))

    # None represents that no piece is set in that position yet
    out_preds = [None] * 64

    final_move_sq = -1
    possible_pieces = []
    pieces_probs_sort = [(probs, i) for i, probs in enumerate(pieces_probs)]

    # First choose the kings, there must be one of each color
    white_king = max(pieces_probs_sort, key=lambda prob: prob[0][1])
    black_kings = sorted(pieces_probs_sort, key=lambda prob: prob[0][8],
                         reverse=True)  # Descending order

    black_king = black_kings[0]
    if black_king[1] == white_king[1]:
        black_king = black_kings[1]

    out_preds[white_king[1]] = 'K'
    out_preds[black_king[1]] = 'k'

    out_preds_empty = 62  # We have already set the kings

    # Then set the blank spaces, the CNN has a very high accuracy
    # detecting these cases
    for idx, piece in enumerate(pieces_probs):
        if out_preds[idx] is None:
            if is_empty_square(piece):
                out_preds[idx] = '_'
                out_preds_empty -= 1

    # Save if there is already a bishop in a [white, black] square
    w_bishop_sq = [False, False]
    b_bishop_sq = [False, False]

    # Set the rest of the pieces in the order given by the highest
    # probability of any piece for all the board
    pieces_lists = __sort_pieces_list(pieces_probs_sort)
    # Index to the highest probability, from each list in pieces_lists,
    # that we have not set yet (in the same order than above).
    idx = [0] * 10
    # Top of each sorted piece list (highest probability of each piece)
    tops = [piece_list[0] for piece_list in pieces_lists]
    # Maximum number of pieces of each type in the same order than tops
    max_pieces_left = [2, 2, 8, 1, 2, 2, 2, 8, 1, 2]
    loopcount = 0
    while out_preds_empty > 0:
        # Fill in the square in out_preds that has the piece with the
        # maximum probability of all the board
        max_idx = __max_piece(tops)
        square = tops[max_idx][1]
        # If we haven't maxed that piece type and the square is empty
        if (max_pieces_left[max_idx] > 0
                and out_preds[square] is None
                and __check_bishop(max_idx, tops, w_bishop_sq, b_bishop_sq)):
            # Fill the square and update counters
            # If we have detected the move previously
            if square == final_move_sq and possible_pieces:
                # Only fill the square if one of the possible pieces
                if __IDX_TO_PIECE[max_idx] in possible_pieces:
                    out_preds[square] = __IDX_TO_PIECE[max_idx]
                    out_preds_empty -= 1
                    max_pieces_left[max_idx] -= 1
            else:
                out_preds[square] = __IDX_TO_PIECE[max_idx]
                out_preds_empty -= 1
                max_pieces_left[max_idx] -= 1
        # In any case we must update the entry in tops with the next
        # highest probability for the piece type we have tried
        idx[max_idx] += 1
        if(max_idx == 2 or max_idx == 7):
            if(idx[max_idx] >= 48):
                idx[max_idx] = 47
                tp = tpdict[__IDX_TO_PIECE[max_idx]]
                pieces_lists[max_idx][idx[max_idx]][0][tp] = 0
        else:
            if(idx[max_idx] >= 64):
                idx[max_idx] = 63
                tp = tpdict[__IDX_TO_PIECE[max_idx]]
                pieces_lists[max_idx][idx[max_idx]][0][tp] = 0
        tops[max_idx] = pieces_lists[max_idx][idx[max_idx]]
        loopcount += 1
        if(loopcount > 64*len(idx)):
            for i in range(64):
                if out_preds[i] is None:
                    out_preds[i] = '_'
            break

    return out_preds


def is_empty_square(square_probs):
    
    return __PREDS_DICT[np.argmax(square_probs)] == '_'


def is_white_piece(square_probs):
    
    return np.sum(square_probs[:6]) >= np.sum(square_probs[7:])


