import pygame
import pygame.gfxdraw
from sys import exit
from main import *


def display_stack_height(board, node):
    stack_height_font = pygame.font.Font(None, 35)
    stack_height = str(board[node][1])

    stack_height_surf = stack_height_font.render(stack_height, True, "White")
    stack_height_rect = stack_height_surf.get_rect(center=board[node][2])

    screen.blit(stack_height_surf, stack_height_rect)


def display_game_over(winner):
    pygame.draw.rect(screen, (119, 77, 37), (218, 288, 300, 250))
    pygame.draw.rect(screen, (167, 122, 68), (218, 288, 300, 250), 10)

    game_over_text_font = pygame.font.SysFont("erasdemiitc", 70)
    winner_text_font = pygame.font.SysFont("erasdemiitc", 40)

    game_surf = game_over_text_font.render("GAME", True, (254, 176, 101))
    game_rect = game_surf.get_rect(center=(368, 350))

    over_surf = game_over_text_font.render("OVER", True, (254, 176, 101))
    over_rect = over_surf.get_rect(center=(368, 415))

    winner_surf = winner_text_font.render(f"{winner} Won!", True, (254, 176, 101))
    winner_rect = winner_surf.get_rect(center=(368, 480))

    screen.blit(game_surf, game_rect)
    screen.blit(over_surf, over_rect)
    screen.blit(winner_surf, winner_rect)


def display_turn_information(player, phase):
    if player == 0:
        player_name = "White"

    else:
        player_name = "Black"

    if phase == 0:
        phase_info = "take a piece."

    else:
        phase_info = "take a piece, stack a piece or pass."

    player_text_font = pygame.font.Font(None, 30)
    player_text_surf = player_text_font.render(f"{player_name} to move,", True, "White")

    phase_info_font = pygame.font.Font(None, 18)
    phase_info_surf = phase_info_font.render(f"You can {phase_info}", True, "White") # TODO Check if take, stack are possible

    screen.blit(player_text_surf, (15, 55))
    screen.blit(phase_info_surf, (15, 80))


def update_phase_player(phase, player):
    phase = (phase + 1) % 2

    if phase == 0:
        player = (player + 1) % 2

    return phase, player


def display_pass(phase, player, m_down_pos):
    if phase == 1:
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

        if pass_surface_rect.collidepoint(m_down_pos):
            phase, player = update_phase_player(phase, player)

    return phase, player


def display_valid_move_indicator(location):
    pygame.gfxdraw.aacircle(screen, int(location[0]), int(location[1]), 36, (0, 128, 255, 100))
    pygame.gfxdraw.filled_circle(screen, int(location[0]), int(location[1]), 36, (0, 128, 255, 100))


def display_piece(board, node):
    piece_rects[board[node][0][0]].center = board[node][2]
    screen.blit(piece_surfs[board[node][0][0]], piece_rects[board[node][0][0]])

    display_stack_height(board, node)


pygame.init()

screen = pygame.display.set_mode((736, 826))

pygame.display.set_caption("TZAAR")

clock = pygame.time.Clock()

piece_data = piece_data_fixed.copy()

board_surf = pygame.image.load("Board.jpg").convert_alpha()

piece_surfs = {piece_type[0]: pygame.image.load(piece_type[2]).convert_alpha() for piece_type in piece_data.keys()}
piece_rects = {piece_type: piece_surfs[piece_type].get_rect() for piece_type in piece_surfs.keys()}

board, neighbours = generate_board_dict(piece_data)

selected_nodes = [None, None]
valid_move_nodes = []

player = 0
phase = 0

winner = None
winner_colour = None

first_turn = True

while True:
    m_pos = (0, 0)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        if ev.type == pygame.KEYDOWN:  # TODO make this a restart at the end of the game
            if ev.key == pygame.K_SPACE:
                if winner is not None:
                    piece_data = piece_data_fixed.copy()

                    board, neighbours = generate_board_dict(piece_data)

                    selected_nodes = [None, None]
                    valid_move_nodes = []

                    player = 0
                    phase = 0

                    winner = None
                    winner_colour = None

                    first_turn = True

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()

    screen.blit(board_surf, (0, 0))

    if winner is None:
        phase, player = display_pass(phase, player, m_pos)
        display_turn_information(player, phase)

    for node in board:
        if board[node][0] is not None:

            display_piece(board, node)

            if winner is None:
                if node in valid_move_nodes:
                    display_valid_move_indicator(board[node][2])

                if piece_rects[board[node][0][0]].collidepoint(m_pos):
                    if selected_nodes[0] is None and board[node][0][1] == player:
                        selected_nodes[0] = node

                        valid_move_nodes = get_valid_target_nodes(board, neighbours, node, (player + 1) % 2, phase)

                    elif node not in valid_move_nodes:
                        # TODO Change this to anywhere on the board other than valid nodes
                        # TODO if you click on a piece which is yours and you can't move to set that as first piece selected

                        selected_nodes[0] = None
                        valid_move_nodes = []

                    else:
                        selected_nodes[1] = node

                        if board[selected_nodes[1]][0][1] != player:
                            board, neighbours, piece_data = move_piece(selected_nodes[0], selected_nodes[1], board, neighbours, piece_data)

                        else:
                            board, neighbours, piece_data = stack_piece(selected_nodes[0], selected_nodes[1], board, neighbours, piece_data)

                        selected_nodes = [None, None]
                        valid_move_nodes = []

                        if first_turn:
                            first_turn = False

                            player = 1

                        else:
                            phase, player = update_phase_player(phase, player)

                            end_game, winner = check_game_end(board, neighbours, piece_data, player)

                            winner_colour = "White" if winner == 0 else "Black"

            else:
                display_game_over(winner_colour)

    pygame.display.update()
    clock.tick(60)
