import copy
from collections import namedtuple
import numpy as np

# NamedTuple definitions
GameState = namedtuple('GameState', 'to_move, utility, board, moves')
Piece = namedtuple('P', 'col h')  # col = colour, h = height

# Static Variable definitions
BLACK = 'black'
WHITE = 'white'
BOOM = "BOOM"
MOVE = "MOVE"
UTILITYPLACEHOLDER = 0

_BLACK_START_SQUARES = [(0, 7), (1, 7), (3, 7), (4, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (3, 6), (4, 6), (6, 6), (7, 6)]
_WHITE_START_SQUARES = [(0, 1), (1, 1), (3, 1), (4, 1), (6, 1), (7, 1),
                        (0, 0), (1, 0), (3, 0), (4, 0), (6, 0), (7, 0)]


# AIMA library function
def alpha_beta_cutoff_search(state, game, eval_fn=None, d=4, cutoff_test=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    """
    def eval_fn(state, game): 
        ourcolour = state.to_move

        if ourcolour == BLACK:
            othercolour = WHITE
        else:
            othercolour = BLACK

        # if we have won in this state, return 100
        if game.terminal_test(state) : 
            winner = whowon(state, game)
            if winner == ourcolour: 
                return 100
            # if opponent has won in this state, return -100
            else if winner == othercolour:
                return -100
        
        # otherwise, return # of our tokens - # of their tokens

        board = state.board
        ntokensleft = n_pieces(board, ourcolour)
        nothertokensleft = n_pieces(board, othercolour)
        # returns positive value if we have more tokens left than opponent
        return nothertokensleft - ntokensleft"""

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def whowon(state, game):
    hasblack = False  # stores whether or not there are any black tokens left
    haswhite = False  # stores whether or not there are any white tokens left

    board = state.board

    for key in board:
        if board[key].col == WHITE:
            haswhite = True
        if board[key].col == BLACK:
            hasblack = True
    if (hasblack and not haswhite):
        return BLACK
    if (haswhite and not hasblack):
        return WHITE
    else:
        return None


# ______________________________________________________________________________
# Algorithm taken from AIMA library: https://github.com/aimacode/aima-python/blob/master/games.py
def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


# AIMA class, examples of how to implement it on https://github.com/aimacode/aima-python/blob/master/games.py
class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class Expendibots(Game):
    """ Note to self/both of us : Given that the game class uses the state passed to all these 
    functions to determine things like whose turn it is to move, our previous version of a state that
    only stored the board without information like whose turn it is, is insufficient. I think it might
    be enough to just add something to the game state that tracks whose turn it is. Can't think of any 
    other missing information at the moment. """

    """ Implements the game class to model Expendibots """

    def __init__(self, player):
        # Player designates the colour of the player
        self.player = player

    def actions(self, state):
        """Return a list of the allowable moves at this point."""

        board = state.board
        possible_actions = []

        for key in board:
            # for each players tokens whose turn it is
            if board[key].col == self.player:

                # one possible action is to boom the white token
                boom = (BOOM, key)
                possible_actions.append(boom)

                my_range = board[key].h
                # for 1..n number of tokens to be moved
                for n in range(1, board[key].h + 1):

                    # for each coordinate within range
                    for x in range(key[0] - my_range, key[0] + my_range + 1):
                        for y in range(key[1] - my_range, key[1] + my_range + 1):

                            # if move is valid, add it to the possible_actions
                            if valid_move(n, key, (x, y), board):
                                move = (MOVE, n, key, (x, y))
                                possible_actions.append(move)

        return possible_actions

    def result(self, state, move):
        """Return the state that results from making a move from a state."""

        moveType = move[0]

        local_board = copy.deepcopy(state.board)

        if moveType == BOOM:

            return GameState(self.to_move(state), self.utility(state, self.player), boom_piece(move[1], local_board),
                             None)  # returns a new boomed board

        else:

            return GameState(self.to_move(state), self.utility(state, self.player),
                             move_token(move[1], move[2], move[3], local_board),
                             None)  # returns a new moved board

    def utility(self, state, player):
        """Returns a negative value if we have lost, a positive value if we won, and a 0 if it is a tie. """
        # TODO figure out how to use utility function? :-) !!!

        ourcolour = state.to_move

        if ourcolour == BLACK:
            othercolour = WHITE
        else:
            othercolour = BLACK

        # if we have won in this state, return 100
        if self.terminal_test(state):
            winner = whowon(state, self)
            if winner == ourcolour:
                return 100
            # if opponent has won in this state, return -100
            elif winner == othercolour:
                return -100

        # otherwise, return # of our tokens - # of their tokens (if it is a tie, it will return 0)
        board = state.board
        ntokensleft = n_pieces(board, ourcolour)
        nothertokensleft = n_pieces(board, othercolour)
        # returns positive value if we have more tokens left than opponent
        return nothertokensleft - ntokensleft

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        hasblack = False  # stores whether or not there are any black tokens left
        haswhite = False  # stores whether or not there are any white tokens left

        board = state.board

        for key in board:
            if board[key].col == WHITE:
                haswhite = True
            if board[key].col == BLACK:
                hasblack = True
        # 1) returns true if there are still black tokens but no white ones (BLACK WON)
        # 2) returns true if there are still white tokens but no black ones (WHITE WON)
        # 3) returns true if there are NO white and NO black tokens left (TIE)
        return (hasblack and not haswhite) or (haswhite and not hasblack) or not (hasblack and haswhite)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        # print_board(state.board)
        print(state.board)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


######################################## functions relating to game and board below ####################################
def valid_move(n, a, b, board):
    # not valid if there is no token at a
    if a not in board:
        return False

    # not valid if a == b (the token isn't moving)
    if (a == b):
        return False

    # not valid if move is diagonal
    if (a[0] != b[0]) and (a[1] != b[1]):
        # print("you cannot move diagonally in a single move")
        return False

    # not valid if the token at loc a is black
    if a in board:
        if board[a].col == BLACK:
            # print("you can't move a black token")
            return False

    # not valid if less than n tokens at loc a
    if board[(a)].h < n:
        # print("you can't move more tokens than exist at loc a")
        return False

    # not valid if loc b is out of reach
    my_range = board[(a)].h
    dist = manhat_dist(a, b)
    if dist > my_range:
        # print("loc b is out of reach")
        return False

    # not valid if there is a black token at loc b
    if b in board:
        if board[b].col == BLACK:
            return False

    # invalid if loc a or loc b are not in valid range
    if a[0] not in range(0, 8):
        # print("loc a not on board")
        return False
    if a[1] not in range(0, 8):
        # print("loc a not on board")
        return False
    if b[0] not in range(0, 8):
        # print("loc b not on board")
        return False
    if b[1] not in range(0, 8):
        # print("loc b not on board")
        return False

    # has passed all the checks, so we return true
    return True


def valid_boom(origin, my_board):
    if origin[0] not in range(0, 8):
        print("x coordinate not in range")
        return False
    if origin[1] not in range(0, 8):
        print("y coordinate not in range")
        return False
    if origin not in my_board:
        print("boom origin location has no token on it")
        return False

    return True


def boom(origin, my_board):
    if not valid_boom(origin, my_board):
        raise RuntimeError("Invalid Boom")

    else:
        x, y = origin[0], origin[1]
        my_range = 1

        del my_board[origin]

        right_limit = x + my_range + 1
        left_limit = x - my_range
        up_limit = y + my_range + 1
        down_limit = y - my_range

        for i in range(left_limit, right_limit):
            for j in range(down_limit, up_limit):
                if (i, j) in my_board:
                    boom((i, j), my_board)

    return my_board


def boom_piece(origin, init_board):
    if not valid_boom(origin, init_board):
        raise RuntimeError("Invalid Boom Move")

    ret_board = copy.deepcopy(init_board)
    boom(origin, ret_board)
    return ret_board


def move_token(n, a, b, board):
    ret_board = copy.deepcopy(board)
    # check if move is valid
    """if not valid_move(n, a, b, board):
            return board"""  # i commented this out because at the moment, we don't need to validate
    # the action given to us for update method in player class

    # handle case where there is already a token at loc b (stack new tokens on top)
    if b in ret_board:
        current_height_b = ret_board[b].h
        new_height_b = current_height_b + n
        ret_board[b] = Piece("w", new_height_b)
    else:  # loc b has no tokens yet so we can just put our new tokens there
        ret_board[b] = Piece("w", n)

    # handle potential remaining tokens at loc a
    current_height_a = ret_board[a].h
    new_height_a = current_height_a - n
    if new_height_a == 0:
        # no more tokens left at loc a
        del ret_board[a]
    else:
        ret_board[a] = Piece("w", new_height_a)

    # done
    return ret_board


def create_board(black_start_squares, white_start_squares):
    board = dict()
    for xy in black_start_squares:
        board[xy] = Piece(BLACK, 1)
    for xy in white_start_squares:
        board[xy] = Piece(WHITE, 1)
    return board


#################### functions that are not in use at the moment, just here for reference: #############
def manhat_dist(a, b):
    """returns the number of cardinal moves a piece would have to make to reach the other piece
    """
    x1, x2 = a[0], b[0]
    y1, y2 = a[1], b[1]

    dist = (abs(x1 - x2)) + (abs(y1 - y2))

    return dist


def n_pieces(board, piece_col):
    """
    Counts how many pieces of the given colour are on the board
    """
    coords = [(x, 7 - y) for y in range(8) for x in range(8)]

    cnt = 0

    for xy in coords:
        if xy in board and board[xy].col == piece_col:
            cnt += board[xy].h

    return cnt


# define initial board
INIT_BOARD = create_board(_BLACK_START_SQUARES, _WHITE_START_SQUARES)
