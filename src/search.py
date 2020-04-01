'''
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
'''

class Node:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data