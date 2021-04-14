import sys
try:
    display = bool(int(sys.argv[4]))
except IndexError:
    display = True
    
if display:
    import pygame
    board_size = sys.argv[3]
    background = pygame.image.load(f"img/Hex_board_{board_size}.png")
    screen = pygame.display.set_mode((1300,900))