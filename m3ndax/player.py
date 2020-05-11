# Remote imports
from collections import namedtuple
import copy

# Import functions from local module
# from m3ndax.game import *
from game import *

class ExamplePlayer:
    def __init__(self, colour, game):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        :return: it's a constructor and returns nothing
        """

        # Initialise game class (in our case the Expendibots class) and the board state
        self.game = game
        self.state = GameState(WHITE, 0, INIT_BOARD, None)

        # our player colour
        self.colour = colour

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        :return: ("MOVE", n, (Xa, Ya), (Xb, Yb)) OR ("BOOM", (x, y))
        """



        ''' Placeholder: just returns a valid action
        Consults Expendibots class to determine what valid actions are?
        for testing purposes to see that init and update methods work as intended,
        this for loop looks for a token in our colour and says to boom this token
        
        for square in self.game.board.keys():
            if self.game.board[square].col == self.colour:
                return "BOOM", square'''

        # Returns the best move to make by using the algorithm from game.py
        return minmax_decision(self.state, self.game)
        # TODO: ensure that the move is in the correct format for the referee

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        :return: Nothing, just updates the game state
        """

        # TODO: implement this method properly (go over and check that it works)
        action_type = action[0]

        if action_type == BOOM:  # action is a BOOM
            origin = action[1]
            placeholderstate = boom(origin, self.state.board)


        else:  # action is a MOVE
            n = action[1]
            loc_a = action[2]
            loc_b = action[3]

            placeholderstate = move_token(n, loc_a, loc_b, self.state.board)

        #update state
        self.state = GameState(colour, 0, placeholderstate, action)



# everything above this line is used by the player class at the moment, but this should probably be moved to game.py file
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
