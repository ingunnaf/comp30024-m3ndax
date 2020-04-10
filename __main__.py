import sys
import json

from search import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    my_board = insert_data_from_json(data)
    expendibots = Expendibots(my_board, None)

    solution_node = recursive_best_first_search(expendibots, None)

    path_to_solution = solution_node.path()
    print("we didn't get this far did we?")
    for node in path_to_solution:
        action = node.action
        action.print_action()


if __name__ == '__main__':
    main()
