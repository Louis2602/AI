from queue import Queue
import timeit
from utils import get_path
import numpy as np
import os


def bfs(adj_list, start, goal):
    timerStart = timeit.default_timer()
    # Implement using queue
    frontier = Queue()
    explored = []
    explored.append(start)
    frontier.put(start)
    parents = {}
    path = []

    while frontier.empty() == False:
        current_node = frontier.get()
        explored.append(current_node)

        if current_node == goal:
            path = get_path(parents, start, goal)
            break

        for neighbor in adj_list[current_node]:
            if neighbor not in explored:
                frontier.put(neighbor)
                parents[neighbor] = current_node
    timerStop = timeit.default_timer()
    elapsed_time = timerStop - timerStart

    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(dir_path)
    np.savetxt(f"{parent_dir}./Output/output_bfs.txt", path, fmt="%d", newline=" ")

    return path, explored, elapsed_time
