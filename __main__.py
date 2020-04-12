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
    
    # this stuff within the parenthesis finds a solution for level 1 and 2
    solution_node = breadth_first_tree_search(problem)
    path_to_solution = solution_node.path()
    
    for node in path_to_solution[1:] :
        action = node.action
        action.print_action()
        print(node.repeats)
    
    


    #solution_node = recursive_best_first_search(problem, h=None)
    

if __name__ == '__main__':
    main()
