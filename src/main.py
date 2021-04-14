#!/usr/bin/env python3
import sys
from time import time
from math import sqrt
import colorama # translate ANSI sequence for Windows
colorama.init()
from misc import display
if display:
    import pygame
    from misc import screen, background
    from Player import Human
from Game import Game
from Player import AI
from Board import Board
from test import test

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
ai_algorithms = ['rand', 'mc', 'mc_ucb1', 'mcts']

if display:
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


# Let's play ####################

if display:
    game = Game(board, player1, player2)
    pygame.init()
    pygame.display.set_caption("Hex")
    screen.blit(background,(0,0))
    game.run()

if not display:
    test('test1', player1_type, player2_type, board_size)

#####################################################


