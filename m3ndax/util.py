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

#TODO: create class to represent game state including who's turn it is