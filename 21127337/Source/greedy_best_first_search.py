from queue import PriorityQueue
import timeit
from utils import calc_heuristics, get_path
import numpy as np
import os


def greedy_best_first_search(adj_list, start, goal, size):
    timerStart = timeit.default_timer()
    # using the Manhattan distance as heuristic
    frontier = PriorityQueue()
    heuristics = calc_heuristics(adj_list, goal, size)
    frontier.put((heuristics[start], start))  # (priority, node)
    explored = []
    explored_with_cost = []
    parents = {}
    path = []

    while frontier.empty() == False:
        hn, current_node = frontier.get()
        explored.append(current_node)
        explored_with_cost.append({"node": current_node, "hn": hn})

        if current_node == goal:
            path = get_path(parents, start, goal)
            break
        for neighbor in adj_list[current_node]:
            if neighbor not in explored:
                frontier.put((heuristics[neighbor], neighbor))
                parents[neighbor] = current_node
    timerStop = timeit.default_timer()
    elapsed_time = timerStop - timerStart

    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(dir_path)
    np.savetxt(f"{parent_dir}./Output/output_gbfs.txt", path, fmt="%d", newline=" ")
    return path, explored, explored_with_cost, elapsed_time
