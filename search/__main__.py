import sys
import json

from search.util import print_move, print_boom, print_board
from search.game import Piece, Stack, Board, Cluster, Directions
from search.actions import move, valid_move_check, boom, remove_stack, range_check
from search.goal_search import get_black_range, get_all_black_ranges, get_cluster, get_goal_tiles, get_intersections, check_chaining, match_with_white, goal_state
from search.a_star import a_star_search, a_star_main


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        black_data = data["black"]

        black_dict = {}
        for input_stack in black_data:
            coords = tuple(input_stack[1:])

            no_pieces = input_stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "B"))

            stack = Stack(Pieces, "B")
            black_dict[coords] = stack

        white_data = data["white"]
        white_dict = {}

        for input_stack in white_data:
            coords = tuple(input_stack[1:])

            no_pieces = input_stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "W"))

            stack = Stack(Pieces, "W")
            white_dict[coords] = stack

        board = Board(black_dict, white_dict)
        goal_board = Board(black_dict, white_dict)
        
        # Find the range of all black tiles
        all_black_range = get_all_black_ranges(board)

        # Combine ranges of black tokens to take into account chain explosions
        chaining_range = check_chaining(board)

        # Find the intersections of adjacent black tokens
        get_intersection = get_intersections(board)

        # Find the clusters of black tokens
        clusters = get_cluster(board)

        list_of_goal_tiles = get_goal_tiles(board, clusters)

        # Match a black cluster with a white token
        match_pairs = match_with_white(board, list_of_goal_tiles)

        board_dict = board.get_board_dict()
        
        # set up the goals
        goals = set_up_goal(goal_board, list_of_goal_tiles, match_pairs)
        print_board(board_dict)
        
        goal_dict_list = []
        
        for goal in goals:
            goal_dict = goal
            goal_dict_list.append(goal_dict)
            
        white_stacks = []
        for key, value in board.white.items():
            white_stacks.append(board.white[key])
        
        
        # Outputting the answer 
        a_star_main(board, goal_dict_list, match_pairs)


def set_up_goal(board, list_of_goal_tiles, match_pairs):

    # Get a list of boards of the final states
    goal_states = goal_state(board, list_of_goal_tiles, match_pairs)

    return goal_states

if __name__ == '__main__':
    main()
