"""
This module contains functions and data types related to the playing of Expendibots
"""

from collections import namedtuple
from search import manhat_dist as md

# create nametuple representing a piece
Piece = namedtuple('P', 'col h')

def create_board():
    '''A dictionary with (x, y) tuples as keys (x, y in range(8))
    and printable objects'''
    dict = {}
    return dict

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

def can_move(board, a, b):
    if (md(a, b) <= board[a].h) :
        return True
    else:
        return False

def valid_move(n, a, b, board) : 

    #not valid if move is diagonal
    if (a[0] != b[0]) && (a[1] != b[1]) :
        print("you cannot move diagonally in a single move")
        return false

    #not valid if the token at loc a is black
    if board[(a)].col == "b" :
        print("you can't move a black token")
        return false

    #not valid if less than n tokens at loc a 
    if board[(a)].h < n :
        print("you can't move more tokens than exist at loc a")
        return false

    #not valid if loc b is out of reach
    reach = board[(a)].h
    dist = manhat_dist(a,b)
    if (dist > reach) or (dist > n):
        print("loc b is out of reach")
        return false

    #not valid if there is a black token at loc b
    if b in board : 
        if board[b].col = "b" : 
            return false

    #invalid if loc a or loc b are not in valid range
    if a[0] not in range(0,8) :
        print("loc a not on board")
        return false
    if a[1] not in range(0,8) :
        print("loc a not on board")
        return false
    if b[0] not in range(0,8) :
        print("loc b not on board")
        return false
    if b[1] not in range(0,8) :
        print("loc b not on board")
        return false

    # has passed all the checks, so we return true
    return true


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
