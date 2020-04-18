# a_star_search(board_dict, start_node, goal_node): return path from start_node -> goal_node (an array of board dicts)

from operator import itemgetter

from search.game import Piece, Stack, Board, Cluster, Directions
from search.actions import valid_move_check, move
from search.util import print_move, print_boom, print_board
from search.goal_search import match_with_white

# Define the node Node(Node parent, state current_state)


class Node():
    def __init__(self, parent=None, state=None, stack=None, direction=None):

        # previous node
        self.parent = parent
        # state = board
        self.state = state
        # board.white().that particular stack
        self.stack = stack
        self.direction = direction

        # values to be calculated:
        # g value - distance from start node to current node
        self.g = 0
        # h value - distance from end node to current node
        self.h = 0
        # f value - g + h
        self.f = 0

        def __str__(self):
            return "parent:%s | state:%s" % (self.parent, self.state)

# initialize_start(Stack.coordinate start)


def initialize_start(start, white_stack):
    start_node = Node(None, start, white_stack, None)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    return start_node

# initialize_start(Stack.coordinate end)
# stack with 0 coordinates
def initialize_end(end, end_stack):

    # get end node stack

    end_node = Node(None, end, end_stack, None)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    return end_node

# find the distance between two nodes
# - get best node (the thing a* is based on) = heuristics
def heuristics(start_node, target_node):
    # D = path cost
    D = 1
    dx = abs(start_node.stack.coordinates[0] -
             target_node.stack.coordinates[0])
    dy = abs(start_node.stack.coordinates[1] -
             target_node.stack.coordinates[1])

    return D * (dx + dy)

# - a star search - the main search function, adapted from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def a_star_search(start, end, white_stack, end_stack):

    # Initialize the start and end node
    start_node = initialize_start(start, white_stack)
    end_node = initialize_end(end, end_stack)

    # Initialize open list = nodes that we've calculated the f value
    open_list = []
    # initialize closed list = nodes that has been evaluated
    closed_list = []

    # add the first node to the open list
    open_list.append(start_node)

    # open FUNCTION: while open list is not empty
    while len(open_list) > 0:

        # the current_node = node in open list with lowest f_value
        current_node = open_list[0]
        current_node_index = 0

        for i in range(len(open_list)):

            # make a sorting function comparing the open and closed list
            if open_list[i].f < current_node.f:
                current_node = open_list[i]
                current_node_index = i

        # remove current_node from open list
        open_list.remove(current_node)
        # add current_node to closed list
        closed_list.append(current_node)

        # print(current_node.stack.coordinates)
        # print(current_node.f)

        # convert the paths from coordinates to Stacks.
        # if current_node reached the goal_node
        if goal_test(current_node, end_node):
            
            path = []
            state_path = []
            path_node = current_node

            # current_node = end_node
            while path_node is not None:
                # change the format to board dict now
                path.append(path_node)
                # state_path.append(path_node.state)
                path_node = path_node.parent
                
            return path[::-1]

        # generate neighbouring nodes
        neighbours_list = []

        #iterate how many piececs to move
        for no_pieces in range(len(current_node.stack.pieces)):
            
            #iterate direction for specified stack (group of pieces) to move
            for direction in Directions:

                #iterate number of spaces to move in that direction
                for spaces in range(len(current_node.stack.pieces)):
                
                    new_state = current_node.state.get_copy()
                    new_stack = new_state.white[current_node.stack.coordinates]

                    stack = move(new_state, new_stack, no_pieces+1, spaces+1, direction)
                    if not stack:
                        continue

                    # create neigbours node node
                    neighbour_node = Node(current_node, new_state, stack, direction)
                    if state_in_list(closed_list, new_state):
                        continue

                    # add to neighbours array
                    neighbours_list.append(neighbour_node)

        for neighbour_node in neighbours_list:

            # check if node is explored and if not just skip
            if is_in_list(closed_list, neighbour_node):
                continue

            # calculate f value of current path
            neighbour_path_cost = current_node.g + heuristics(current_node, neighbour_node)

            # - goal test
            # check if the new path is shorter or neighbour is not included in open list yet
            if (neighbour_path_cost < current_node.g) or (neighbour_node not in open_list):
                neighbour_node.g = neighbour_path_cost
                neighbour_node.h = heuristics(
                    neighbour_node, end_node)
                neighbour_node.f = neighbour_node.g + neighbour_node.h
                
            # if node is already in open list, dont add it in
            if is_in_list(open_list, neighbour_node):
                continue

            # Add the child to the open list
            open_list.append(neighbour_node)


def a_star_main(board, end_boards, goal_pairs):
    
    total_paths = []
    white_dict = board.white
    
    all_boards = [board] + end_boards
    
    for i, end_board in enumerate(end_boards):
        
        end_white_dict = end_board.white
        white_dict = all_boards[i].white
        
        for coordinate, white_stack in white_dict.items():
            
            for end_coord, end_stack in end_white_dict.items():
                
                if coordinate in goal_pairs:
                    
                    if goal_pairs[coordinate] == end_coord:
                        
                        paths = a_star_search(all_boards[i], all_boards[i+1], white_dict[coordinate], end_white_dict[end_coord])
                        
                        if paths is not None:
                            
                            total_paths.append(paths)
                        
    
    for i in range(len(total_paths)):
        for j in range(len(total_paths[i])):
            print_board(total_paths[i][j].state.get_board_dict())
            
    for i in range(len(total_paths)):
        for j in range(len(total_paths[i])-1):
            print_move(total_paths[i][j].stack.number, total_paths[i][j].stack.coordinates[0], total_paths[i][j].stack.coordinates[1],total_paths[i][j+1].stack.coordinates[0], total_paths[i][j+1].stack.coordinates[1] )
            
    for i in range(len(total_paths)):
        print_boom(total_paths[i][-1].stack.coordinates[0],total_paths[i][-1].stack.coordinates[1] )

    
    # for path in total_paths:
        # print_board(path.state.get_board_dict())
        # print_board(path.get_board_dict())
    # return total_paths

# get current stack by comparing the old state and the new state


def get_current_stack(new_state):
    coord = list(new_state.white.keys())[-1]
    return new_state.white[coord]
    

# Node -> state (board) -> white_stack = board.get_white()
# -> iterate ->  white_stack[goal_tile] = Stack(PIECES, white) (match coordinate with goal coordinate)
# def get_white_piece(board, goal_tile_list, goal_pairs):
#     # get board state
#     white_dict = board.white

#     for coordinate, stack in white_dict.items():
#         for goal_tile in goal_tile_list:

def state_in_list(open_closed_list, state):
    state_white_coordinates = sorted(list(state.white.keys()), key=itemgetter(0))
    for node in open_closed_list:
        open_closed_state_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
        if state_white_coordinates == open_closed_state_white_coordinates:
            return True

    return False

def is_in_list(open_closed_list, node):
    node_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
    for node in open_closed_list:
        open_closed_node_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
        if node_white_coordinates == open_closed_node_white_coordinates:
            return True

    return False

def goal_test(node, end_node):
    node_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
    end_node_white_coordinates = sorted(list(end_node.state.white.keys()), key=itemgetter(0))
    if node_white_coordinates == end_node_white_coordinates:
        return True
    else:
        return False
