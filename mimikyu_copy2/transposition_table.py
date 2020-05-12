from operator import itemgetter

from mimikyu_copy2.game import Board
from mimikyu_copy2.actions import sort_list_of_coordinates

class TT:
    def __init__(self, colour):
        if (colour == "black"):

            #dictionary cannot use list as key.
            self.TT = {
                tuple(sort_list_of_coordinates([(0, 7), (1, 7),   (3, 7), (4, 7),   (6, 7), (7, 7),
                (0, 6), (1, 6),    (3, 6), (4, 6),   (6, 6), (7, 6)])): ("MOVE", 1, (3,7), (3,6)),
                
                tuple(sort_list_of_coordinates([(0, 7), (1, 7),    (4, 7),   (6, 7), (7, 7),
                (0, 6), (1, 6),    (3, 6), (4, 6),   (6, 6), (7, 6)])): ("MOVE", 2, (3,6), (3,4)),

                tuple(sort_list_of_coordinates([(0, 7), (1, 7),    (4, 7),   (6, 7),
                (0, 6), (1, 6),    (3, 4), (4, 6),   (6, 6), (7,4)])): ("MOVE", 2, (3,4), (3,2)),

                tuple(sort_list_of_coordinates([(0, 7), (1, 7),    (4, 7),   (6, 7),
                (0, 6), (1, 6),    (3, 2), (4, 6),   (6, 6), (7,2)])): ("MOVE", 1, (3,2), (5,2))
            }
        else:
            self.TT = {
                tuple(sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),   (6, 1), (7, 1), 
                (0, 0), (1, 0),   (3, 0), (4, 0),   (6, 0), (7, 0)])): ("MOVE", 1, (4,0), (4,1)),

                tuple(sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),  (6, 1), (7, 1), 
                (0, 0), (1, 0),   (3, 0),   (6, 0), (7, 0)])): ("MOVE", 2, (4,1), (4,3)),

                tuple(sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1),   (6, 1), (7, 1),          
                (0, 0), (1, 0),   (3, 0), (4, 3),   (6, 0), (7, 0)])): ("MOVE", 2, (4,3), (4,5)),

                tuple(sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1),   (6, 1), (7, 1),          
                (0, 0), (1, 0),   (3, 0), (4, 5),   (6, 0), (7, 0)])): ("MOVE", 1, (4,5), (2,5))
            }

    def get_move(self, board):
        #Convert to list to sort, then convert to tuple to compare
        our_coordinates = tuple(sort_list_of_coordinates(list(board.ally)))

        for key in self.TT:
            if key == our_coordinates:
                return self.TT[our_coordinates]

        return False