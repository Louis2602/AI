from enum import Enum


class Direction(Enum):
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360


class ScoreType(Enum):
    COOKIE = 10
    POWERUP = 50
    GHOST = 400


class GhostBehaviour(Enum):
    CHASE = 1
    SCATTER = 2


def translate_screen_to_maze(in_coords, in_size=32):
    return int(in_coords[0] / in_size), int(in_coords[1] / in_size)


def translate_maze_to_screen(in_coords, in_size=32):
    return in_coords[0] * in_size, in_coords[1] * in_size


def draw_path(pacman_game, game_renderer, unified_size, GameObject, Wall):
    red = (255, 0, 0)
    green = (0, 255, 0)
    _from = (1, 1)
    _to = (24, 14)
    path_array = pacman_game.p.get_path(_from[1], _from[0], _to[1], _to[0])

    white = (255, 255, 255)
    for path in path_array:
        game_renderer.add_game_object(
            Wall(game_renderer, path[0], path[1], unified_size, white)
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
