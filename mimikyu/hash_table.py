import random

from mimikyu.game import Board, Stack

#constants for hash function
_ally = 0
_enemy = 1
#board spaces
_width = 8
_height = 8
#white or black
_colour = 2
#number possible in stack
_num_stack = 12


_our_hash_table = None

def initialise_our_hash():
    global _our_hash_table
    _our_hash_table = Hash_table()


#using zobrist hashing altered for expendibots
class Hash_table:

    def __init__(self):
        global _width
        global _height
        _width = 8
        _height = 8

        global _colour
        _colour = 2
        
        global _num_stack
        _num_stack = 12
        

        self.table = [[[[[0 for x in range(_num_stack)] for y in range(_colour)] for a in range(_height)] for b in range(_width)] for w in range(_colour)]
        for h in range(_colour):
            for i in range(_width):
                for j in range(_height):
                    for k in range(_colour):
                        for l in range(_num_stack):
                            self.table[h][i][j][k][l] = random.randint(0, 2**64 - 1)

    def hash_board(self, board, turn):

        global _ally
        global _enemy
        global _width
        global _height
        global _colour
        global _num_stack

        ally = board.ally
        enemy = board.enemy
        cur_turn = 0
        if list(turn.values())[0].get_colour() == list(board.ally.values())[0].get_colour():
            cur_turn = _ally
        else:
            cur_turn = _enemy

        h_score = 0
        for coordinates, stack in ally.items():
            x = coordinates[0]
            y = coordinates[1]
            number_stack = stack.get_number()
            h_score = h_score ^ self.table[cur_turn][x][y][_ally][number_stack]

        for coordinates, stack in enemy.items():
            x = coordinates[0]
            y = coordinates[1]
            number_stack = stack.get_number()
            h_score = h_score ^ self.table[cur_turn][x][y][_enemy][number_stack]

        return h_score