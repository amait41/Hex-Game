#!/usr/bin/env python3
from misc import display
if not display:
    raise Exception('Use the test.py file to perform tests.')
import sys
from time import time
from math import sqrt
import colorama # translate ANSI sequence for Windows
colorama.init()
import pygame

from misc import screen, background
from Game import Game
from Board import Board
from Player import AI, Human

"""
CONTROLS
ESC : Quit the game
"""

####### Init Game, Players and Board instances #######

#init boardgame
board_size = sys.argv[3]
board = Board(board_size)

#init players
RED, BLUE = 1, 2
player1_type = sys.argv[1]
player2_type = sys.argv[2]
ai_algorithms = ['random', 'mc', 'mc_ucb1', 'uct', 'uct_wm']

if player1_type == 'h':   # h for human
    player1 = Human(RED)
elif player1_type in ai_algorithms:
    player1 = AI(RED, player1_type)
else:
    print('Wrong player type.')
    print(f'Available options: {["h"] + ai_algorithms}.')
    exit()

if player2_type == 'h':
    player2 = Human(BLUE)
elif player2_type in ai_algorithms:
    player2 = AI(BLUE, player2_type)
else:
    print(f'Wrong player type.')
    print(f'Available options: {["h"] + ai_algorithms}.')
    exit()

#####################################################


# Let's play ########################################

game = Game(board, player1, player2)
pygame.init()
pygame.display.set_caption("Hex")
screen.blit(background,(0,0))
game.run()

#####################################################


