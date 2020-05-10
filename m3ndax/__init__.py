# Note:
# The class defined within this module with the name 'Player' is the
# class we will test when assessing your project.
# You can define your player class inside this file, or, as in the
# example import below, you can define it in another file and import
# it into this module with the name 'Player':

from m3ndax.player import ExamplePlayer as Player
from m3ndax.game import *
from m3ndax.player import INIT_BOARD

team_m3ndax = Player(WHITE, Expendibots())
team_m3ndax.action()

