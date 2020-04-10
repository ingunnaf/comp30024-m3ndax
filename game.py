"""
This module contains functions and data types related to the playing of Expendibots
"""

from collections import namedtuple

# define static variables
BLACK = 'b'
WHITE = 'w'
BOOM = "boom"
MOVE = "move"

"""
create namedtuple representing a piece
where col represent the colour (either 'b' for black or 'w' for white)
and h is the height of the stack (minimum 1)
"""

Piece = namedtuple('P', 'col h')


def create_board():
    """
    A dictionary with (x, y) tuples as keys (x, y in range(8))
    and printable objects
    """
    board = {}
    return board


def manhat_dist(a, b):
    """returns the number of cardinal moves a piece would have to make to reach the other piece
    """
    x1, x2 = a[0], b[0]
    y1, y2 = a[1], b[1]

    dist = (abs(x1 - x2)) + (abs(y1 - y2))

    return dist


def insert_data_from_json(json_data):
    """
    Process json input and return a dictionary representation of the board
    """
    board = create_board()

    # fetch black pieces
    black_pieces = json_data['black']

    # iterate through provided
    for piece in black_pieces:
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = Piece(BLACK, h)

    # white pieces
    white_pieces = json_data['white']

    for piece in white_pieces:
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = Piece(WHITE, h)

    return board


def valid_move(n, a, b, board):
    # not valid if there is no token at a
    if a not in board:
        return False

    # not valid if a == b (the token isn't moving)
    if (a == b):
        return False

    # not valid if move is diagonal
    if (a[0] != b[0]) and (a[1] != b[1]):
        # print("you cannot move diagonally in a single move")
        return False

    # not valid if the token at loc a is black
    if a in board:
        if board[a].col == BLACK:
            # print("you can't move a black token")
            return False

    # not valid if less than n tokens at loc a
    if board[(a)].h < n:
        # print("you can't move more tokens than exist at loc a")
        return False

    # not valid if loc b is out of reach
    reach = board[(a)].h
    dist = manhat_dist(a, b)
    if (dist > reach) or (dist > n):
        # print("loc b is out of reach")
        return False

    # not valid if there is a black token at loc b
    if b in board:
        if board[b].col == BLACK:
            return False

    # invalid if loc a or loc b are not in valid range
    if a[0] not in range(0, 8):
        # print("loc a not on board")
        return False
    if a[1] not in range(0, 8):
        # print("loc a not on board")
        return False
    if b[0] not in range(0, 8):
        # print("loc b not on board")
        return False
    if b[1] not in range(0, 8):
        # print("loc b not on board")
        return False

    # has passed all the checks, so we return true
    return True


def move_token(n, a, b, board):
    # check if move is valid
    if not valid_move(n, a, b, board):
        return board

    # handle case where there is already a token at loc b (stack new tokens on top)
    if b in board:
        current_height_b = board[b].h
        new_height_b = current_height_b + n
        board[b] = Piece("w", new_height_b)
    else:  # loc b has no tokens yet so we can just put our new tokens there
        board[b] = Piece("w", n)

    # handle potential remaining tokens at loc a
    current_height_a = board[a].h
    new_height_a = current_height_a - n
    if new_height_a == 0:
        # no more tokens left at loc a
        del board[a]
    else:
        board[a] = Piece("w", new_height_a)

    # done
    return board


def valid_boom(origin, my_board):
    if origin[0] not in range(0, 8):
        print("x coordinate not in range")
        return False
    if origin[1] not in range(0, 8):
        print("y coordinate not in range")
        return False
    if origin not in my_board:
        print("origin not on board")
        return False

    return True


def boom_piece(origin, init_board):
    if not valid_boom(origin, init_board):
        raise RuntimeError("Invalid Boom Move")

    ret_board = init_board.copy()
    boom(origin, ret_board)
    return ret_board


def boom(origin, my_board):
    if not valid_boom(origin, my_board):
        raise RuntimeError("Invalid Boom")

    else:
        x, y = origin[0], origin[1]
        my_range = my_board[origin].h

        del my_board[origin]

        booms = []

        right_limit = x + my_range + 1
        left_limit = x - my_range
        up_limit = y + my_range + 1
        down_limit = y - my_range

        for i in range(left_limit, right_limit):
            for j in range(down_limit, up_limit):
                if (i, j) in my_board:
                    booms.append((i, j))

        for boomer in booms:
            boom(boomer, my_board)

    return my_board


def n_pieces(board, piece_col):
    """
    counts how many pieces of the given colour are on the board
    """
    coords = [(x, 7 - y) for y in range(8) for x in range(8)]

    cnt = 0

    for xy in coords:
        if xy in board:
            if board[xy].col == piece_col:
                cnt += board[xy].h

    return cnt
