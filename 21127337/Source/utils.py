def readMazeFromFile(filename):
    with open(filename, "r") as file:
        size = int(file.readline().strip())
        start, goal = map(int, file.readline().strip().split())
        adj_list = {}
        for _ in range(size * size):
            node, neighbors = file.readline().strip().split(":")
            node = int(node)
            neighbors = [
                int("".join(filter(str.isdigit, neighbor.strip())))
                for neighbor in neighbors.split(",")
                if neighbor.strip()
            ]
            adj_list[node] = neighbors

    return adj_list, size, start, goal


def get_path(parents, start, goal):
    path = []
    current_node = goal
    while current_node != start:
        path.append(current_node)
        current_node = parents[current_node]

    path.append(start)
    path.reverse()
    return path


def calc_heuristics(adj_list, goal, size):
    heuristics = {}
    goal_pos = (goal // size, goal % size)

    for node, _ in adj_list.items():
        current_node_pos = (node // size, node % size)
        heuristic = manhattan_distance(current_node_pos, goal_pos)
        heuristics[node] = heuristic

    return heuristics


def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
