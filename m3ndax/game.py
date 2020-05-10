import copy
from collections import namedtuple
import numpy as np
from m3ndax.util import print_board

# NamedTuple definitions
GameState = namedtuple('GameState', 'to_move, utility, board, moves')
Piece = namedtuple('P', 'col h') # col = colour, h = height

# Static Variable definitions
BLACK = 'black'
WHITE = 'white'
BOOM = "boom"
MOVE = "move"


# ______________________________________________________________________________
# Algorithm taken from AIMA library: https://github.com/aimacode/aima-python/blob/master/games.py
def expect_minmax(state, game):
    """
    [Figure 5.11]
    Return the best move for a player after dice are thrown. The game tree
    includes chance nodes along with min and max nodes."""

    player = game.to_move(state)

    def max_value(state):
        v = -np.inf
        for a in game.actions(state):
            v = max(v, chance_node(state, a))
        return v

    def min_value(state):
        v = np.inf
        for a in game.actions(state):
            v = min(v, chance_node(state, a))
        return v

    def chance_node(state, action):
        res_state = game.result(state, action)
        if game.terminal_test(res_state):
            return game.utility(res_state, player)
        sum_chances = 0
        num_chances = len(game.chances(res_state))
        for chance in game.chances(res_state):
            res_state = game.outcome(res_state, chance)
            util = 0
            if res_state.to_move == player:
                util = max_value(res_state)
            else:
                util = min_value(res_state)
            sum_chances += util * game.probability(chance)
        return sum_chances / num_chances

    # Body of expect_minmax:
    return max(game.actions(state), key=lambda a: chance_node(state, a), default=None)


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

    def play_game(self, *players):
        # TODO: figure out whether this method can be removed
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class Expendibots(Game):
    """ Note to self/both of us : Given that the game class uses the state passed to all these 
    functions to determine things like whose turn it is to move, our previous version of a state that
    only stored the board without information like whose turn it is, is insufficient. I think it might
    be enough to just add something to the game state that tracks whose turn it is. Can't think of any 
    other missing information at the moment. """

    """ Implements the game class to model Expendibots """

    def actions(self, state):
        """Return a list of the allowable moves at this point."""

        board = state.board
        possible_actions = []

        for key in board:
            # for each players tokens whose turn it is
            if board[key].col == state[0]:

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
        """ Also just copied from part A at the moment, needs to be modified"""
        # TODO modify this method to be used for part B instead of part A

        movetype = move[0]

        local_board = copy.deepcopy(state.board)

        if movetype == BOOM:
            # TODO: return game state in GameState format  'to_move, utility, board, moves'
            return boom_piece(move[1], local_board)  # returns a new boomed board

        else:
            return move_token(move[1], move[2], move[3], local_board)  # returns a new moved board

    def utility(self, state, player):
        """Returns a negative value if we have lost, a positive value if we won, and a 0 if it is a tie. """
        # TODO figure out how to use utility function? :-)
        ourcolour = player.colour
        board = state.board

        """ If there is at least one remaining token in our colour and the game has ended, we have won"""
        for key in board:
            if board[key].col == ourcolour:
                return 1
            else:
                # a token of another colour was found
                return -1
        # otherwise (if there no tokens of any colour) return neutral value 0
        return 0

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        black = False
        white = False

        board = state[2]

        for key in board:
            if board[key].col == WHITE:
                white = True
            if board[key].col == BLACK:
                black = True

        return black and white

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state[0]

    def display(self, state):
        """Print or otherwise display the state."""
        # TODO maybe use the printing methods provided to us in Part A to print state of the game?
        print_(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        # TODO implement this method. The stuff currently here is just copied from the abstract implementation of Game
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


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
