import sys
import json

import util as u
import game as g
import search as s


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    
    my_board = g.insert_data_from_json(data)

    problem = s.Expendibots(my_board, None)

    #solution_node is a node where we have won
    solution_node = s.recursive_best_first_search(problem, None)

    #path_nodes is a list of nodes on the path to the solution node
    path_nodes = solution_node.path()

    for node in path_nodes :
        print(str(node.action))
    


if __name__ == '__main__':
    main()
