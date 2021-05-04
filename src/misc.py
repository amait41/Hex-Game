import sys
try:
    display = True if sys.argv[4]==1 else False
except IndexError:
    display = True
except ValueError:
    display = False
    
if display:
    import pygame
    board_size = sys.argv[3]
    background = pygame.image.load(f"img/Hex_board_{board_size}.png")
    screen = pygame.display.set_mode((1300,900))