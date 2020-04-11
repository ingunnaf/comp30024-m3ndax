import sys
import json

from util import * 
from game import *
from search import *
#from game import Piece, BLACK, WHITE, MOVE, BOOM



def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = insert_data_from_json(data)
    problem = Expendibots(my_board, None)
    print_board(my_board)

    solution_node = breadth_first_tree_search(problem)
    print(solution_node.parent.__repr__())
    print(solution_node.depth)
    print(solution_node.repeats)
    """
    path_to_solution = solution_node.path()
    if path_to_solution: 
        for node in path_to_solution :
            action = node.action
            action.print_action()
    else: 
        print("Actually, solution was not found? ")
    """

if __name__ == '__main__':
    main()
