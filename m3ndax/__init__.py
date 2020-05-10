# Note:
# The class defined within this module with the name 'Player' is the
# class we will test when assessing your project.
# You can define your player class inside this file, or, as in the
# example import below, you can define it in another file and import
# it into this module with the name 'Player':

from m3ndax.player import ExamplePlayer as Player
from m3ndax.player import UTILITYPLACEHOLDER, GameState, _BLACK_START_SQUARES, _WHITE_START_SQUARES
from m3ndax.game import *
from m3ndax.util import *

myExpendibots = Expendibots()

board = create_board(_BLACK_START_SQUARES, _WHITE_START_SQUARES)

my_gamestate = GameState(WHITE, UTILITYPLACEHOLDER, board, None)

minmax_decision(my_gamestate, myExpendibots)