from mimikyu.game import Piece, Board, Directions, Stack
from mimikyu.actions import move, boom

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.game_board = Board({},{}, colour)
        self.colour = colour

        _BLACK_START_SQUARES = [(0,7), (1,7),   (3,7), (4,7),   (6,7), (7,7), (0,6), (1,6),   (3,6), (4,6),   (6,6), (7,6)]
        _WHITE_START_SQUARES = [(0,1), (1,1),   (3,1), (4,1),   (6,1), (7,1), (0,0), (1,0),   (3,0), (4,0),   (6,0), (7,0)]
        for coordinate in _BLACK_START_SQUARES:
            black_piece = Piece(coordinate, "B")
            black_stack = Stack([black_piece])
            if colour == "black":
                self.game_board.ally[coordinate] = black_stack
            else:
                self.game_board.enemy[coordinate] = black_stack

        for coordinate in _WHITE_START_SQUARES:
            white_piece = Piece(coordinate, "W")
            white_stack = Stack([white_piece])
            if colour == "white":
                self.game_board.ally[coordinate] = white_stack
            else:
                self.game_board.enemy[coordinate] = white_stack
        

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        return ("BOOM", (0, 0))


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        is_ally = (self.colour == colour)
        if is_ally:
            turn = self.game_board.ally
        else:
            turn = self.game_board.enemy
        
        if action[0] == "MOVE":
            move(self.game_board, action[1], action[2], action[3], turn)

        elif action[0] == "BOOM":
            boom(self.game_board, action[1])
