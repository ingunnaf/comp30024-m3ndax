import sys
import json
import timeit

from search import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = insert_data_from_json(data)

    problem = Expendibots(my_board, None)

    start = timeit.default_timer()

    solution_node2 = recursive_best_first_search(problem)

    for node in solution_node2.path()[1:]:
        action = node.action
        action.print_action()

    stop = timeit.default_timer()

    print("time: " + str(stop - start))


if __name__ == '__main__':
    main()
