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
    u.print_board(my_board)
    expendibots = s.Expendibots(my_board, None)
    
    node = s.Node(expendibots.board)
    
    successors = node.expand(expendibots, my_board)

    """
    for snode in successors: 
        print(snode.__repr__())

    actions = expendibots.actions()
    for action in actions:
        action.print_action()
    """
    u.print_board(my_board)









    """
    action1 = s.Action(MOVE, 1, (1,4), (1,5))
    action2 = s.Action(MOVE, 1, (1,5), (1,6))
    action3 = s.Action(MOVE, 1, (1,6), (2,6))
    action4 = s.Action(MOVE, 1, (2,6), (3,6))
    resulting_board = expendibots.result(action1)
    resulting_board = expendibots.result(action2)
    resulting_board = expendibots.result(action3)
    resulting_board = expendibots.result(action4)
    u.print_board(resulting_board)
    print(expendibots.goal_test(resulting_board))
    resulting_board = expendibots.result(s.Action(BOOM, 1, (3,6), None))
    u.print_board(resulting_board)

    print(expendibots.goal_test(resulting_board)) """
    """

    solution_node = s.recursive_best_first_search(problem, None)
    if solution_node : 
        print("Yay")
        path_nodes = solution_node.path()
        for node in path_nodes: 
            action = node.action
            s.print_action(action)
"""
    
if __name__ == '__main__':
    main()
