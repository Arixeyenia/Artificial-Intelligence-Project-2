from operator import itemgetter

from mimikyu.game import Board
from mimikyu.actions import sort_list_of_coordinates

class TT:
    def __init__(self, colour):
        if (colour == "black"):
            self.TT = {
                sort_list_of_coordinates([(0, 7), (1, 7),   (3, 7), (4, 7),   (6, 7), (7, 7),
                (0, 6), (1, 6),   (3, 6), (4, 6),   (6, 6), (7, 6)]): ("MOVE", 1, (1,6), (0,6)),
                
                sort_list_of_coordinates([(0, 7), (1, 7),   (3, 7), (4, 7),   (6, 7),(7, 7),
                (0, 6),           (3, 6), (4, 6),   (6, 6), (7, 6)]): ("MOVE", 2, (0,6), (0,7)),

                sort_list_of_coordinates([(0, 7), (1, 7),   (3, 7), (4, 7),   (6, 7),(7, 7),
                                   (3, 6), (4, 6),   (6, 6), (7, 6)]): ("MOVE", 3, (0,7), (1,7)),

                sort_list_of_coordinates([        (1, 7),   (3, 7), (4, 7),   (6, 7),(7, 7),
                                   (3, 6), (4, 6),   (6, 6), (7, 6)]): ("MOVE", 4, (1,7), (4,7)),

                sort_list_of_coordinates([                  (3, 7), (4, 7),   (6, 7),(7, 7),
                                   (3, 6), (4, 6),   (6, 6), (7, 6)]): ("MOVE", 1, (3,6), (4,6)),

                sort_list_of_coordinates([                  (3, 7), (4, 7),   (6, 7),(7, 7),
                                           (4, 6),   (6, 6), (7, 6)]): ("MOVE", 1, (3,7), (4,7)),

                sort_list_of_coordinates([                          (4, 7),   (6, 7),(7, 7),
                                           (4, 6),   (6, 6), (7, 6)]): ("MOVE", 1, (4,6), (4,7))
            }
        else:
            self.TT = {
                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),   (6, 1), (7, 1), 
                (0, 0), (1, 0),   (3, 0), (4, 0),   (6, 0), (7, 0)]): ("MOVE", 1, (6,1), (7,1)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),           (7, 1), 
                (0, 0), (1, 0),   (3, 0), (4, 0),   (6, 0), (7, 0)]): ("MOVE", 1, (7,1), (7,0)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),            
                (0, 0), (1, 0),   (3, 0), (4, 0),   (6, 0), (7, 0)]): ("MOVE", 1, (7,0), (6,0)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),            
                (0, 0), (1, 0),   (3, 0), (4, 0),   (6, 0)        ]): ("MOVE", 1, (6,0), (3,0)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1), (4, 1),            
                (0, 0), (1, 0),   (3, 0), (4, 0),                 ]): ("MOVE", 1, (4,1), (3,1)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1),           
                (0, 0), (1, 0),   (3, 0), (4, 0),                 ]): ("MOVE", 1, (4,0), (3,0)),

                sort_list_of_coordinates([(0, 1), (1, 1),   (3, 1),           
                (0, 0), (1, 0),   (3, 0)                          ]): ("MOVE", 1, (3,1), (3,0))
            }

    def get_move(self, board):
        our_coordinates = sort_list_of_coordinates(board.ally)

        for key in self.TT:
            all_match = True

            for coordinates in key:

                if all_match:
                    for one_coordinate in our_coordinates:
                        if(one_coordinate != coordinates):
                            all_match = False
                            break
                
                else:
                    break
            
            if all_match:
                return self.TT[our_coordinates]
