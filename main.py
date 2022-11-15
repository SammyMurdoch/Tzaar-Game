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


def move_piece(start, end, nodes, neighbours, piece_data):
    piece_data[nodes[end][0]] -= 1

    nodes[end] = nodes[start]
    nodes[start] = [None, 0]

    for d, neighbour in enumerate(neighbours[start]):
        if neighbour is not None:
            neighbours[neighbour][(d+3) % 6] = neighbours[start][(d+3) % 6]

    return nodes, neighbours, piece_data


def stack_piece(start, end, nodes, neighbours, piece_data):
    stack_height = nodes[start][1]

    nodes, neighbours, piece_data = move_piece(start, end, nodes, neighbours, piece_data)
    nodes[end][1] += stack_height

    return nodes, neighbours, piece_data


def get_valid_target_nodes(board, neighbours, node, target_colour):
    print(node)
    valid_moves = []

    if board[node][0] is not None:
        for neighbour in neighbours[node]:
            if neighbour is not None:
                if board[neighbour][0][1] == target_colour:
                    valid_moves.append(neighbour)

    return valid_moves


def sub_turn(board, neighbours, piece_data, target_colour, player):
    print("What is your starting node?")
    start = eval(input())
    print(start, type(start))
    print("Your valid target nodes are:", get_valid_target_nodes(board, neighbours, start, target_colour))

    print("What node do you want to move to?")
    end = eval(input())

    if target_colour == player:
        nodes, neighbours, piece_data = move_piece(start, end, board, neighbours, piece_data)

    else:
        nodes, neighbours, piece_data = stack_piece(start, end, board, neighbours, piece_data)

    return nodes, neighbours, piece_data


def turn(board, neighbours, piece_data, player):
    print("First move: Take")

    nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, (player+1)%2, player)

    print(board)

    print("Second Move: Take, Stack or Pass")
    second_move = input("Take: 0, Stack: 1, Pass: 2\n")

    if second_move == "0":
        nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, (player+1)%2, player)

    elif second_move == "1":
        nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, player, player)

    print(board)

    return nodes, neighbours, piece_data


piece_data = {("W-Tzaar", 0): 6, ("W-Tzaara", 0): 9, ("W-Tott", 0): 15, ("B-Tzaar", 1): 6, ("B-Tzaara", 1): 9, ("B-Tott", 1): 15}
directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]

board, neighbours = generate_board_dict(piece_data, directions)

# board, neighbours, piece_data = move_piece((0, 1), (0, 0), board, neighbours, piece_data)
# board, neighbours, piece_data = stack_piece((0, 3), (0, 4), board, neighbours, piece_data)

# print(get_valid_target_nodes(board, neighbours, (0, 2), 0))
# print(get_valid_target_nodes(board, neighbours, (0, 2), 1))

#
# print(neighbours)

print(board)
turn(board, neighbours, piece_data, 0)