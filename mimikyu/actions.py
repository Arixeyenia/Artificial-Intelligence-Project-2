import math
from operator import itemgetter
from mimikyu.game import Piece, Stack, Board, Directions

# get all the possible moes


def move(board, no_pieces, old_coord, new_coord, turn):
    stack = turn[old_coord]
    valid = valid_move_check(board, stack, no_pieces, old_coord, new_coord)
    if valid:
        substack = stack.get_substack(no_pieces)
        stack.remove_pieces(substack.pieces)
        substack.set_coordinates(new_coord)
        if new_coord in turn:
            turn[new_coord].add_stack(substack)
        else:
            turn[new_coord] = substack
        if turn[old_coord].get_number() == 0:
            del turn[old_coord]


def valid_move_check(board, stack, no_pieces, old_coord, new_coord):
    spaces = manhattan_distance(old_coord, new_coord)
    if stack.get_number() < no_pieces or stack.get_number() < spaces:
        return False

    if new_coord[0] < 0 or new_coord[0] > 7 or new_coord[1] < 0 or new_coord[1] > 7:
        return False

    if stack.get_colour() == board.my_colour:
        if new_coord in board.enemy:
            return False
    else:
        if new_coord in board.ally:
            return False

    return True


def manhattan_distance(old_coord, new_coord):
    dx = abs(old_coord[0] -
             new_coord[0])
    dy = abs(old_coord[1] -
             new_coord[1])

    return (dx + dy)


def boom(board, coordinates):
    all_coordinates = range_check(board, coordinates)
    remove_stack(board, coordinates)
    for coordinate in all_coordinates:
        boom(board, coordinate)

# get pieces


def get_pieces_affected_by_boom(board, coordinates):
    all_coordinates = []
    all_coordinates = range_check(board, coordinates)
    for coordinate in all_coordinates:
        more_coordinates = range_check(board, coordinate)
        for one_coordinate in more_coordinates:
            if one_coordinate in all_coordinates:
                continue
            else:
                all_coordinates.append(one_coordinate)
    return all_coordinates

# remove stack from the game/dict


def remove_stack(board, coordinates):
    if coordinates in board.ally:
        board.ally.pop(coordinates)
    if coordinates in board.enemy:
        board.enemy.pop(coordinates)


# return coordinates with stacks that is in the range of the stack specified
def range_check(board, coordinates):
    all_coordinates = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict():
                if (x == 1 and y == 1):
                    continue
                all_coordinates.append(check_coord)
    return all_coordinates

def range_check_get_enemy_pieces(board, coordinates):
    enemy_pieces = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict():
                if (x == 1 and y == 1):
                    continue
                if check_coord in board.enemy:
                    enemy_pieces.append(board.enemy[check_coord])
    return enemy_pieces

def range_check_get_ally_pieces(board, coordinates):
    ally_pieces = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict():
                if (x == 1 and y == 1):
                    continue
                if check_coord in board.ally:
                    ally_pieces.append(board.ally[check_coord])
    return ally_pieces

def get_minimum_distance_from_enemy(board):
    min_dist = math.inf

    for a_stack in board.ally:
        for e_stack in board.enemy:
            distance = manhattan_distance(a_stack, e_stack)
            if (distance < min_dist):
                min_dist = distance

    return min_dist


def sort_list_of_coordinates(list_of_coordinates):
    list_of_coordinates.sort(key=itemgetter(0, 1))
    return list_of_coordinates

def get_minimum_distance_from_enemy_to_our_stack(board, stack):
    min_dist = math.inf

    for e_stack in board.enemy:
        distance = manhattan_distance(stack, e_stack)
        if (distance < min_dist):
            min_dist = distance

    return min_dist

def get_enemy_pieces_in_blast_range(board, stack):
    all_enemy_stack = []
    all_enemy_stack = range_check_get_enemy_pieces(board, stack.get_coordinates())
    for a_stack in all_enemy_stack:
        more_stacks = range_check_get_enemy_pieces(board, a_stack.get_coordinates())
        for one_stack in more_stacks:
            if one_stack in all_enemy_stack:
                continue
            else:
                all_enemy_stack.append(one_stack)
    
    all_enemy_pieces = []
    for stack in all_enemy_stack:
        for piece in stack.pieces:
            all_enemy_pieces.append(piece)

    return all_enemy_pieces

def get_ally_pieces_in_blast_range(board, stack):
    all_ally_stack = []
    all_ally_stack = range_check_get_ally_pieces(board, stack.get_coordinates())
    for a_stack in all_ally_stack:
        more_stacks = range_check_get_ally_pieces(board, a_stack.get_coordinates())
        for one_stack in more_stacks:
            if one_stack in all_ally_stack:
                continue
            else:
                all_ally_stack.append(one_stack)
    
    all_ally_pieces = []
    for stack in all_ally_stack:
        for piece in stack.pieces:
            all_ally_pieces.append(piece)

    return all_ally_pieces

def get_stack_closest_to_enemy(board, turn):
    player = turn
    if (player == board.ally):
        player2 = board.enemy
    else:
        player2 = board.ally

    min_dist = math.inf
    for a_stack in player.values():
        distance_to_all_enemies = 0
        for e_stack in player2.values():
            distance_to_all_enemies += manhattan_distance(a_stack.get_coordinates(), e_stack.get_coordinates())
        
        if ( distance_to_all_enemies < min_dist):
            min_dist = distance_to_all_enemies
            closest_stack = a_stack

    return closest_stack
