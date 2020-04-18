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
    def __init__(self, pieces, colour):
        self.pieces = pieces
        self.colour = colour
        self.number = len(pieces)
        self.coordinates = pieces[0].coordinates
        self.prev_coordinates = None

    def __str__(self):
        return self.colour + str(self.number)

    def remove_pieces(self, pieces):
        for piece in pieces:
            self.pieces.remove(piece)
            self.number -= 1

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def add_stack(self, stack):
        self.pieces += stack.pieces
        self.number = len(self.pieces)

    def get_substack(self, no_pieces):
        return Stack(self.pieces[:no_pieces], self.colour)
        
class Cluster:
      def __init__(self, coordinates, intersection):
        self.coordinates = coordinates
        self.intersection = intersection
        
class Board:
    def __init__(self, black, white):
        self.black = black
        self.white = white

    def get_white(self):
        return self.white
    
    def get_black(self):
        return self.black

    def get_board_dict(self):
        board_dict = self.white.copy()
        board_dict.update(self.black.copy())
        
        return board_dict

    def get_copy(self):
        return copy.deepcopy(self)

class Directions(enum.Enum):
    left = 1
    right = 2
    up = 3
    down = 4