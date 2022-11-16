import random
import numpy as np

def generate_connections(node, nodes, directions):
    connections = [(node[0] + dir[0], node[1] + dir[1]) if (node[0] + dir[0], node[1] + dir[1]) in nodes else None for dir in directions]

    return connections


def generate_board_dict(piece_data, directions, side_length=5, xy_0=(0, 0), s=5, d=1):
    max_row_length = 2 * side_length - 1

    board_keys = [(x, y) for x in range(max_row_length) for y in range(max_row_length - abs(x-side_length+1))]
    board_keys.remove((side_length - 1, side_length - 1))

    piece_order = [key for key, value in piece_data.items() for i in range(value)]
    random.shuffle(piece_order)

    node_pixel_coordinates = generate_node_coordinate_array(board_keys, xy_0, d, s)

    node_data = [[piece, 1, node_pixel_coordinates[i]] for i, piece in enumerate(piece_order)]
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

    print("Your valid target nodes are:", get_valid_target_nodes(board, neighbours, start, target_colour))

    print("What node do you want to move to?")
    end = eval(input())

    if target_colour == player:
        nodes, neighbours, piece_data = move_piece(start, end, board, neighbours, piece_data)

    else:
        nodes, neighbours, piece_data = stack_piece(start, end, board, neighbours, piece_data)

    return nodes, neighbours, piece_data


def turn(board, neighbours, piece_data, player, start=False):
    if check_game_end(board, neighbours, piece_data, player):
        return board, neighbours, piece_data, (player + 1) % 2

    print("First move: Take")

    nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, (player+1) % 2, player)

    if check_game_end(board, neighbours, piece_data, player):
        return nodes, neighbours, piece_data, player

    if not start:
        print("Second Move: Take, Stack or Pass")
        second_move = input("Take: 0, Stack: 1, Pass: 2\n")

        if second_move == "0":
            nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, (player+1) % 2, player)

            if check_game_end(board, neighbours, piece_data, player):
                return nodes, neighbours, piece_data, player

        elif second_move == "1":
            nodes, neighbours, piece_data = sub_turn(board, neighbours, piece_data, player, player)

            if check_game_end(board, neighbours, piece_data, player):
                return nodes, neighbours, piece_data, (player + 1) % 2

    return nodes, neighbours, piece_data, None


def check_take_possible(board, neighbours, player):
    for node in neighbours:
        if len(get_valid_target_nodes(board, neighbours, node, (player + 1) % 2)) > 0:
            return True

    return False


def check_game_end(board, neighbours, piece_data, player): # TODO test this
    if 0 in piece_data.values():
        return True

    elif not check_take_possible(board, neighbours, player):
        return True

    return False


def generate_node_coordinate_array_upper(nodes, d, s):
    coord_array = np.array(nodes)

    coord_array = np.apply_along_axis(lambda node: (d*np.sqrt(3)/2 * (node[1]-node[0]), d/2 * (node[1]+node[0]) - (s-1)*d), 1, coord_array)

    return coord_array


def generate_node_coordinate_array(nodes, centre_coord, d, s):
    upper_nodes = nodes[:int(((3*s**2-s-2)/2))]
    upper_nodes_coord_array = generate_node_coordinate_array_upper(upper_nodes, d, s)

    lower_nodes_coord_array = -1 * upper_nodes_coord_array[:int((3*s**2-5*s+2)/2)][::-1] # rotates the coordinates from the upper

    nodes_coordinate_array = np.concatenate((upper_nodes_coord_array, lower_nodes_coord_array))

    return nodes_coordinate_array + centre_coord


piece_data = {("W-Tzaar", 0): 6, ("W-Tzaara", 0): 9, ("W-Tott", 0): 15, ("B-Tzaar", 1): 6, ("B-Tzaara", 1): 9, ("B-Tott", 1): 15}
directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]

board, neighbours = generate_board_dict(piece_data, directions)
node_pixels = {}

print(board)

###COMMENT OUT AFTER THIS TO STOP THE GAME PLAYING

# player = 0
#
# print("TZAAR")
# print(board)
#
#
# board, neighbours, piece_data, winner = turn(board, neighbours, piece_data, player, True)
#
# player = 1
#
# while winner is None:
#     print("Next Player")
#
#     turn(board, neighbours, piece_data, player)
#     player = (player + 1) % 2
#
#     print(board)
#
# print(winner, "Won!")
#
#