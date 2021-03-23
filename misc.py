import pygame
import sys

board_size = sys.argv[3]
background = pygame.image.load(f"img/Hex_board_{board_size}.png")
screen = pygame.display.set_mode((1300,900))