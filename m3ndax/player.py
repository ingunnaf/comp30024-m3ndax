from collections import namedtuple
import copy

_BLACK_START_SQUARES = [(0,7), (1,7),   (3,7), (4,7),   (6,7), (7,7),
                        (0,6), (1,6),   (3,6), (4,6),   (6,6), (7,6)]
_WHITE_START_SQUARES = [(0,1), (1,1),   (3,1), (4,1),   (6,1), (7,1),
                        (0,0), (1,0),   (3,0), (4,0),   (6,0), (7,0)]

# col = colour, h = height
Piece = namedtuple('P', 'col h')

# define static variables
BLACK = 'black'
WHITE = 'white'
BOOM = "boom"
MOVE = "move"

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # Set up state representation
        self.board = create_board(_BLACK_START_SQUARES, _WHITE_START_SQUARES)
        self.colour = colour


    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """


        # TODO: Decide what action to take, and return it

        # Placeholder: just returns a valid action
        # Consults Expendibots class to determine what valid actions are?

        #for testing purposes to see that init and update methods work as intended, 
        # this for loop looks for a token in our colour and says to boom this token
        for square in self.board.keys(): 
            if self.board[square].col == self.colour :
                return ("BOOM", square)


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
        """

        action_type = action[0]

        if action_type == "BOOM": # action is a BOOM
            origin = action[1]
            self.board = boom(origin, self.board)
        
        else: # action is a MOVE
            n = action[1]
            loc_a = action[2]
            loc_b = action[3]

            self.board = move_token(n, loc_a, loc_b, self.board)


        # TODO: Update state representation in response to action.


def create_board(black_start_squares, white_start_squares) : 
    board = dict()
    for xy in black_start_squares: 
        board[xy] = Piece(BLACK, 1)
    for xy in white_start_squares:
        board[xy] = Piece(WHITE, 1)
    return board


def boom(origin, my_board):

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
                boom((i,j), my_board)

    return my_board

def move_token(n, a, b, board):
        ret_board = copy.deepcopy(board)
        # check if move is valid
        """if not valid_move(n, a, b, board):
            return board""" #i commented this out because at the moment, we don't need to validate 
            #the action given to us for update method in player class

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


# everything above this line is used by the player class at the moment, but this should probably be moved to game.py file
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
