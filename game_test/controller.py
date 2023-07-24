import random
from search import Pathfinder
from graphics import Ghost
from utils import translate_maze_to_screen, translate_screen_to_maze, get_maze


class PacmanGameController:
    def __init__(self, maze_name):
        # self.ascii_maze = [
        #     "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        #     "XP           XX            X",
        #     "X XXXX XXXXX XX XXXXX XXXX X",
        #     "X XXXXOXXXXX XX XXXXXOXXXX X",
        #     "X XXXX XXXXX XX XXXXX XXXX X",
        #     "X                          X",
        #     "X XXXX XX XXXXXXXX XX XXXX X",
        #     "X XXXX XX XXXXXXXX XX XXXX X",
        #     "X      XX    XX    XX      X",
        #     "XXXXXX XXXXX XX XXXXX XXXXXX",
        #     "XXXXXX XXXXX XX XXXXX XXXXXX",
        #     "XXXXXX XX     G    XX XXXXXX",
        #     "XXXXXX XX XXX  XXX XX XXXXXX",
        #     "XXXXXX XX X      X XX XXXXXX",
        #     "   G      X      X          ",
        #     "XXXXXX XX X      X XX XXXXXX",
        #     "XXXXXX XX XXXXXXXX XX XXXXXX",
        #     "XXXXXX XX    G     XX XXXXXX",
        #     "XXXXXX XX XXXXXXXX XX XXXXXX",
        #     "XXXXXX XX XXXXXXXX XX XXXXXX",
        #     "X            XX            X",
        #     "X XXXX XXXXX XX XXXXX XXXX X",
        #     "X XXXX XXXXX XX XXXXX XXXX X",
        #     "X   XX       G        XX   X",
        #     "XXX XX XX XXXXXXXX XX XX XXX",
        #     "XXX XX XX XXXXXXXX XX XX XXX",
        #     "X      XX    XX    XX      X",
        #     "X XXXXXXXXXX XX XXXXXXXXXX X",
        #     "X XXXXXXXXXX XX XXXXXXXXXX X",
        #     "X   O                 O    X",
        #     "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        # ]

        self.maze, self.size, self.pacman_pos = get_maze(maze_name)

        self.numpy_maze = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            "images/ghost.png",
            "images/ghost_pink.png",
            "images/ghost_orange.png",
            "images/ghost_blue.png",
        ]
        self.npsize = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.maze)

    def request_new_random_path(self, in_ghost: Ghost):
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.get_position())
        path = self.p.get_path_a_star(
            current_maze_coord,
            random_space,
        )
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(test_path)

    def convert_maze_to_numpy(self):
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                if self.maze[row][column] == 0:
                    self.reachable_spaces.append((row, column))
                if self.maze[row][column] == 2:
                    self.cookie_spaces.append((row, column))
                    self.reachable_spaces.append((row, column))
                if self.maze[row][column] == 3:
                    self.ghost_spawns.append((row, column))
