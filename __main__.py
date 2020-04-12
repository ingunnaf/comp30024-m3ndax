import sys
import json
import timeit

from search import *



def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = insert_data_from_json(data)

    print_board(my_board)

    problem = Expendibots(my_board, None)
    # solution_node = breadth_first_tree_search(problem)

    '''for node in solution_node.path()[1:]:
        # print_board(node.state)
        action = node.action
        action.print_action()'''

    start = timeit.default_timer()
    #solution_node2 = iterative_deepening_search(problem)

    solution_node2 = recursive_best_first_search(problem, problem.h)
    for node in solution_node2.path()[1:]:
        # print_board(node.state)
        action = node.action
        action.print_action()

    stop = timeit.default_timer()

    print('Time: ', stop - start)

if __name__ == '__main__':
    main()
