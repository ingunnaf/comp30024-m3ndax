import sys
import json

import util as u
import game as g


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = g.insert_data_from_json(data)



    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
