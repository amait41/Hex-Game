from misc import display
if display:
    import pygame
    from misc import background, screen
from AI.dispatcher import *


class Player:

    def __init__(self, color):
        self.color = color
        self.name = 'Red player' if self.color==1 else 'Blue player'

    
class Human(Player):

    def __init__(self, color):
        super().__init__(color)
   
    def plays(self, board):
        pos = pygame.mouse.get_pos()
        if background.get_at(pos) == (223, 223, 223, 255):
            return board.update(pos, self.color)

                
class AI(Player):

    def __init__(self, color, algorithm):
        super().__init__(color)
        algorithms = {
                    'random': random,    # random
                    'mc': mc,            # Monte_Carlo
                    'mc_ucb1': mc_ucb1,  # Monte-Carlo + UUpperConfidenceBound 1
                    'uct': uct,          # Upper Confidence bounds for Trees
                    'uct_wm': uct_wm,    # Upper Confidence bounds for Trees With Memory
                    }
        self.algorithm_name = algorithm
        self.algorithm = algorithms[algorithm]
        self.explorationConstant = 0.13
        self.tree = None

    def plays(self, board):
        if self.algorithm_name == 'uct_wm':
            self.tree, (i,j) = self.algorithm(board, self.color, self.explorationConstant, self.tree)
        else:
            (i,j) = self.algorithm(board, self.color, self.explorationConstant)
        tile_center = board.tiles_centers[board.coord_to_index(i, j)]
        return board.update(tile_center, self.color, True)
    
    def __str__(self):
        return f"{self.color},{self.name},{self.algorithm_name}"
