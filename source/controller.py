from search import PathFinder
from utils import get_maze


class PacmanGameController:
    def __init__(self, maze_name):
        self.maze, self.size, self.pacman_pos = get_maze(maze_name)

        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            "images/ghost.png",
            "images/ghost_pink.png",
            "images/ghost_orange.png",
            "images/ghost_blue.png",
        ]
        self.read_maze()
        self.search = PathFinder(self.maze, self.pacman_pos)

    def read_maze(self):
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                if self.maze[row][column] == 0:
                    self.reachable_spaces.append((row, column))
                if self.maze[row][column] == 2:
                    self.cookie_spaces.append((row, column))
                    self.reachable_spaces.append((row, column))
                if self.maze[row][column] == 3:
                    self.ghost_spawns.append((row, column))
