"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""



def search(initial_board_configuration) :
    """ Takes the initial board configuration as input
        returns an action sequence that leads to a winning outcome"""

    # create an empty heap
    heap = []

    #create the first node to be put into the heap, which does not have a parent or a move that led to it
    origin_node = Node(origin_node, null, null)

    #add origin_node to heap
    heappush(heap, origin_node)

    
    pass

#this function is borrowed from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
def heappush(heap, node) :
    """ Push item onto heap, maintain the heap invariant """
    heap.append(node)
    _siftdown(heap, 0, len(heap)-1)


#this function is borrowed from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
""" 'heap' is a heap at all indices >= startpos, except possibly for pos.  pos
# is the index of a leaf with a possibly out-of-order value.  Restore the
# heap invariant."""
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if compare_depth_nodes(newitem, parent): #if newitem has greater depth than parent, continue to sift through heap
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem


def compare_depth_nodes(newitem, parent):
    """ Returns true if newitem has smaller depth than the parent node"""
    if (newitem.depth < parent. depth) :
        return True
    else :
        return False


class Node:
    """ Represents a state of the game, connected to other nodes by Moves 
        Contains
        """

    def __init__(self, parent_node=null, move):
        self.depth = parent.depth + 1 #depth of the node in the search tree, represents number of moves away from current state 
        self.parent_node = parent_node
        self.move = move
        self.board_configuration = board
        
        

    """ This function needs to be called to update our have_won bool value each time we create a new node"""
    def have_won() :

        # loops through all coordinates on the board
        for x in range(0,8) :
            for y in range(0,8) :

                # if there are any remaining black tokens, return False
                if (x,y) in board : 
                    if board[(x,y)].col == "b" :
                        return False

        # there are no more black pieces on the board, so return True
        return True
        
    """ contains:
    game board configuration 
    bool -> have we won? 
    need to create a  heuristic function that tries to calculate how close we are to winning?
    pointer to parent node? does python use pointers?
    depth of node? -> only needed with certain search strategies
    what move led to this node? -> to help us backtrack what action sequence led to this node """

<<<<<<< HEAD

class Move:
    """ A Move serves as an edge in the search tree and stores information about the move that connects two nodes
        n = number of tokens moved
        a = where a token was moved from
        b = where a token was moved to
        boom = boolean value that stores whether or not this Move is a boom
    """

    def __init__(self, n, a, b, boom=False) :
        self.n = n
        self.a = a
        self.b = b
        self.boom = boom
        pass



class PriorityQueue: 

    def __init__(self, max_size) :
        self.max_size = max_size
        #funcs we need to write: 
        # put (enqueue a node)
        # get 
        