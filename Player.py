import pygame
from misc import background, screen
from AI.Algorithm_AI import *

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

    def __init__(self, color, algorithm,explorationConstant=None):
        super().__init__(color)
        algorithms = {
                    'random':run_random,    # random
                    'mc0':run_mc0,          # simple monte-carlo v0
                    'mc':run_mc,            # simple monte-carlo v1
                    'mc_ucb1':run_mc_ucb1,  # mc + ucb1
                    'mcts':run_mcts         # monte-carlo tree search
                    }
        self.algorithm_name = algorithm
        self.algorithm = algorithms[algorithm]
        self.explorationConstant = explorationConstant

    def plays(self, board):
        if self.algorithm in ['mc_ucb1','mcts']:
            pos = self.algorithm(board, self.color, self.explorationConstant)
        else:
            pos = self.algorithm(board, self.color)
        tile_center = board.tiles_centers[board.coord_to_action(pos[0], pos[1])]
        return board.update(tile_center, self.color, True)
    
    def __str__(self):
        return f"{self.color},{self.name},{self.algorithm_name}"