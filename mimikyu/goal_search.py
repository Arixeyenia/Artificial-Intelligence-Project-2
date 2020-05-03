class Cluster:
      def __init__(self, coordinates, intersection):
        self.coordinates = coordinates
        self.intersection = intersection
        

# Get one black token and find its range
def get_black_range(board, stack):
    coordinates = stack.coordinates
    black_coordinates = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if (x == 1 and y == 1) or not valid_tile(check_coord, board):
                continue
            black_coordinates.append(check_coord)

    return black_coordinates

# get all the black token and use the black range function
def get_all_black_ranges(board):

    black_ranges_dict = {}
    coordinates = list(board.black.values())

    for coordinate in coordinates:
        black_stacks = get_black_range(board, coordinate)
        black_ranges_dict[coordinate.coordinates] = black_stacks

    # return a dictionary of {(x,y): [(a,b),(c,d),(e,f)]}
    return black_ranges_dict

# check for adjacent pieces for chain explosions
def check_chaining(board):
    black_ranges = get_all_black_ranges(board)
    # black_ranges = {(x,y): [(a,b),(c,d),(e,f)]}
    blacks = list(black_ranges.keys())
    black_ranges_list = list(black_ranges.values())

    # blacks = [(x,y), (z,a)] a list of black coordinates
    for i in range(len(blacks)):
        for j in range(len(black_ranges_list)):
            if blacks[i] in black_ranges_list[j]:
                black_ranges[blacks[j]] = list(
                    set(black_ranges[blacks[i]] + black_ranges_list[j]).difference(set([blacks[j]])))

    return black_ranges

# get the intersecting black ranges
def get_intersections(board):
    intersection_list = []
    a_list = []
    black_ranges_dict = check_chaining(board)

    blacks = list(black_ranges_dict.keys())
    black_ranges_list = list(black_ranges_dict.values())

    # turn dictionary into a pair of list
    black_ranges = list(black_ranges_dict.items())

    for i in range(len(black_ranges)):
        current = set(black_ranges[i][1])
        for j in range(len(black_ranges)):

            # add all intersections to a list
            if len(list(set(black_ranges[i][1]).intersection(set(black_ranges[j][1])))) != 0:

                current = set(black_ranges[i][1]).intersection(black_ranges[j][1])
                intersection_class = Cluster([black_ranges[i][0], black_ranges[j][0]], list(current))
                intersection_list.append(intersection_class)
                a_list.append([black_ranges[i][0], black_ranges[j][0]])

            # if no intersection found, add one coordinate as a intersection anyways
            if (j+1 == len(black_ranges)) and (current == set(black_ranges[i][1])):
                intersection_class = Cluster(
                    [black_ranges[i][0]], list(current))
                intersection_list.append(intersection_class)
                a_list.append(black_ranges[i][0])

        if (i+2 == len(black_ranges)) and (current == set(black_ranges[i][1])):
            intersection_class = Cluster(
                [black_ranges[i+1][0]], list(current))
            intersection_list.append(intersection_class)
            a_list.append(black_ranges[i+1][0])

    return intersection_list


# Get list of clusters Cluster(black_coordinates, [intersections])
def get_cluster(board):

    intersection_list = get_intersections(board)

    cluster_dict = {}

    for i in range(len(intersection_list)):

        current = set(intersection_list[i].coordinates)
        current_inter = set(intersection_list[i].intersection)

        for j in range(len(intersection_list)):

            # if there's only one cluster
            if len(current.union(set(intersection_list[j].coordinates))) == len(list(board.black)):

                current = current.union(set(intersection_list[j].coordinates))
                current_inter = current_inter.intersection(
                    set(intersection_list[j].intersection))

                cluster_dict[tuple(current)] = list(current_inter)

                return cluster_dict

            if (current.intersection(set(intersection_list[j].coordinates)) != set()) and (
                current_inter.intersection(set(intersection_list[j].intersection)) != set()):

                # unionize the coordinates
                current = current.union(set(intersection_list[j].coordinates))

                # find the intersection from the intersections
                current_inter = current_inter.intersection(
                    set(intersection_list[j].intersection))

            if j+1 == len(intersection_list):
                cluster_dict[tuple(current)] = list(current_inter)

        if i+2 == len(intersection_list):
            cluster_dict[tuple(current)] = list(current_inter)

    if len(cluster_dict) == len(board.white):
        return cluster_dict
    else:
        return False

# Check if a potential goal tile 
def white_victims(board, coordinates):
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)
    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.white:
                if (x == 1 and y == 1):
                    continue
                stacks.append(board.white[check_coord])
    if len(stacks) != 0:
        return True
    return False

#  Get a goal tile from each cluster and append to a list
def get_goal_tiles(board, cluster_dict={}):

    goal_tile_list = []
    cluster_list = list(cluster_dict.values())
 
    for i, cluster in enumerate(cluster_list):
        for j in range(len(cluster)):            
            # if boom range results in white catastrophe, thank u next
            if white_victims(board, cluster[j]):
                continue
            else:
                goal_tile_list.append(cluster[j])
                break
        
    return goal_tile_list

# Create a new goal tile
def goal_tile_states(board, goal_tile, coord):

    new_board = board.get_copy()
    new_board.white[goal_tile] = new_board.white[coord]
    new_board.white[coord].coordinates = goal_tile
    for piece in new_board.white[coord].pieces:
        piece.set_coordinates(goal_tile)
        if goal_tile != coord:
            del new_board.white[coord]

    return new_board

# match a starting white stack with a goal tile
def match_with_white(board, end_boards):

    white_stacks = list(board.get_white().keys())
    goal_pairs = {}

    for i, end_board in enumerate(end_boards):
        goal_pairs[white_stacks[i]] = end_board

    return goal_pairs

# produce the final goal state
def goal_state(board, goal_tile_list, goal_pair):

    state = board.get_copy()
    coords = list(state.white.keys())
 
    consecutive_states = []

    for goal_tile in goal_tile_list:
        for coord in coords:
            if goal_pair[coord] == goal_tile:
                state = goal_tile_states(
                    state.get_copy(), goal_pair[coord], coord)
                consecutive_states.append(state)
                
    return consecutive_states

# Check if the tile is valid
def valid_tile(coordinate, board):
    if coordinate in list(board.black.values()):
        return False

    for i, point in enumerate(coordinate):
        if coordinate[i] > 7 or coordinate[i] < 0:
            return False
    return True
