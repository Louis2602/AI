import random
from search import Pathfinder
from setup import Ghost
from utils import translate_maze_to_screen, translate_screen_to_maze


class PacmanGameController:
    def __init__(self):
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
        self.ascii_maze = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XP           XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X                          X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X      XX    XX    XX      X",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX X   G  X XX XXXXXX",
            "          X G    X          ",
            "XXXXXX XX X   G  X XX XXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

        self.numpy_maze = []
        self.cookie_spaces = []
        self.powerup_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            "images/ghost.png",
            "images/ghost_pink.png",
            "images/ghost_orange.png",
            "images/ghost_blue.png",
        ]
        self.size = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.numpy_maze)

    def request_new_random_path(self, in_ghost: Ghost):
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.get_position())

        path = self.p.get_path(
            current_maze_coord[1],
            current_maze_coord[0],
            random_space[1],
            random_space[0],
        )
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(test_path)

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "G":
                    self.ghost_spawns.append((y, x))

                if column == "X":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
                    if column == "O":
                        self.powerup_spaces.append((y, x))

            self.numpy_maze.append(binary_row)
