from astar import astar
from level4 import handleMainLv4


class PathFinder:
    def __init__(self, maze, pacman_pos):
        self.maze = maze
        self.start = pacman_pos

    def get_path_a_star(self, start, goal) -> object:
        res = astar(self.maze, start, goal)
        # return [(sub[1], sub[0]) for sub in res]
        return res

    def get_path_lv4(self):
        pacman_path, ghost_path = handleMainLv4(self.maze, self.start)

        return pacman_path, ghost_path
