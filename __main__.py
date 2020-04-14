import sys
import json

from search import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = insert_data_from_json(data)

    problem = Expendibots(my_board, None)

    solution_node2 = recursive_best_first_search(problem)

    for node in solution_node2.path()[1:]:
        action = node.action
        action.print_action()


if __name__ == '__main__':
    main()
