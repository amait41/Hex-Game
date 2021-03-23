import pygame
from misc import background, screen
from AI.Algorithm_AI import run_random, run_mc, run_mcts


class Player:

    def __init__(self, color):
        self.color = color
        self.name = 'Red player' if self.color==1 else 'Blue player'

    
class Human(Player):

    def __init__(self, color):
        super().__init__(color)
   

    def plays(self, board):
        have_play = False
        pos = pygame.mouse.get_pos()

        if background.get_at(pos) == (223, 223, 223, 255):

            hex_vertices = board.update(pos, self.color)

            if hex_vertices != None:
                color = 'red' if self.color==1 else 'blue'
                pygame.draw.polygon(screen, color, hex_vertices)
                return True

                
class AI(Player):

    def __init__(self, color, algorithm):
        super().__init__(color)
        algorithms = {
                    'random':run_random, # random
                    'mc':run_mc,         # simple monte-carlo
                    'mcts':run_mcts      # monte-carlo tree search
                    }
        self.algorithm = algorithms[algorithm]


    def plays(self, board):
        pos = self.algorithm(board, self.color)
        tile_center = board.tiles_centers[board.coord_to_action(pos[0], pos[1])]
        hex_vertices = board.update(tile_center, self.color, True)
        if hex_vertices != None:
            color = 'red' if self.color==1 else 'blue'
            pygame.draw.polygon(screen, color, hex_vertices)
            return True
