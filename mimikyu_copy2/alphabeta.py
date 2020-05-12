import math
from random import randint
from mimikyu_copy2.game import Directions, Board, Piece, Stack, get_opposite_direction
from mimikyu_copy2.actions import valid_move_check, manhattan_distance, move, boom, get_pieces_affected_by_boom, get_minimum_distance_from_enemy, get_minimum_distance_from_enemy_to_our_stack, get_enemy_pieces_in_blast_range, get_ally_pieces_in_blast_range, get_stack_closest_to_enemy
from mimikyu_copy2.transposition_table import TT


class Node:
    def __init__(self, board, parent, alpha=-math.inf, beta=math.inf):
        self.board = board
        self.parent = parent
        self.alpha = alpha
        self.beta = beta
        self.successors = []
        if self.parent is None:
            self.depth = 0
            self.turn = self.board.ally
        else:
            self.depth = self.parent.depth + 1
            if list(self.parent.turn.values())[0].get_colour() == list(self.parent.board.ally.values())[0].get_colour():
                self.turn = self.board.ally
            else:
                self.turn = self.board.enemy

        self.previous_move = ()

    def swap_turn(self):
        if (game_over(self)):
            return
        if list(self.turn.values())[0].get_colour() == list(self.board.ally.values())[0].get_colour():
            self.turn = self.board.enemy
        elif list(self.turn.values())[0].get_colour() == list(self.board.enemy.values())[0].get_colour():
            self.turn = self.board.ally


# Chooses the best action to take for both maximizing and minimizing player based on their  
def alpha_beta_search(state, TT):
    
    #check transposition table
    if (get_minimum_distance_from_enemy(state.board) >1):
        move = TT.get_move(state.board)
        if (move != False):
            valid = valid_move_check(state.board, state.board.ally[move[2]], move[1], move[2], move[3])
            if (valid):
                return move
        
    # test and print
    v_max = -math.inf
    best_move = None
    successors = next_states(state)
    for move in successors:
        v = min_value(successors[move], v_max, math.inf)
        # if (v == math.inf and move[0] == "BOOM"):
        #     return move
        if v > v_max or best_move is None: 
            v_max = v
            best_move = move

    return best_move


# Maximizing player returns highest value for a move. Record alpha as the current largest value and prune branches worse than that
def max_value(state, alpha=-math.inf, beta=math.inf):
    if cutoff_test(state):
        # if enemy is within range, proceed capture strategy
        #if get_minimum_distance_from_enemy(state.board) <= 2:
        #    return quiscence(state, alpha, beta)
        #else:
        return evaluate(state)
    
    for s in next_states(state).values():
        alpha = max(alpha, min_value(s, alpha, beta))
        if alpha >= beta:
            return beta

    return alpha


# Minimizing player returns lowest value for a move and updates beta to lowest value
def min_value(state, alpha=-math.inf, beta=math.inf):
    if cutoff_test(state):
        # if enemy is within range, proceed capture strategy
        # if get_minimum_distance_from_enemy(state.board) <= 2:
        #    return quiscence(state, alpha, beta)
        # else:
        return evaluate(state)

    for s in next_states(state).values():
        beta = min(beta, max_value(s, alpha, beta))
        if beta <= alpha:
            return alpha

    return beta


# Specify cutoff depth of where the tree will search to
def cutoff_test(state):
    if (state.depth == 4 or game_over(state)):
        return True
    else:
        return False


# Determine end of the game
def game_over(state):
    if (state.board.get_ally_count() == 0 or state.board.get_enemy_count() == 0):
        return True
    else:
        return False


# Quiescence search to evaluate quiescent positions
def quiscence(state, alpha, beta):
    stand_pat = evaluate(state)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat
    
    for capture in get_all_captures(state):
        new_state = create_new_node(state)
        new_state.swap_turn()
        boom(new_state.board, capture)
        score = -quiscence(new_state, -beta, -alpha)
        
        if (score >= beta):
            return beta
        if (score > alpha):
            alpha = score

    return alpha


# alternative getting moves
def get_critical_moves(state):
    closest_stack = get_stack_closest_to_enemy(state.board, state.turn)
    moves = []
    for no_pieces in range(1, closest_stack.get_number() + 1):
        for spaces in range(1, closest_stack.get_number() + 1):
            piece = closest_stack.get_substack(no_pieces)
            current_coordinates = piece.get_coordinates()

            for d in Directions:
                if (state.parent is not None and get_opposite_direction(state.parent.previous_move) == d):
                    continue
                new_coordinate = piece.get_new_coordinates(d, spaces)
                valid = valid_move_check(state.board, closest_stack, no_pieces, current_coordinates, new_coordinate)
                if not valid:
                    continue
                else:
                    moves.append(
                        ('MOVE', no_pieces, current_coordinates, new_coordinate))

    
    moves.append(('BOOM', closest_stack.get_coordinates()))
    return moves


