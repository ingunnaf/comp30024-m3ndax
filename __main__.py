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

    solution = s.recursive_best_first_search(problem, problem.h())
    # h = heuristic function? i think
    
    """
    for action in solution :
        print(action)
    """
    

    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
