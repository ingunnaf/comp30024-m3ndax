"""
This module contains functions and data types related to the playing of Expendibots
"""

from collections import namedtuple

# TODO: create reperesentation of game board. perhaps a 2d array of a struct/object which each 'point/square' storing color and height of the pieces there
Piece = namedtuple('Piece', 'colour height')

def create_board():
    '''A dictionary with (x, y) tuples as keys (x, y in range(8))
    and printable objects'''
    dict = {}
    return dict

def insert_data_from_JSON(JSON_data):
    """
    Process json input and return a struct representation of the board
    """
    board = create_board()
    # TODO:iterate and insert black pieces
    black_pieces = JSON_data['black']

    for piece in black_pieces:
        print(piece)
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = "bl" + str(h)


    # TODO: iterate and insert white pieces
    white_pieces = JSON_data['white']

    for piece in white_pieces:
        x_y = tuple(piece[1:])
        h = piece[0]
        board[x_y] = "wh" + str(h)

    return (board)


