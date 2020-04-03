"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""



def search(initial_board_configuration) :
    """ Takes the initial board configuration as input
        returns an action sequence that leads to a winning outcome"""

    # create an empty priority queue
    pq = PriorityQueue()

    #create the first node to be put into the heap, which does not have a parent or a move that led to it
    origin_node = Node(origin_node, null, null)

    #add origin_node to heap
    pq.heappush(origin_node)

    while (pq.get_length() > 0) :
        current = pq.pop()

        pass #continue to generate more nodes, look for a solution node






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

                # if a black token is found on board, return False
                if (x,y) in board : 
                    if board[(x,y)].col == "b" :
                        return False

        # there are no more black pieces on the board, so return True
        return True
        
    """ contains:
    
    pointer to parent node? does python use pointers?
    depth of node? -> only needed with certain search strategies
    what move led to this node? -> to help us backtrack what action sequence led to this node """




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

    def __init__(self) :
        self.priorityqueue = []

    #method borrowed from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
    def heappush(self, node) :
        """ Push item onto heap, maintain the heap invariant """
        heap.append(node)
        _siftdown(heap, 0, len(heap)-1)

    #method borrowed from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
    """ 'heap' is a heap at all indices >= startpos, except possibly for pos.  pos
    # is the index of a leaf with a possibly out-of-order value.  Restore the
    # heap invariant."""
    def _siftdown(self, startpos, pos):
        newitem = self.priorityqueue[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.priorityqueue[parentpos]
            if compare_depth_nodes(newitem, parent): #if newitem has greater depth than parent, continue to sift through heap
                self.priorityqueue[pos] = parent
                pos = parentpos
                continue
            break
        self.priorityqueue[pos] = newitem
            
    
    def get_length(self) :
        return len(self.priorityqueue)

    #modified method from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
    def pop(self) :
        """ Returns the next node with smallest depth, maintains the heap """
        lastelt = self.priorityqueue.pop()
        if self.priorityqueue:
            returnitem = self.priorityqueue[0]
            self.priorityqueue[0] = lastelt
            _siftup(self.priorityqueue, 0)
        else: 
            returnitem = lastelt
        return returnitem

        
    #modified method from https://github.com/python/cpython/blob/ba8a2bcebfdb41acafea9a195e45e9d177dc216f/Lib/heapq.py#L140
    def _siftup(self, pos):
        endpos = len(self.priorityqueue)
        startpos = pos
        newitem = self.priorityqueue[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not compare_depth_nodes(self.priorityqueue[childpos], self.priorityqueue[rightpos]):
                childpos = rightpos
            # Move the smaller child up.
            self.priorityqueue[pos] = self.priorityqueue[childpos]
            pos = childpos
            childpos = 2*pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self.priorityqueue[pos] = newitem
        _siftdown(self.priorityqueue, startpos, pos)

