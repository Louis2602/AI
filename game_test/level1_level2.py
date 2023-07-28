def heuristic(node, goal):
    # Euclidean distance heuristic
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5


def get_neighbors(pos, maze):
    neighbors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if (
            0 <= x < len(maze)
            and 0 <= y < len(maze[0])
            and (maze[x][y] == 0 or maze[x][y] == 2)
        ):
            neighbors.append((x, y))

    return neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def find_food(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                return (i, j)


def solve(maze, start):
    start_node = tuple(start)
    goal_node = tuple(find_food(maze))

    queue = [(0, start_node, 0)]  # Using a queue: (total_cost, current_node, score)
    visited = set()
    came_from = {}

    while queue:
        _, current_node, score = queue.pop(0)

        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in get_neighbors(current_node, maze):
                if neighbor not in visited:
                    total_cost = 1 + heuristic(neighbor, goal_node)
                    came_from[neighbor] = current_node
                    queue.append((total_cost, neighbor, score - 1))
        queue.sort(
            key=lambda x: x[2], reverse=True
        )  # Sort in descending order based on score

    return []


def handleLevel1_2(maze, start):
    return solve(maze, start)
