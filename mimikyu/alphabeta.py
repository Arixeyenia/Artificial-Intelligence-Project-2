import math

from mimikyu.game import Directions, Board, Piece, Stack
from mimikyu.actions import valid_move_check, move, boom, get_pieces_affected_by_boom


class Node:
    def __init__(self, board, parent, alpha=-math.inf, beta=math.inf):
        self.board = board
        self.parent = parent
        self.successors = []
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        self.turn = self.board.ally

    def swap_turn(self):
        if self.turn == self.board.ally:
            self.turn = self.board.enemy
        elif self.turn == self.board.enemy:
            self.turn = self.board.ally


def max_value(state, alpha, beta):
    if cutoff_test(state):
        return eval(state)
    for s in successors(state):
        alpha = max(alpha, min_value(s, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha


def min_value(state, alpha, beta):
    if cutoff_test(state):
        return eval(state)
    for s in successors(state):
        alpha = min(alpha, max_value(s, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha

# TODO: Change to quiscence search


def cutoff_test(state):
    if state.depth == 5:
        return False
    else:
        return True

# TODO: Create search evaluation

def eval(state):

    # Evaluation function
    # TODO: Determine weights to use
    # F = w1(nEnemyTokenInRange - nOurTokenInRange) + w2(nEnemyToken - nOurToken)
    
    # get number of enemies & allies token
    num_enemy = state.board.get_enemy_count
    num_ally = state.board.get_ally_count
    
    ally_count = 0
    enemy_count = 0
    
    # get number of enemy token in range and allies token in range
    for stack in state.board.ally:
        all_coordinates = get_pieces_affected_by_boom(state.board, stack.get_coordinates())
        for coordinates in all_coordinates:
            if state.board.ally[coordinates]:
                ally_count += 1
            else:
                enemy_count += 1
        
    eval_value = (num_enemy - num_ally) + (enemy_count - ally_count)
    
    return eval_value


def successors(state):
    turn = state.turn
    s = []
    for stack in turn:
        new_state = create_new_node(state)
        boom(new_state.board, stack.get_coordinaates())
        s.append(new_state)
        for no_pieces in len(stack):
            for spaces in len(stack):

                piece = stack[no_pieces]
                current_coordinates = piece.coordinates
                new_coordinate = piece.get_new_coordinate(d, spaces)

                for d in Directions:
                    valid = valid_move_check(
                        state.board, stack, no_pieces, current_coordinates, new_coordinate)
                    if not valid:
                        continue
                    else:
                        new_state = create_new_node(state)
                        move(new_state.board, no_pieces, current_coordinates,
                             new_coordinate, new_state.turn)
                        s.append(new_state)
    return s


def create_new_node(state):
    new_board = state.board.get_copy()
    new_state = Node(new_board, state)
    new_state.swap_turn()
    return new_state
