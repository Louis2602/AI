from queue import PriorityQueue
import timeit
from utils import calc_heuristics, get_path
import numpy as np
import os


def a_star(adj_list, start, goal, size):
    # using the Manhattan distance as heuristic
    timerStart = timeit.default_timer()
    frontier = PriorityQueue()
    heuristics = calc_heuristics(adj_list, goal, size)
    frontier.put((0, start))  # (priority, node)
    explored = []
    explored_with_cost = []
    parents = {}
    path = []
    gn = {start: 0}  # gn at goal

    while frontier.empty() == False:
        fn, current_node = frontier.get()
        explored.append(current_node)
        explored_with_cost.append({"node": current_node, "fn": fn})
        if current_node == goal:
            path = get_path(parents, start, goal)
            break
        for neighbor in adj_list[current_node]:
            cur_dist = gn[current_node] + 1
            if neighbor not in gn or cur_dist < gn[neighbor]:
                gn[neighbor] = cur_dist
                # f(n) = g(n) + h(n)
                fn = heuristics[neighbor] + cur_dist
                frontier.put((fn, neighbor))
                parents[neighbor] = current_node

    timerStop = timeit.default_timer()
    elapsed_time = timerStop - timerStart

    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(dir_path)
    np.savetxt(f"{parent_dir}./Output/output_a_star.txt", path, fmt="%d", newline=" ")
    return path, explored, explored_with_cost, elapsed_time
