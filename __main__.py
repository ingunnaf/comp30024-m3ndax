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

    u.print_board(my_board)


    node = s.Node(my_board)
    print(" Initial node: " + str(node.__repr__()))
    successors = node.expand(expendibots, my_board)

    
    for snode in successors:
        next_node = snode
        print(" D1node: " + str(snode.__repr__()) + "\n")
        for d2node in next_node.expand(expendibots, next_node.state) :
            
            print(" D2node: " + str(d2node.__repr__()))
        print("\n")
    
    #solution_node = s.breadth_first_tree_search(expendibots)
    
    #path_to_solution = solution_node.path()
    #print("we didn't get this far did we?")
    #for node in path_to_solution :
    #    action = node.action
    #    action.print_action()
    
    
    #

    
if __name__ == '__main__':
    main()
