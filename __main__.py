import sys
import json

import util as u
import game as g
import search as s

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = g.insert_data_from_JSON(data)
    

    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
