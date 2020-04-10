"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""

import util as u

#from collections import deque AIMA
#from utils import * AIMA
from collections import defaultdict, deque

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

    def __init__(self, board, goal=None):
        """ Define goal state and initialize a problem """
        super().__init__(board, goal)
        self.board = board
        self.goal = goal

    """def __copy__(self):
        return Expendibots(self.board, None)"""


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
                    for x in range(key[0] - 1, key[0] + 2) :
                        for y in range(key[1] - 1, key[1] + 2) :
                            
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
            return g.boom(action.loc_a, local_board) #returns a new boomed board

        else:
            return g.move_token(action.n, action.loc_a, action.loc_b, local_board) #returns a new moved board

    """
    def perform_action(self, action) :
        #Given state and action, perform action to the state

        my_type = action.action_type

        if my_type == BOOM :
            new_board = g.boom(action.loc_a, self.board)
            self.board = new_board
            
        else:
            new_board = g.move_token(action.n, action.loc_a, action.loc_b, self.board)
            self.board = new_board
            
    """

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

    def __init__(self, state, h=0, parent=None, action=None, depth = 0, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.h = self.heuristic() #heuristic value of the node, not dependent on path, only depends on the # black&white tokens on board
        self.path_cost = path_cost
        self.repeats = self.repeated_states()#repeats = 0 if this is the first version of this state, repeats = 1 if there are two duplicate nodes
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __eq__(self, node):
        return dict_equal(self.state, node.state)

    def heuristic(self):
        white_counter = 12
        black_counter = 0

        """ The search function chooses the node with the smallest heuristic value first. 
        We want to explore nodes with the minimum number of black tokens first and the highest number of white tokens? 
        
        """
        # h decreases the more white tokens are on the board, and increases the more black tokens are on the board

        for key in self.state: 
            if self.state[key].col == BLACK:
                black_counter += self.state[key].h 
            else:
                white_counter -= self.state[key].h 

        h = white_counter + black_counter

        return h
    
    def expand(self, problem, board):
        """List the nodes reachable in one step from this node."""
        children = []
        for action in problem.actions(board):
            action.print_action() #ah so here is where the print statement is! -> it reveals that all the same actions are generated repeatedly
            child = self.child_node(problem, action)
            children.append(child)
        return children


    def child_node(self, problem, action):
        """Given a current problem and an action, this func generates the next node and returns that"""
        next_state = problem.result(action, problem.board) #generates a new board state
        h = 0 #not needed
        next_node = Node(next_state, h, self, action, 0) #creates a new node
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

    def repeated_states(self):
        """Return the number of times the state of current node has been repeated previously"""
        node = self
        #stores initial state to compare other nodes states to 
        this_state = self.state

        node = node.parent

        # at first finding of an equal node state, return the number of repeats stored in that node
        while node:
            if dict_equal(node.state,this_state) :
                return node.repeats + 1
            node = node.parent
        return 0

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

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0  # (The second value is immaterial)
        successors = node.expand(problem, problem.board)
        if len(successors) == 0:
            return None

        for s in successors:
            s.repeats = s.repeated_states()
            if s.repeats == 2 : #remove those that repeat a state four times
                print(s.__repr__())
                successors.remove(s)
                print("4 repeated states detected! Node removed. ")
            elif s.depth > 250 :
                successors.remove(s)
        #check again if there are any successors left after removing nodes that have 4 repeated states
        if len(successors) == 0:
            return None

        while True:
            # Order by lowest heuristic value
            successors.sort(key=lambda node: node.h)
            best = successors[0]

            #perform action to board so that the new board is passed to the recurring function
            action = best.action
            board = problem.board #current_board
            if action.action_type == MOVE :
                board = g.move_token(action.n, action.loc_a, action.loc_b, board)
            else :
                board = g.boom(action.loc_a, board)
            problem = Expendibots(board)
            
            print(best.__repr__())
            if best.h > flimit:
                return None
            if len(successors) > 1:
                alternative = successors[1].h
                print(alternative)
            else:
                alternative = np.inf
                print(alternative)
            
            result = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result

    h = 0
    node = Node(problem.board, h)
    result = RBFS(problem, node, np.inf)
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




def dict_equal(dict1, dict2) : 

    d1_keys = set(dict1.keys())
    d2_keys = set(dict2.keys())

    #continue only if both dicts contain the same keys
    if not (d1_keys.issubset(d2_keys) and d2_keys.issubset(d1_keys)) :
        return False
    
    #continue only if all the keys correspond to the same values
    for key in dict1.keys() :
        if not (dict1[key] == dict2[key]) :
            return False
    
    #return True if the dicts passed the checks
    return True




def breadth_first_tree_search(problem):
    """
    [Figure 3.7]
    Search the shallowest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    """

    frontier = deque([Node(problem.board)])  # FIFO queue

    while frontier:
        node = frontier.popleft()
        print(node.__repr__())
        if problem.goal_test(node.state):
            print("solution node found")
            return node
        
        nboard = problem.board
        if node.depth != 0 :
            print("Hello")
            action = node.action
            if action.action_type == MOVE :
                nboard = g.move_token(action.n, action.loc_a, action.loc_b, nboard)
            else :
                nboard = g.boom(action.loc_a, nboard)
            problem = Expendibots(nboard)

        successors = node.expand(problem, problem.board)
        for s in successors: 
            print("S-node: " + str(s.__repr__()))
            print("Number of successor nodes: " + str(len(successors)))

        frontier.extend(node.expand(problem, problem.board))
        for fnode in frontier: 
            print("Number of nodes in frontier: " + str(len(frontier)))
            print("Fnode: " + str(fnode.__repr__()))

    print("why can't we find the solution :((( ")
    return None