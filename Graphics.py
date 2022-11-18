import pygame
from sys import exit
import numpy as np
from main import *


def display_stack_height(board, node):
    stack_height_font = pygame.font.Font(None, 35)
    stack_height = str(board[node][1])

    stack_height_surf = stack_height_font.render(stack_height, True, "White")

    stack_height_rect = stack_height_surf.get_rect(center=board[node][2])

    screen.blit(stack_height_surf, stack_height_rect)


def display_pass():
    pass_font = pygame.font.Font(None, 70)
    pass_colour = "White"
    pass_font_surf = pass_font.render("PASS", True, pass_colour)
    pass_surface_rect = pass_font_surf.get_rect(topright=(681, 55))

    if pass_surface_rect.collidepoint(pygame.mouse.get_pos()):
        pass_colour = "Grey"

    else:
        pass_colour = "White"

    pass_font_surf = pass_font.render("PASS", True, pass_colour)

    screen.blit(pass_font_surf, pass_surface_rect)


pygame.init()

screen = pygame.display.set_mode((736, 826))

pygame.display.set_caption("TZAAR")

clock = pygame.time.Clock()

board_surf = pygame.image.load("Board.jpg").convert_alpha()

piece_surfs = {piece_type[0]: pygame.image.load(piece_type[2]).convert_alpha() for piece_type in piece_data.keys()}
piece_rects = {piece_type: piece_surfs[piece_type].get_rect() for piece_type in piece_surfs.keys()}

board, neighbours = generate_board_dict(piece_data, directions)

print(board)

#board, neighbours, piece_data, winner = turn(board, neighbours, piece_data, 0)

print(board)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                piece_data = piece_data_fixed.copy()

                board, neighbours = generate_board_dict(piece_data, directions)
                print(board)
                print(piece_data)

    screen.blit(board_surf, (0, 0))

    display_pass()

    for node in board:
        if board[node][0] is not None:
            piece_rects[board[node][0][0]].center = board[node][2]
            screen.blit(piece_surfs[board[node][0][0]], piece_rects[board[node][0][0]])

            display_stack_height(board, node)


    pygame.display.update()
    clock.tick(60)