# Get the next succesor states
def next_states(state):
    s = {}
    s_moves = get_critical_moves(state)
    for s_move in s_moves:
        if (s_move[0] == 'BOOM'):
            new_state = create_new_node(state)
            
            boom(new_state.board, s_move[1])
            new_state.previous_move = s_move
            
            s[s_move] = new_state

        elif (s_move[0] == 'MOVE'):
            new_state = create_new_node(state)
            move(new_state.board, s_move[1], s_move[2], s_move[3], new_state.turn)
            new_state.previous_move = s_move
            s[s_move] = new_state
        
        new_state.swap_turn()
    return s


# get all captured states for quiscence search
def get_all_captures(state):
    player = state.turn
    capture = []
    for stack in player:
        capture.append(stack)
    return capture


# create new node and update the depth
def create_new_node(state):
    new_board = state.board.get_copy()
    new_state = Node(new_board, state)
    # new_state.swap_turn()
    return new_state


# Gives an evaluation value of different possible states for alpha-beta to choose
def evaluate(state):
    parent = state.parent
    enemies_killed = parent.board.get_enemy_count()-state.board.get_enemy_count()
    allies_left = state.board.get_ally_count()
    enemies_left = state.board.get_enemy_count()
    
    # Evaluate endgame conditions
    if (enemies_left == 0 and allies_left > 0):
        return math.inf
    if (allies_left == 0):
        return -math.inf
        
    # eval_value = (allies_left - enemies_left) + enemies_killed + escape(state) + sacrifice_few_for_many + sacrifice_one_for_one + 0.125*attack_potential
    eval_value = 0.5*evaluate_move_taken(state) + 0.125*move_closer(state) + escape(state)
    
    # eval_value = 20*allies_left + 20*(12 - enemies_left) + 0.5*get_biggest_boom(state) + move_closer(state)
    return eval_value


# Encourage a stack if threatened to escape. Returns a very negative value
def escape(state):
    our_stacks = state.board.ally.values()
    num_piece_in_stacks_that_can_die = 0
    for stack in our_stacks:
        if (stack.get_number() >= 2 and get_minimum_distance_from_enemy_to_our_stack(state.board, stack.get_coordinates()) <= 2):
            num_piece_in_stacks_that_can_die += stack.get_number()

    return -(num_piece_in_stacks_that_can_die * 2)


# Get closer to enemy to attack them
def move_closer(state):
    move = state.previous_move
    distance = 8
    if (move != () and move[0] == "MOVE"):
        distance = get_minimum_distance_from_enemy_to_our_stack(state.board, move[3])

    return (8 - distance)


# Evaluate move based on previous move
def evaluate_move_taken(state):
    move = state.previous_move
    parent = state.parent
    if (move!= () and move[0] == "BOOM"):
        boom_coord = move[1]
        boom_stack = parent.turn[boom_coord]
        ally_dead = get_ally_pieces_in_blast_range(parent.board, boom_stack.get_coordinates())
        enemy_dead = get_enemy_pieces_in_blast_range(parent.board, boom_stack.get_coordinates())
        return 2*(len(enemy_dead) - len(ally_dead))

    if (move != () and move[0] == "MOVE"):
        move_new_coord = move[3]
        moved_stack = state.board.get_board_dict()[move_new_coord]
        ally_in_range = get_ally_pieces_in_blast_range(state.board, moved_stack.get_coordinates())
        enemy_in_range = get_enemy_pieces_in_blast_range(state.board, moved_stack.get_coordinates())
        if (len(enemy_in_range) == 0):
            return 0
        return (len(enemy_in_range) - len(ally_in_range))

    return 0
 
        
# Evaluate the best potential boom space with the least steps to take there
def get_biggest_boom(state):
    spaces_with_best_potential = []
    best_potential = 0
    
    for i in range(8):
        for j in range(8):
            # evaluate blast potential for an empty space
            if (i, j) not in state.board.ally and (i, j) not in state.board.enemy:
                enemy_in_range = get_enemy_pieces_in_blast_range(state.board, (i, j))
                ally_in_range = get_ally_pieces_in_blast_range(state.board, (i, j))
                
                potential = len(enemy_in_range) - len(ally_in_range)
                    
                # go for the space with the absolute best potential kill to save ratio
                if potential > best_potential:
                    spaces_with_best_potential = [(i,j)]
                    best_potential = potential
                    
                # append other spaces with the same potential
                elif potential == best_potential:
                    spaces_with_best_potential.append((i,j))
    
    # choose the best potential space with the shortest distance (using manhattan distance) to it
    distances = []
    for key in state.board.ally:
        step_size = state.board.ally[key].get_number()
        
        for space in spaces_with_best_potential: 
            steps_needed = manhattan_distance(space, key)
            distances.append(steps_needed / step_size)   

    # the points get higher the closer you are, agent will want to move closer to the enemy
    return -min(distances)

# priotarize running away by stacking
