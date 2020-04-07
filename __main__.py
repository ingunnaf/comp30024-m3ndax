import sys
import json

import util as u
import game as g
import search as s
from game import Piece, BLACK, WHITE, MOVE, BOOM



def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    
    my_board = g.insert_data_from_json(data)
    expendibots = s.Expendibots(my_board, None)

    solution_node = s.recursive_best_first_search(expendibots, None)
    
    path_to_solution = solution_node.path()
    print("we didn't get this far did we?")
    for node in path_to_solution :
        action = node.action
        action.print_action()
    
    
    #u.print_board(my_board)

    
if __name__ == '__main__':
    main()
