import timeit
from utils import get_path
import numpy as np
import os


def dfs(
    adj_list, start, current_node, goal, explored=None, parents=None, timerStart=None
):
    if explored is None and parents is None:
        explored = []
        parents = {}
        path = []
        timerStart = timeit.default_timer()
    explored.append(current_node)
    # print(current_node, end=" ")
    if current_node == goal:
        path = get_path(parents, start, goal)
        timerStop = timeit.default_timer()
        elapsed_time = timerStop - timerStart

        dir_path = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(dir_path)
        np.savetxt(f"{parent_dir}./Output/output_dfs.txt", path, fmt="%d", newline=" ")

        return path, explored, elapsed_time
    for neighbor in adj_list[current_node]:
        if neighbor not in explored:
            parents[neighbor] = current_node
            result = dfs(adj_list, start, neighbor, goal, explored, parents, timerStart)
            if result is not None:
                return result
