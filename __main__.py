import sys
import json

import util
import game
import search

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = game.insert_data_from_JSON(data)
    util.print_board(board)

    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()
