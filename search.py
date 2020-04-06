"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""

import util as u

#from collections import deque AIMA
#from utils import * AIMA
from collections import defaultdict
from game import Piece, BLACK, WHITE, MOVE, BOOM
import numpy as np
import game as g



# AIMA class
class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1



# ______________________________________________________________________________

class Expendibots(Problem) : 
    """ The problem of playing Expendibots. It is played on a 8*8 board with black and white
    tiles, and we always play the white player. We are the only ones that get to do actions, the
    black player is static. A state is represented by a dict with the coordinates on the board as keys
    and a tuple containing the number of tokens and the colour of the tokens (col, h) as the value."""

    #the below functions are just an example of the way 8-puzzle was implemented as a problem. 

    def __init__(self, board, goal= None):
        """ Define goal state and initialize a problem """
        super().__init__(board, goal)
        self.board = board
        self.goal = goal

    def __copy__(self):
        return Expendibots(self.board, None)


    def actions(self, board):
        """ Return the actions that can be executed in the given state.
        The result would be a list of Actions"""

        possible_actions = []

        for key in board :
            #for each white token
            if board[key].col == WHITE:
                
                #one possible action is to boom the white token
                boom = Action(BOOM, 1, key, None)
                possible_actions.append(boom)

                #for 1..n number of tokens to be moved
                for n in range(1, board[key].h + 1) :
                    
                    # for each coordinate within range
                    for x in range(key[0] - board[key].h, key[0] + board[key].h + 1) :
                        for y in range(key[1] - board[key].h, key[1] + board[key].h + 1) :
                            
                            #if move is valid, add it to the possible_actions
                            if g.valid_move(n, key, (x,y), board) :
                                possible_actions.append(Action(MOVE, n, key, (x,y)) )
                                

        return possible_actions

    
    def result(self, action, board):
        """Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        my_type = action.action_type
        local_board = board.copy()

        if my_type == BOOM :
            return g.boom(action.loc_a, local_board)

        else:
            return g.move_token(action.n, action.loc_a, action.loc_b, local_board)



    def goal_test(self, board):
        """ Given a state of the board, return True if state is a goal state (no remaining black tokens) or False, otherwise """

        for token in board: 
            if board[token].col == BLACK: 
                return False

        return True

    
    def h(self, node):
        white_counter = 12
        black_counter = 0

        """ The search function chooses the node with the smallest heuristic value first. 
        We want to explore nodes with the minimum number of black tokens first and the highest number of white tokens? 
        
        """
        # h decreases the more white tokens are on the board, and increases the more black tokens are on the board

        for key in self.board: 
            if self.board[key].col == BLACK:
                black_counter += self.board[key].h 
            else:
                white_counter -= self.board[key].h 

        h = white_counter + black_counter

        return h




# ______________________________________________________________________________


#AIMA class
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0, repeats = 0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        self.repeats = repeats
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)


    
    def expand(self, problem, board):
        """List the nodes reachable in one step from this node."""
        children = []
        for action in problem.actions(board):
            action.print_action()
            child = self.child_node(problem, action)
            children.append(child)
        return children


    def child_node(self, problem, action):
        """Given a current problem and an action, this func generates the next node and returns that"""
        next_state = problem.result(action, problem.board)
        next_node = Node(next_state, self, action, 0)
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________

#AIMA function
def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = u.memoize(h or problem.h, 'h')

    #stores all the nodes that we generate, used to count duplicate states
    generated_nodes = {}


    def RBFS(problem, node, flimit):

        #If a node's state is a goal state, return node
        if problem.goal_test(node.state):
            return node, 0  # (The second value is immaterial)
        
        #This node isn't the goal, so expand on successors
        successors = node.expand(problem, problem.board)

        # if there are no successors, return None
        if len(successors) == 0:
            return None, np.inf

        # for each successor, calculate a heuristic value? 
        for s in successors:
            s.f = max(h(s), node.f)
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = np.inf
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.board)
    node.f = h(node)
    result, bestf = RBFS(problem, node, np.inf)
    return result



# ______________________________________________________________________________


class Action : 

    # actiontype is assumed to be either the constant MOVE or BOOM
    def __init__(self, action_type, n, loc_a, loc_b=None):
        self.action_type = action_type
        self.loc_a = loc_a
        self.n = n
        self.loc_b = loc_b
        
    def print_action(self) :
        if self.action_type == MOVE :
            u.print_move(self.n, self.loc_a[0], self.loc_a[1], self.loc_b[0], self.loc_b[1])
        else: 
            u.print_boom(self.loc_a[0], self.loc_a[1])




def hash_dict(my_dict):
    """
    Uses a frozen set to return a hash of the dictionary
    :param my_dict: provided dictionary
    :return: hash
    """
    return hash(frozenset(my_dict.items()))


def four_recurrences(rec_tracker):
    if 4 in rec_tracker.values():
        return True
    else:
        return False
