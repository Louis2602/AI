from graphics import Hero, Cookie, Wall, Ghost, GameRenderer, GameObject
from utils import GhostBehaviour, draw_path
from controller import PacmanGameController
from utils import translate_maze_to_screen


def get_maze_path():
    string = input("Input maze name: ")
    string = "./input/" + string + ".txt"
    return string


if __name__ == "__main__":
    unified_size = 32
    maze_name = get_maze_path()
    # level = int(input("Input level of game (1/2/3/4): "))
    # speed = int(input("Input game speed (ms): "))

    pacman_game = PacmanGameController(maze_name)
    size = pacman_game.size
    game_renderer = GameRenderer(
        size[1] * unified_size, size[0] * unified_size
    )  # width = size[1], height = size[0]

    for y, row in enumerate(pacman_game.maze):
        for x, column in enumerate(row):
            if column == 1:
                game_renderer.add_wall(Wall(game_renderer, x, y, unified_size))

    # Draw path
    # path_array = draw_path(pacman_game, game_renderer, unified_size, GameObject, Wall)

    for cookie_space in pacman_game.cookie_spaces:
        translated = translate_maze_to_screen(cookie_space)
        cookie = Cookie(
            game_renderer,
            translated[0] + unified_size / 2,
            translated[1] + unified_size / 2,
        )
        game_renderer.add_cookie(cookie)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = translate_maze_to_screen(ghost_spawn)
        ghost = Ghost(
            game_renderer,
            translated[0],
            translated[1],
            unified_size,
            pacman_game,
            pacman_game.ghost_colors[i % 4],
        )
        game_renderer.add_ghost(ghost)

    pacman = Hero(game_renderer, pacman_game, unified_size, unified_size, unified_size)
    game_renderer.add_hero(pacman)
    game_renderer.set_current_mode(GhostBehaviour.CHASE)
    game_renderer.tick(120)
