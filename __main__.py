import sys
import json

import util as u
import game as g


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

<<<<<<< HEAD
    board = g.insert_data_from_JSON(data)
    
=======
    my_board = g.insert_data_from_json(data)

    #g.boom((4, 3), my_board)
    u.print_board(my_board, unicode=True)
>>>>>>> 655605eebf86f9b35262f78f568c3f27e1f12dd9

    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
