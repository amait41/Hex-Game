from random import choice


class AI_player:

    def __init__(self, color):
        self.color = color


    def plays(self, board, i=None, j=None):
        if i == None:
            i, j = board.action_to_coord(choice(board.actions))
        return board.update(self.color, i, j)