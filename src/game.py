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

