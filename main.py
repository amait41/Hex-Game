#!/usr/bin/env python3
import sys
import pygame
from misc import board_size, screen, background
from time import time
from Game import Game
from Player import Human, AI
from Board import Board
import colorama # translate ANSI sequence for Windows
colorama.init()

"""
CONTROLS
ESC : Quit the game
"""


############### Init window ################

pygame.init()
pygame.display.set_caption("Hex")

#   0__________________x=1300
#   |
#   | (x0,y0)
#   |  
#   |       screen
#   |
#   y=900

#apply boardgame picture
screen.blit(background,(0,0))

#####################################################



####### Init Game, Players and Board instances #######

#init boardgame
board = Board(board_size, background, screen)

#init players
RED, BLUE = 1, 2

if sys.argv[1] == '0':
    player1 = Human(RED)
elif sys.argv[1] == '1':
    player1 = AI(RED, 'mcts')
else:
    print('Veuilliez saisir un type de joueur correct : 0 ou 1.')
    exit()

if sys.argv[2] == '0':
    player2 = Human(BLUE)
elif sys.argv[2] == '1':
    player2 = AI(BLUE, 'mcts')
else:
    print('Veuilliez saisir un type de joueur correct : 0 ou 1.')
    exit()


#init game
game = Game(board, player1, player2)

#####################################################


##################### Let's play ####################

game.run()

#####################################################
