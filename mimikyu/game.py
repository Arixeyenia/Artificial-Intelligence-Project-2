import enum, copy

class Piece:
    def __init__(self, coordinates, colour):
        self.coordinates = coordinates
        self.colour = colour

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def __str__(self):
        return self.colour

class Stack:
    def __init__(self, pieces):
        self.pieces = pieces
        self.prev_coordinates = None

    def __str__(self):
        return self.get_colour + str(self.get_number)

    def remove_pieces(self, pieces):
        for piece in pieces:
            self.pieces.remove(piece)

    def set_coordinates(self, coordinates):
        for piece in self.pieces:
            piece.set_coordinates(coordinates)

    def add_stack(self, stack):
        self.pieces += stack.pieces

    def get_substack(self, no_pieces):
        return Stack(self.pieces[:no_pieces])

    def get_colour(self):
        return self.pieces[0].colour
    
    def get_number(self):
        return len(self.pieces)

    def get_coordinates(self):
        return self.pieces[0].coordinates

class Board:
    def __init__(self, ally, enemy):
        self.ally = ally
        self.enemy = enemy

    def get_board_dict(self):
        board_dict = self.ally.copy()
        board_dict.update(self.enemy.copy())
        
        return board_dict

    def get_copy(self):
        return copy.deepcopy(self)

    def get_ally_count(self):
        return len(self.ally)

    def get_enemy_count(self):
        return len(self.enemy)

class Directions(enum.Enum):
    left = 1
    right = 2
    up = 3
    down = 4