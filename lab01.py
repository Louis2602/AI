from queue import PriorityQueue, Queue
import numpy as np


def readGraphFromFile(filename):
    with open(filename, 'r') as file:
        size = int(file.readline().strip())
        start, goal = map(
            int, file.readline().strip().split())
        graph = {}
        for _ in range(size):
            line = file.readline().strip().split(':')
            vertex, neighbors = int(line[0]), line[1].strip()[
                1:-1].split('), ')
            weighted_neighbors = []
            for neighbor in neighbors:
                neighbor = neighbor.strip('()').split(', ')
                weighted_neighbors.append(
                    (int(neighbor[0]), int(neighbor[1])))
            graph[vertex] = weighted_neighbors

    return graph, size, start, goal


def get_path(parents, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.append(current_node)
        current_node = parents[current_node]

    path.append(start)
    path.reverse()
    return path


def bfs(graph, start, goal):
    # Implement using queue
    frontier = Queue()
    visited = []
    visited.append(start)
    frontier.put(start)
    parents = {}

    while frontier:
        current_node = frontier.get()
        print("Frontier: ", frontier)
        print("Visited: ", visited)

        if current_node == goal:
            return get_path(parents, start, goal)

        for neighbor in graph[current_node]:
            if neighbor[0] not in visited:
                visited.append(neighbor[0])
                frontier.append(neighbor[0])
                parents[neighbor[0]] = current_node


def dfs(graph, start, goal, visited=None):
    # Implement using stack
    if visited is None:
        visited = []
    visited.append(start)
    print(start, end=" ")
    if start == goal:
        return
    for neighbor in graph[start]:
        if neighbor[0] not in visited:
            dfs(graph,  neighbor[0], goal, visited)


def ucs(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))  # (priority, node)
    visited = []
    parents = {}

    while frontier:
        ucs_w, current_node = frontier.get()
        visited.append(current_node)

        if current_node == goal:
            return get_path(parents, start, goal)

        for neighbor in graph[current_node]:
            if neighbor[0] not in visited:
                frontier.put((
                    ucs_w + neighbor[1],
                    neighbor[0]
                ))
                parents[neighbor[0]] = current_node


def a_star():
    # using the Manhattan distance as heuristic
    pass


def greedy_best_first_search():
    # using the Manhattan distance as heuristic
    pass


if __name__ == "__main__":
    graph, size, start, goal = readGraphFromFile('maze.txt')
    print("Graph:")
    for vertex, neighbors in graph.items():
        print(vertex, ":", neighbors)
    print(f'Go from vertex: {start} to vertex {goal}')
    print("BFS: ", end="")
    print(bfs(graph, start, goal))
    print("DFS: ", end="")
    dfs(graph, start, goal)
    print("\nUCS: ", end="")
    print(ucs(graph, start, goal))
