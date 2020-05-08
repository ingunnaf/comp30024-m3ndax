

import copy
import itertools
import random
from collections import namedtuple

import numpy as np

from utils import vector_add

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


# ______________________________________________________________________________


def expect_minmax(state, game):
    """
    [Figure 5.11]
    Return the best move for a player after dice are thrown. The game tree
	includes chance nodes along with min and max nodes.
	"""
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

#AIMA class, examples of how to implement it on https://github.com/aimacode/aima-python/blob/master/games.py
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

        """ #TODO The below is just copied from Part A, need to modify to allow for game state to 
        store whose turn it is"""

        board = state.board
        possible_actions = []

        for key in board:
            # for each white token
            if board[key].col == WHITE:

                # one possible action is to boom the white token
                boom = ("BOOM", key)
                possible_actions.append(boom)

                my_range = board[key].h
                # for 1..n number of tokens to be moved
                for n in range(1, board[key].h + 1):

                    # for each coordinate within range
                    for x in range(key[0] - my_range, key[0] + my_range + 1):
                        for y in range(key[1] - my_range, key[1] + my_range + 1):

                            # if move is valid, add it to the possible_actions
                            if valid_move(n, key, (x, y), board):
                                move = ("MOVE", n, key, (x,y))
                                possible_actions.append(move)

        return possible_actions

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        """ Also just copied from part A at the moment, needs to be modified"""
        #TODO modify this method to be used for part B instead of part A

        my_type = action.action_type
        local_board = copy.deepcopy(board)

        if my_type == BOOM:
            return boom_piece(action.loc_a, local_board)  # returns a new boomed board

        else:
            return move_token(action.n, action.loc_a, action.loc_b, local_board)  # returns a new moved board
        

    def utility(self, state, player):
        """Return the value of this final state to player."""
        #TODO figure out how to use utility function? :-) 

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        #TODO either ensure that self.actions can be used as it is below, OR make a new terminal test
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        #TODO implement this method, also remember to add somewhere to store whose turn it is in game state 
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        #TODO maybe use the printing methods provided to us in Part A to print state of the game? 
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        #TODO implement this method. The stuff currently here is just copied from the abstract implementation of Game
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))