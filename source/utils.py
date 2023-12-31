from enum import Enum
import pygame


class Direction(Enum):
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360


class ScoreType(Enum):
    COOKIE = 20
    STEP = -1


def translate_screen_to_maze(in_coords, in_size=32):
    return int(in_coords[1] / in_size), int(in_coords[0] / in_size)


def translate_maze_to_screen(in_coords, in_size=32):
    return in_coords[1] * in_size, in_coords[0] * in_size


def draw_path(
    pacman_game,
    game_renderer,
    unified_size,
    GameObject,
    Wall,
    _from,
    _to,
):
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)
    gray = (211, 211, 211)

    path_array = pacman_game.p.get_path_a_star(_from, _to)

    for path in path_array:
        game_renderer.add_game_object(
            Wall(game_renderer, path[1], path[0], unified_size, gray)
        )

    from_translated = translate_maze_to_screen(_from)
    game_renderer.add_game_object(
        GameObject(
            game_renderer, from_translated[0], from_translated[1], unified_size, red
        )
    )

    to_translated = translate_maze_to_screen(_to)
    game_renderer.add_game_object(
        GameObject(
            game_renderer, to_translated[0], to_translated[1], unified_size, green
        )
    )
    return path_array


"""
The function get maze will return a 2D array, maze size (m x n) and pos of pacman (x, y)
This is a coordinate and each element hold a value, present it is empty (0), wall (1), monster (3) or food (@)
Ex maze:
    0 0 1 0
    0 0 1 2
    0 0 3 0
    0 0 0 0
--> maze[2][2] will be 3
"""


def string_to_number(str):
    return [int(i) for i in str]


def get_maze(filename):
    f = open(filename, "r")
    maze, pos, size = [], [], []
    size = f.readline()
    temp = f.readlines()

    for index in range(len(temp)):
        maze.append(string_to_number(temp[index].split()))

    pos = maze.pop(-1)
    size = tuple(string_to_number(size.split()))
    return maze, size, pos
