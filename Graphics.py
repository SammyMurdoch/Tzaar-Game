import pygame
from sys import exit
import numpy as np
from main import *

pygame.init()

screen = pygame.display.set_mode((736, 826))

pygame.display.set_caption("TZAAR")

clock = pygame.time.Clock()

#test_surface = pygame.Surface((100, 200))

background_surface = pygame.image.load("Board.jpg").convert_alpha()

piece_surfaces = {piece_type[0]: pygame.image.load(piece_type[2]).convert_alpha() for piece_type in piece_data.keys()}
piece_rects = {piece_type: piece_surfaces[piece_type].get_rect() for piece_type in piece_surfaces.keys()}

print(piece_surfaces)
print(piece_rects)

board, neighbours = generate_board_dict(piece_data, directions)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))

    for node in board:
        if board[node][0] is not None:
            piece_rects[board[node][0][0]].center = board[node][2]
            screen.blit(piece_surfaces[board[node][0][0]], piece_rects[board[node][0][0]])

    pygame.display.update()
    clock.tick(60)

