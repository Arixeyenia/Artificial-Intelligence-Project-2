from mimikyu.game import Piece, Stack, Board, Directions

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