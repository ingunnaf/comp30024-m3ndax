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

        return ("BOOM", (0, 0))


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
        ret_board = board.copy()
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


# everything above this line is used by the player class
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# everything below this line is just here for reference at the moment



class Expendibots: 

    def __init__(self) :
        self.board = dict()
        for xy in _BLACK_START_SQUARES: 
            self.board[xy] = Piece(BLACK, 1)
        for xy in _WHITE_START_SQUARES:
            self.board[xy] = Piece(WHITE, 1)

        self.turn = WHITE #white always begins 

    def manhat_dist(self, a, b):
        """returns the number of cardinal moves a piece would have to make to reach the other piece
        """
        x1, x2 = a[0], b[0]
        y1, y2 = a[1], b[1]

        dist = (abs(x1 - x2)) + (abs(y1 - y2))

        return dist


    def valid_move(self, n, a, b, board):
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
        if (dist > my_range):
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


    


    def valid_boom(self, origin, my_board):
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


    def boom_piece(self, origin, init_board):
        if not valid_boom(origin, init_board):
            raise RuntimeError("Invalid Boom Move")

        ret_board = copy.deepcopy(init_board)
        boom(origin, ret_board)
        return ret_board


    


    def n_pieces(self, board, piece_col):
        """
        counts how many pieces of the given colour are on the board
        """
        coords = [(x, 7 - y) for y in range(8) for x in range(8)]

        cnt = 0

        for xy in coords:
            if xy in board:
                if board[xy].col == piece_col:
                    cnt += board[xy].h

        return cnt

