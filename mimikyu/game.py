import enum
import copy


class Piece:
    def __init__(self, coordinates, colour):
        self.coordinates = coordinates
        self.colour = colour

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_new_coordinates(self, direction, spaces):
        if direction == Directions.left:
            new_coordinates = self.coordinates[0] - spaces
        elif direction == Directions.right:
            new_coordinates = self.coordinates[0] + spaces
        elif direction == Directions.up:
            new_coordinates = self.coordinates[1] + spaces
        elif direction == Directions.down:
            new_coordinates = self.coordinates[1] - spaces

        return new_coordinates

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
    
    def get_new_coordinates(self, direction, spaces):
        if direction == Directions.left:
            new_coordinates = (self.get_coordinates()[0] - spaces, self.get_coordinates()[1])
        elif direction == Directions.right:
            new_coordinates = (self.get_coordinates()[0] + spaces, self.get_coordinates()[1])
        elif direction == Directions.up:
            new_coordinates = (self.get_coordinates()[0], self.get_coordinates()[1] + spaces)
        elif direction == Directions.down:
            new_coordinates = (self.get_coordinates()[0], self.get_coordinates()[1] - spaces)
        return new_coordinates


class Board:
    def __init__(self, ally, enemy, colour):
        self.ally = ally
        self.enemy = enemy
        self.my_colour = colour[0].upper()

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
