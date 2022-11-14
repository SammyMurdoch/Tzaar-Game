import random
from numpy import *


def generate_connections(node, nodes, directions):
    connections = [(node[0] + dir[0], node[1] + dir[1]) if (node[0] + dir[0], node[1] + dir[1]) in nodes else None for dir in directions]

    return connections


def generate_board_dict(piece_data, directions, side_length=5):
    max_row_length = 2 * side_length - 1

    board_keys = [(x, y) for x in range(max_row_length) for y in range(max_row_length - abs(x-side_length+1))]
    board_keys.remove((side_length - 1, side_length - 1))

    piece_order = [key for key, value in piece_data.items() for i in range(value)]
    random.shuffle(piece_order)

    node_data = [[piece, 1] for piece in piece_order]
    node_dict = dict(zip(board_keys, node_data))
    
    neighbour_data = [generate_connections(node, board_keys, directions) for node in board_keys]
    neighbour_dict = dict(zip(board_keys, neighbour_data))

    return node_dict, neighbour_dict


def move_piece(start, end, nodes, neighbours):
    nodes[end] = nodes[start]
    nodes[start] = [None, 0]

    for d, neighbour in enumerate(neighbours[start]):
        if neighbour is not None:
            neighbours[neighbour][(d+3) % 6] = neighbours[start][(d+3) % 6]

    return nodes, neighbours


def stack_piece(start, end, nodes, neighbours):
    stack_height = nodes[start][1]

    nodes, neighbours = move_piece(start, end, nodes, neighbours)
    nodes[end][1] += stack_height

    return nodes, neighbours


piece_data = {"W-Tzaar": 6, "W-Tzaara": 9, "W-Tott": 15, "B-Tzaar": 6, "B-Tzaara": 9, "B-Tott": 15}
directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]

board, neighbours = generate_board_dict(piece_data, directions)

print(neighbours)

board, neighbours = move_piece((0, 1), (0, 0), board, neighbours)
board, neighbours = stack_piece((0, 2), (0, 3), board, neighbours)

print(neighbours)

print(neighbours[(0, 2)])