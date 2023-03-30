
PIECE_TYPES = ['r', 'n', 'b', 'q', 'k', 'p', 'P', 'R', 'N', 'B', 'Q', 'K', '_']


def fen_to_board(fen):
    
    rows = fen.split(sep='/')

    if len(rows) != 8:
        raise ValueError(f"fen must have 8 rows: {fen}")

    board = []
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(['_'] * int(char))
            else:
                board_row.append(char)
        if len(board_row) != 8:
            raise ValueError(f"Each fen row must have 8 positions: {fen}")
        board.append(board_row)

    return board


def board_to_fen(board):
    
    fen = []
    for row in board:
        prev_empty = False
        empty = 0
        for square in row:
            if square == '_':
                empty += 1
                prev_empty = True
            else:
                if prev_empty:
                    prev_empty = False
                    fen.append(str(empty))
                    empty = 0
                fen.append(square)

        if prev_empty:
            fen.append(str(empty))

        fen.append('/')

    return ''.join(fen[:-1])  # Remove final /


def list_to_board(pieces_list, a1_pos="BL"):
    
    if len(pieces_list) != 64:
        raise ValueError("Input pieces list must be of length 64")

    board = [pieces_list[ind:ind + 8] for ind in range(0, 64, 8)]
    board = rotate_board_image2fen(board, a1_pos)
    return board


def board_to_list(board):
    
    return [pos for row in board for pos in row]


def is_white_square(list_pos):

    if not 0 <= list_pos <= 63:
        raise ValueError("List positions must be between 0 and 63")

    if list_pos % 16 < 8:  # Odd rows
        return list_pos % 2 == 0
    else:  # Even rows
        return list_pos % 2 == 1


def rotate_board_fen2image(board, a1_pos):
    if a1_pos == "BL":
        return board
    if a1_pos == "BR":  # Counterclockwise rotation
        return list(map(list, zip(*board)))[::-1]
    if a1_pos == "TL":  # Clockwise rotation
        return list(map(list, zip(*board[::-1])))
    if a1_pos == "TR":  # 180 degree rotation
        tmp = list(map(list, zip(*board[::-1])))
        return list(map(list, zip(*tmp[::-1])))

    raise ValueError("a1_pos is not BL, BR, TL or TR")


def rotate_board_image2fen(board, a1_pos):
    
    if a1_pos == "BR":
        a1_pos = "TL"
    elif a1_pos == "TL":
        a1_pos = "BR"

    return rotate_board_fen2image(board, a1_pos)


def compare_fen(fen1, fen2):
    board1 = fen_to_board(fen1)
    board2 = fen_to_board(fen2)
    count = 0
    for i in range(8):
        for j in range(8):
            if board1[i][j] != board2[i][j]:
                count += 1
    return count
