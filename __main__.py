import sys
import json
import os

from util import print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    print(data)
    print_board(data)


    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()
