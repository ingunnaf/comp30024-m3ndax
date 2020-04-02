"""
This module contains functions and data types related to the playing of Expendibots
"""

from collections import namedtuple

# create nametuple representing a piece
Piece = namedtuple('P', 'col h')

def create_board():
    '''A dictionary with (x, y) tuples as keys (x, y in range(8))
    and printable objects'''
    dict = {}
    return dict


def manhat_dist(a, b):
    #returns the number of cardinal moves a piece would have to make to reach the other piece
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]

    dist = (abs(x1-x2)) + (abs(y1-y2))

    return dist


def insert_data_from_JSON(JSON_data):
    """
    Process json input and return a dictionary representation of the board
    """
    board = create_board()

    # fetch black pieces
    black_pieces = JSON_data['black']

    # iterate through provided
    for piece in black_pieces:
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = Piece("b", h)

    # white pieces
    white_pieces = JSON_data['white']

    for piece in white_pieces:
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = Piece("w", h)

    return board


def valid_move(n, a, b, board) : 

    #not valid if move is diagonal
    if (a[0] != b[0]) and (a[1] != b[1]) :
        print("you cannot move diagonally in a single move")
        return False

    #not valid if the token at loc a is black
    if board[(a)].col == "b" :
        print("you can't move a black token")
        return False

    #not valid if less than n tokens at loc a 
    if board[(a)].h < n :
        print("you can't move more tokens than exist at loc a")
        return False

    #not valid if loc b is out of reach
    reach = board[(a)].h
    dist = manhat_dist(a,b)
    if (dist > reach) or (dist > n):
        print("loc b is out of reach")
        return False

    #not valid if there is a black token at loc b
    if b in board : 
        if board[b].col == "b" : 
            return False

    #invalid if loc a or loc b are not in valid range
    if a[0] not in range(0,8) :
        print("loc a not on board")
        return False
    if a[1] not in range(0,8) :
        print("loc a not on board")
        return False
    if b[0] not in range(0,8) :
        print("loc b not on board")
        return False
    if b[1] not in range(0,8) :
        print("loc b not on board")
        return False

    # has passed all the checks, so we return true
    return True


def move_token(n, a, b, board) :

    #check if move is valid
    if not valid_move(n, a, b, board) :
        print("Move is invalid")
        return board


    # handle case where there is already a token at loc b (stack new tokens on top)
    if b in board :
        current_height_b = board[b].h
        new_height_b = current_height_b + n
        board[b] = Piece("w", new_height_b)
    else: # loc b has no tokens yet so we can just put our new tokens there
        board[b] = Piece("w", n)


    #handle potential remaining tokens at loc a
    current_height_a = board[a].h
    new_height_a = current_height_a - n
    if new_height_a == 0 :
        #no more tokens left at loc a
        del board[a]
    else :
        board[a] = Piece("w", new_height_a)
        
    #done
    return board

def valid_boom(a, board) :

    #invalid if a is not on the board
    if a[0] not in range(8) :
        return False
    if a[1] not in range(8) :
        return False

    #invalid if there is no token at loc a
    if a not in board :
        return False
    
    #invalid if token at loc a is black
    if board[a].col == "b" :
        return False

    #if it passes tests, return true
    return True


def boom(origin, board) :

    if not valid_boom(origin, board) :
        print("Invalid boom")
        return board
    
    #stores coordinate-tuples of tokens that will be boomed
    booms = [] 
    booms.append(origin)

    while len(booms) > 0 :

        # remove next token to be boomed from booms
        next = booms.pop(-1)
        
        # get x and y-coordinates of next to be boomed
        x = int(next[0])
        y = int(next[1])

        # gets the range of the boom based on how many tokens are stacked in that location
        range = int(board[next].h)
        right_limit = int(x + range)
        left_limit = int(x - range)
        up_limit = int(y + range)
        down_limit = int(y - range)
        
        # loops through all coordinates within range of the boom to find new tokens to add to booms
        for i in list(range(left_limit, right_limit)) :
            for j in list(range(down_limit, up_limit)) :
                
                #if token is found within range, add to booms and delete token from the board_dict
                if ((i,j) in board): 
                    booms.append((i,j))
                    del board[(i,j)]

    return board

