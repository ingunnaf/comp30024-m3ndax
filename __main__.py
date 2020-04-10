import sys
import json

from game import *
from search import *
from util import *




def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    
    my_board = insert_data_from_json(data)
    print_board(my_board)

    boom_board = boom_piece((1, 4), my_board)

    print_board(boom_board)

    print_board(my_board)
if __name__ == '__main__':
    main()
