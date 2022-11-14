import random
from numpy import *


def generate_board_dict(piece_data, side_length=5):
    max_row_length = 2 * side_length - 1

    board_keys = [(x, y) for x in range(max_row_length) for y in range(max_row_length - abs(x-side_length+1))]
    board_keys.remove((side_length - 1, side_length - 1))

    piece_order = [key for key, value in piece_data.items() for i in range(value)]
    random.shuffle(piece_order)

    node_data = [[piece, 1] for piece in piece_order]

    board = dict(zip(board_keys, node_data))

    return board


def move_piece(start, end, board):
    board[end] = board[start]
    board[start] = [None, 0]

    return board


def stack_piece(start, end, board):
    stack_height = board[start][1]

    board = move_piece(start, end, board)
    board[end][1] += stack_height

    return board




piece_data = {"W-Tzaar": 6, "W-Tzaara": 9, "W-Tott": 15, "B-Tzaar": 6, "B-Tzaara": 9, "B-Tott": 15}

board = generate_board_dict(piece_data)

print(board)

move_piece((0, 0), (0, 1), board)
stack_piece((0, 2), (0, 3), board)

print(board)
