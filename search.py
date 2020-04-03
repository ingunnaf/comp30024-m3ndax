"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""


class Node:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
    """ contains:
    game board configuration 
    bool -> have we won? 
    maybe some heuristic function that tries to calculate how close we are to winning?
    pointer to parent node? does python use pointerS?
    depth of node? depends on search strategy
    what move led to this node? -> to help us backtrack what action sequence led to this node """



