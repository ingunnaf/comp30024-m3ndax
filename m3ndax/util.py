# TODO: Add or move utility functions here

# TODO:put create_board method into expendibots class
def create_board(black_start_squares, white_start_squares) :
    board = dict()
    for xy in black_start_squares:
        board[xy] = Piece(BLACK, 1)
    for xy in white_start_squares:
        board[xy] = Piece(WHITE, 1)
    return board

# TODO:put boom method into expendibots class
def boom(origin, my_board):

    x, y = origin[0], origin[1]
    my_range = 1

    del my_board[origin]

    right_limit = x + my_range + 1
    left_limit = x - my_range
    up_limit = y + my_range + 1
    down_limit = y - my_range

    for i in range(left_limit, right_limit):
        for j in range(down_limit, up_limit):
            if (i, j) in my_board:
                boom((i,j), my_board)

    return my_board

# TODO:put move_token method into expendibots class
def move_token(n, a, b, board):
        ret_board = copy.deepcopy(board)
        # check if move is valid
        """if not valid_move(n, a, b, board):
            return board""" #i commented this out because at the moment, we don't need to validate
            #the action given to us for update method in player class

        # handle case where there is already a token at loc b (stack new tokens on top)
        if b in ret_board:
            current_height_b = ret_board[b].h
            new_height_b = current_height_b + n
            ret_board[b] = Piece("w", new_height_b)
        else:  # loc b has no tokens yet so we can just put our new tokens there
            ret_board[b] = Piece("w", n)

        # handle potential remaining tokens at loc a
        current_height_a = ret_board[a].h
        new_height_a = current_height_a - n
        if new_height_a == 0:
            # no more tokens left at loc a
            del ret_board[a]
        else:
            ret_board[a] = Piece("w", new_height_a)

        # done
        return ret_board



def print_board(board_dict, message="", unicode=False, compact=True, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:
    board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
        and printable objects (e.g. strings, numbers) as values. This function
        will arrange these printable values on the grid and output the result.
        Note: At most the first 3 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    unicode -- True if you want to use non-ASCII symbols in the board
        visualisation (see below), False to use only ASCII symbols.
        Default is False, since the unicode symbols may not agree with some
        terminal emulators.
    compact -- True if you want to use a compact board visualisation, with
        coordinates along the edges of the board, False to use a bigger one
        with coordinates alongside the printable information in each square.
        Default True (small board).
    
    Any other keyword arguments are passed through to the print function.
    """
    if unicode:
        if compact:
            template = """# {}
#    ┌───┬───┬───┬───┬───┬───┬───┬───┐
#  7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  6 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  5 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  4 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  3 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  2 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  1 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    └───┴───┴───┴───┴───┴───┴───┴───┘
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,7 │ 1,7 │ 2,7 │ 3,7 │ 4,7 │ 5,7 │ 6,7 │ 7,7 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,6 │ 1,6 │ 2,6 │ 3,6 │ 4,6 │ 5,6 │ 6,6 │ 7,6 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,5 │ 1,5 │ 2,5 │ 3,5 │ 4,5 │ 5,5 │ 6,5 │ 7,5 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,4 │ 1,4 │ 2,4 │ 3,4 │ 4,4 │ 5,4 │ 6,4 │ 7,4 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,3 │ 1,3 │ 2,3 │ 3,3 │ 4,3 │ 5,3 │ 6,3 │ 7,3 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,2 │ 1,2 │ 2,2 │ 3,2 │ 4,2 │ 5,2 │ 6,2 │ 7,2 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,1 │ 1,1 │ 2,1 │ 3,1 │ 4,1 │ 5,1 │ 6,1 │ 7,1 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,0 │ 1,0 │ 2,0 │ 3,0 │ 4,0 │ 5,0 │ 6,0 │ 7,0 │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘"""
    else:
        if compact:
            template = """# {}
#    +---+---+---+---+---+---+---+---+
#  7 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  6 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  5 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  4 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  3 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  2 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  1 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  0 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,7 | 1,7 | 2,7 | 3,7 | 4,7 | 5,7 | 6,7 | 7,7 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,6 | 1,6 | 2,6 | 3,6 | 4,6 | 5,6 | 6,6 | 7,6 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,5 | 1,5 | 2,5 | 3,5 | 4,5 | 5,5 | 6,5 | 7,5 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,4 | 1,4 | 2,4 | 3,4 | 4,4 | 5,4 | 6,4 | 7,4 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,3 | 1,3 | 2,3 | 3,3 | 4,3 | 5,3 | 6,3 | 7,3 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,2 | 1,2 | 2,2 | 3,2 | 4,2 | 5,2 | 6,2 | 7,2 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,1 | 1,1 | 2,1 | 3,1 | 4,1 | 5,1 | 6,1 | 7,1 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,0 | 1,0 | 2,0 | 3,0 | 4,0 | 5,0 | 6,0 | 7,0 |
# +-----+-----+-----+-----+-----+-----+-----+-----+"""
    # board the board string
    coords = [(x, 7 - y) for y in range(8) for x in range(8)]
    cells = []
    for xy in coords:
        if xy not in board_dict:
            cells.append("   ")
        else:
            colour = str(board_dict[xy].col)
            height = str(board_dict[xy].h)
            piece = (colour + height + "")
            cells.append(piece[:3].center(3))
            # cells.append(str(board_dict[xy])[:3].center(3))
    # print it
    print(template.format(message, *cells), **kwargs)