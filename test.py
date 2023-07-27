def heuristic(node, goal):
    # Euclidean distance heuristic
    return ((node[0] - goal[0])**2 + (node[1] - goal[1])**2)**0.5

def get_neighbors(pos, maze):
    neighbors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0:
            neighbors.append((x, y))

    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))

def astar(maze, size, start, goal):
    n, m = size
    start_node = tuple(start)
    goal_node = tuple(goal)

    stack = [(start_node, 0)]  # Using stack: (current_node, g_score)

    g_score = {start_node: 0}
    came_from = {}

    while stack:
        current, g = stack.pop()

        if current == goal_node:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, maze):
            tentative_g_score = g + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                stack.append((neighbor, tentative_g_score))

    return None

# Example usage:
maze = [
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0]
]

size = (5, 5)
start_pos = [0, 0]
goal_pos = [4, 4]

path = astar(maze, size, start_pos, goal_pos)
print(path)
