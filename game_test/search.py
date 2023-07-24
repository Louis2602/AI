from astar import astar


class Pathfinder:
    def __init__(self, maze):
        self.maze = maze

    def get_path_a_star(self, start, goal) -> object:
        res = astar(self.maze, start, goal)
        # return [(sub[1], sub[0]) for sub in res]
        return res
