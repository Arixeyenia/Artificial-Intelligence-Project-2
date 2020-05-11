import math
from random import randint
from mimikyu.game import Directions, Board, Piece, Stack, get_opposite_direction
from mimikyu.actions import valid_move_check, move, boom, get_pieces_affected_by_boom, get_minimum_distance_from_enemy, get_minimum_distance_from_enemy_to_our_stack, get_enemy_pieces_in_blast_range, get_ally_pieces_in_blast_range, get_stack_closest_to_enemy
from mimikyu.transposition_table import TT

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
        if (v == math.inf and move[0] == "BOOM"):
            return move
        if v > v_max or best_move is None: 
            v_max = v
            best_move = move

    return best_move

def max_value(state, alpha=-math.inf, beta=math.inf):
    if cutoff_test(state):
        # if enemy is within range, proceed capture strategy
        #if get_minimum_distance_from_enemy(state.board) <= 2:
        #    return quiscence(state, alpha, beta)
        #else:
        return eval(state)
    
    for s in next_states(state).values():
        alpha = max(alpha, min_value(s, alpha, beta))
        if alpha >= beta:
            return beta

    return alpha

def min_value(state, alpha=-math.inf, beta=math.inf):
    if cutoff_test(state):
        # if enemy is within range, proceed capture strategy
        # if get_minimum_distance_from_enemy(state.board) <= 2:
        #    return quiscence(state, alpha, beta)
        # else:
        
        return eval(state)

    for s in next_states(state).values():
        beta = min(beta, max_value(s, alpha, beta))
        if beta <= alpha:
            return alpha

    return beta


def cutoff_test(state):
    if (state.depth == 4 or game_over(state)):
        return True
    else:
        return False

def game_over(state):
    if (state.board.get_ally_count() == 0 or state.board.get_enemy_count() == 0):
        return True
    else:
        return False

def quiscence(state, alpha, beta):
    stand_pat = eval(state)
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

# get all the possible moves
def get_all_moves(state):
    turn = state.turn
    moves = []
    for stack in turn.values():
        for no_pieces in range(1, stack.get_number() + 1):
            for spaces in range(1, stack.get_number() + 1):
                piece = stack.get_substack(no_pieces)
                current_coordinates = piece.get_coordinates()

                for d in Directions:
                    new_coordinate = piece.get_new_coordinates(d, spaces)
                    valid = valid_move_check(
                        state.board, stack, no_pieces, current_coordinates, new_coordinate)
                    if not valid:
                        continue
                    else:
                        moves.append(
                            ('MOVE', no_pieces, current_coordinates, new_coordinate))

        
    for stack in turn.values():
        moves.append(('BOOM', stack.get_coordinates()))
    return moves

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


def eval(state):
    parent = state.parent
    enemies_killed = parent.board.get_enemy_count()-state.board.get_enemy_count()
    allies_left = state.board.get_ally_count()
    enemies_left = state.board.get_enemy_count()
    
    if (enemies_left == 0 and allies_left > 0):
        return math.inf
    if (allies_left == 0):
        return -math.inf
    
    # 1. Escape if in danger
    # 3. Trying to escape, choose the best path
    #minimal_loss = minimize_loss(state)
    stacks_dead = escape(state)
    
    # 2. Evaluate whether to run/throw/capture
    sacrifice_one_for_many = 0
    #sacrifice_few_for_many = explode_clusters(state)
    sacrifice_one_for_one = 0
    
    # evaluate moving towards enemy to attack
    attack_potential = move_closer(state)
    
    #eval_value = (allies_left - enemies_left) + enemies_killed + stacks_dead + sacrifice_few_for_many + sacrifice_one_for_one + 0.125*attack_potential
    
    eval_value = 2*evaluate_move_taken(state) + 0.125*attack_potential + stacks_dead

    return eval_value


def minimize_loss(state):
    num_ally_in_enemy_range = 0
    num_enemy_in_enemy_range = 0
    max_util = []

    for stack in state.board.enemy.values():
        all_coordinates = get_pieces_affected_by_boom(
            state.board, stack.get_coordinates())
        for coordinates in all_coordinates:
            if coordinates in state.board.ally:
                num_ally_in_enemy_range += state.board.ally[coordinates].get_number()
            else:
                num_enemy_in_enemy_range += state.board.enemy[coordinates].get_number()
        max_util.append(num_enemy_in_enemy_range-num_ally_in_enemy_range)
        
    return max([x for x in max_util])

def explode_clusters(state):
    
    num_ally_in_range = 0
    num_enemy_in_range = 0
    max_util = []

    for stack in state.board.ally.values():
        all_coordinates = get_pieces_affected_by_boom(
            state.board, stack.get_coordinates())
        for coordinates in all_coordinates:
            if coordinates in state.board.ally:
                num_ally_in_range += state.board.ally[coordinates].get_number()
            else:
                num_enemy_in_range += state.board.enemy[coordinates].get_number()
        max_util.append(num_enemy_in_range-num_ally_in_range)
    return min([x for x in max_util])

# encourage a stack if threatened to escape
# returns a very negative value
def escape(state):
    our_stacks = state.board.ally.values()
    num_piece_in_stacks_that_can_die = 0
    for stack in our_stacks:
        if (stack.get_number() >= 2 and get_minimum_distance_from_enemy_to_our_stack(state.board, stack.get_coordinates()) <= 2):
            num_piece_in_stacks_that_can_die += stack.get_number()

    return -(num_piece_in_stacks_that_can_die * 2)

def move_closer(state):
    move = state.previous_move
    distance = 8
    if (move != () and move[0] == "MOVE"):
        distance = get_minimum_distance_from_enemy_to_our_stack(state.board, move[3])

    return (8 - distance)

def evaluate_move_taken(state):
    move = state.previous_move
    parent = state.parent
    if (move!= () and move[0] == "BOOM"):
        boom_coord = move[1]
        boom_stack = parent.turn[boom_coord]
        ally_dead = get_ally_pieces_in_blast_range(parent.board, boom_stack)
        enemy_dead = get_enemy_pieces_in_blast_range(parent.board, boom_stack)
        return 2*(len(enemy_dead) - len(ally_dead))

    if (move != () and move[0] == "MOVE"):
        move_new_coord = move[3]
        moved_stack = state.board.get_board_dict()[move_new_coord]
        ally_in_range = get_ally_pieces_in_blast_range(state.board, moved_stack)
        enemy_in_range = get_enemy_pieces_in_blast_range(state.board, moved_stack)
        if (len(enemy_in_range) == 0):
            return 0
        return (len(enemy_in_range) - len(ally_in_range))

    return 0