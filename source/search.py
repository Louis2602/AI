from level1_level2 import handleLevel1_2
from level4 import handleMainLv4
from level3 import handleMainLv3


class PathFinder:
    def __init__(self, maze, pacman_pos):
        self.maze = maze
        self.start = pacman_pos

    def get_path_lv1_lv2(self) -> object:
        res = handleLevel1_2(self.maze, self.start)
        return res

    def get_path_lv3(self):
        pacman_path, ghost_path = handleMainLv3(self.maze, self.start)
        return pacman_path, ghost_path, status

    def get_path_lv4(self):
        pacman_path, ghost_path, status = handleMainLv4(self.maze, self.start)

        return pacman_path, ghost_path, status
