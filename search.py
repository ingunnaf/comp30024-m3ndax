"""
This module contains functions and data types for the creation and searching of a game-state tree.
These functions are used to find the a winning set of moves
"""

from util import *
from numpy import *
from game import *
import copy
import sys
from collections import deque, Counter
import numpy as np


# TODO check that the repeats counting functionality works as intended
#  -> my thought was that each node would store the number of times the state (board) it stores has been
#  repeateded previously on the path to that node, and that each time we pop a new node from the queue,
#  we update the number of repeats, and if it has 4 or more, we just skip that node and continue the loop

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
        # Not relevant to BFS
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


# ______________________________________________________________________________

class Expendibots(Problem):
    """ The problem of playing Expendibots. It is played on a 8*8 board with black and white
    tiles, and we always play the white player. We are the only ones that get to do actions, the
    black player is static. A state is represented by a dict with the coordinates on the board as keys
    and a tuple containing the number of tokens and the colour of the tokens (col, h) as the value."""

    def __init__(self, board, goal=create_board()):
        """ Define goal state and initialize a problem """
        super().__init__(board, goal)
        self.board = board
        self.goal = goal

    def actions(self, board):
        """ Return the actions that can be executed in the given state.
        The result would be a list of Actions"""

        possible_actions = []

        for key in board:
            # for each white token
            if board[key].col == WHITE:

                # one possible action is to boom the white token 
                # #TODO check if there are any black tokens around it, if there aren't don't append this boom
                boom = Action(BOOM, 1, key, None)
                possible_actions.append(boom)

                my_range = board[key].h
                # for 1..n number of tokens to be moved
                for n in range(1, board[key].h + 1):

                    # for each coordinate within range
                    for x in range(key[0] - my_range, key[0] + my_range + 1):
                        for y in range(key[1] - my_range, key[1] + my_range + 1):

                            # if move is valid, add it to the possible_actions
                            if valid_move(n, key, (x, y), board):
                                possible_actions.append(Action(MOVE, n, key, (x, y)))

        return possible_actions

    def result(self, action, board):
        """Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        my_type = action.action_type
        local_board = copy.deepcopy(board)

        if my_type == BOOM:
            return boom_piece(action.loc_a, local_board)  # returns a new boomed board

        else:
            return move_token(action.n, action.loc_a, action.loc_b, local_board)  # returns a new moved board

    def goal_test(self, board):
        """ Given a state of the board, return True if state is a goal state (no remaining black tokens) or False, otherwise """

        for token in board:
            if board[token].col == BLACK:
                return False

        return True

    def h(self, node):
        white_counter = 12
        black_counter,  white_piece_density, black_to_white_distance = 0
        WEIGHT = 2
        """ The search function chooses the node with the smallest heuristic value first. 
        We want to explore nodes with the minimum number of black tokens first and the highest number of white tokens? 
        """
        # h decreases the more white tokens are on the board, and increases the more black tokens are on the board

        for key1 in node.state:

            if node.state[key].col == BLACK:
                # count the number of remaining black pieces
                black_counter += node.state[key].h

                # compare against other pieces
                for key2 in node.state:
                    # skip if the same piece
                    if key1 == key2:
                        pass
                    # otherwise if the second key is white
                    elif node.state[key].col == WHITE:
                        # calculate distances between black and white pieces
                        black_to_white_distance += manhat_dist(key1, key2)
                    # otherwise calculate black
                    else:
                        continue

            else:
                white_counter -= node.state[key].h

        print(black_to_white_distance)

        return white_counter + black_counter + WEIGHT * black_to_white_distance


# ______________________________________________________________________________


# AIMA class
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, h=0, parent=None, action=None, depth=0, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.h = self.heuristic()  # heuristic value of the node, not dependent on path, only depends on the # black&white tokens on board
        self.path_cost = path_cost
        self.repeats = self.repeated_states()  # repeats = 0 if this is the first version of this state, repeats = 1 if there are two duplicate nodes
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def heuristic(self):
        white_counter = 12
        black_counter = 0
        black_to_white_distance = 0
        WEIGHT = 1
        """ The search function chooses the node with the smallest heuristic value first. 
        We want to explore nodes with the minimum number of black tokens first and the highest number of white tokens? 
        """
        # h decreases the more white tokens are on the board, and increases the more black tokens are on the board

        for key1 in self.state:

            if self.state[key1].col == BLACK:
                # count the number of remaining black pieces
                black_counter += self.state[key1].h

                # compare against other pieces
                for key2 in self.state:
                    # skip if the same piece
                    if key1 == key2:
                        pass
                    # otherwise if the second key is white
                    elif self.state[key2].col == WHITE:
                        # calculate distances between black and white pieces
                        black_to_white_distance += manhat_dist(key1, key2)
                    # otherwise calculate black
                    else:
                        continue

            else:
                white_counter -= self.state[key1].h

        # print(black_to_white_distance)

        return WEIGHT * black_to_white_distance

    def expand(self, problem, board):
        """List the nodes reachable in one step from this node."""
        children = []
        for action in problem.actions(board):
            # action.print_action()  # ah so here is where the print statement is! -> it reveals that all the same actions are generated repeatedly
            child = self.child_node(problem, action)

            # check number of repeats prior to appending child to children
            child.repeats = child.repeated_states()
            if not (child.repeats > 3 or child.depth > 250):  # remove those that repeat a state four times
                children.append(child)
            else:
                # print("4 repeated states detected! Node removed. ")
                continue
                # it never prints this statement although I have counted the number of repeats manually so the repeats function is definitely not working properly

        return children

    def child_node(self, problem, action):
        """Given a current problem and an action, this func generates the next node and returns that"""
        next_state = problem.result(action, self.state)  # generates a new board state
        h = 0  # not needed
        next_node = Node(next_state, h, self, action, 0)  # creates a new node
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            # print(node.__repr__())
            node = node.parent
        return list(reversed(path_back))

    def repeated_states(self):
        """Return the number of times the state of current node has been repeated previously"""
        node = self
        # stores initial state to compare other nodes states to
        this_state = self.state

        node = node.parent

        # at first finding of an equal node state, return the number of repeats stored in that node
        while node:
            if dict_equal(node.state, this_state):
                return node.repeats + 1
            node = node.parent
        return 0

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and dict_equal(self.state, other.state)

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        hash(frozenset(self.state.items()))


# ______________________________________________________________________________

# AIMA function
def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0  # (The second value is immaterial)
        successors = node.expand(problem, problem.board)
        if len(successors) == 0:
            return None

        while True:
            # Order by lowest heuristic value
            successors.sort(key=lambda node: node.h)
            best = successors[0]
            if best.h > flimit:
                return None
            if len(successors) > 1:
                alternative = successors[1].h
                print(alternative)
            else:
                alternative = inf
                print(alternative)

            result = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result

    h = 0
    node = Node(problem.board, h)
    result = RBFS(problem, node, inf)
    return result


# ______________________________________________________________________________


class Action:

    # actiontype is assumed to be either the constant MOVE or BOOM
    def __init__(self, action_type, n, loc_a, loc_b=None):
        self.action_type = action_type
        self.loc_a = loc_a
        self.n = n
        self.loc_b = loc_b

    def print_action(self):
        if self.action_type == MOVE:
            print_move(self.n, self.loc_a[0], self.loc_a[1], self.loc_b[0], self.loc_b[1])
        else:
            print_boom(self.loc_a[0], self.loc_a[1])


def dict_equal(dict1, dict2):
    d1_keys = set(dict1.keys())
    d2_keys = set(dict2.keys())

    # continue only if both dicts contain the same keys
    if not (d1_keys.issubset(d2_keys) and d2_keys.issubset(d1_keys)):
        return False

    # continue only if all the keys correspond to the same values
    for key in dict1.keys():
        if not (dict1[key] == dict2[key]):
            return False

    # return True if the dicts passed the checks
    return True


def breadth_first_tree_search(problem):
    """
    [Figure 3.7]
    Search the shallowest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    """
    # stores explored nodes
    # explored_states = set()
    # to store all nodes 
    explored = []

    frontier = deque([Node(problem.board)])  # FIFO queue

    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            # print("solution node found")
            return node

        explored.append(node)
        # print(node.__repr__())
        frontier.extend(node.expand(problem, node.state))

    print("why can't we find the solution :((( ")
    return None

# ______________________________________________________________________________

def depth_limited_search(problem, limit=250):
    """[Figure 3.17]"""

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem, node.state):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    """[Figure 3.18]"""
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result

# ______________________________________________________________________________

def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0  # (The second value is immaterial)
        successors = node.expand(problem, node.state)
        if len(successors) == 0:
            return None, np.inf
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
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

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, np.inf)
    return result