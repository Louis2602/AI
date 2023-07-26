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


def get_ghost_neighbors(pos, maze):
    neighbors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and (maze[x][y] != 1):
            neighbors.append((x, y))

    return neighbors


def check_safe_move(pos, ghosts):
    for ghost in ghosts:
        if heuristic(pos, ghost) <= 1:
            return False
    return True


def getMoveablePos(maze, pos, ghosts):
    res = []
    neighbors = get_neighbors(pos, maze)
    for neighbor in neighbors:
        if check_safe_move(neighbor, ghosts):
            res.append(neighbor)
    return res


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def find_object(maze, entity):
    res = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == entity:
                res.append((i, j))
    return res


def CalcHeuristic(start, array):
    res = []
    for i in array:
        res.append(heuristic(start, i))
    return res


def astar(maze, start, goal):
    queue = [(0, start, 0)]  # Using a queue: (total_cost, current_node, score)
    visited = set()
    came_from = {}

    while queue:
        distance, current_node, score = queue.pop(0)

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in get_neighbors(current_node, maze):
                if neighbor not in visited:
                    total_cost = distance + 1 + heuristic(neighbor, goal)
                    came_from[neighbor] = current_node
                    queue.append((total_cost, neighbor, score - 1))
        queue.sort(key=lambda x: x[0], reverse=False)

    return False


def ghostAstart(maze, start, goal):
    queue = [(0, start, 0)]  # Using a queue: (total_cost, current_node, score)
    visited = set()
    came_from = {}

    while queue:
        distance, current_node, score = queue.pop(0)

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in get_ghost_neighbors(current_node, maze):
                if neighbor not in visited:
                    total_cost = distance + 1 + heuristic(neighbor, goal)
                    came_from[neighbor] = current_node
                    queue.append((total_cost, neighbor, score - 1))
        queue.sort(key=lambda x: x[0], reverse=False)

    return False


def changePath(maze, pacmanPos, ghosts):
    check = False
    moveablePos = get_neighbors(pacmanPos, maze)
    for pos in moveablePos:
        if check_safe_move(pos, ghosts) == True:
            check = True
            pacmanPos = pos
            break
    if check:
        return pacmanPos
    else:
        return -1


def ghostMove(maze, pacmanPos, ghosts):
    ghostsPos = []
    for ghost in ghosts:
        ghostPath = ghostAstart(maze, ghost, pacmanPos)
        maze[ghostPath[0][0]][ghostPath[0][1]] = 0
        maze[ghostPath[1][0]][ghostPath[1][1]] = 3
        ghostsPos.append(ghostPath[1])
    return maze, ghostsPos


def eatFood(maze, pacmanPos, foods):
    if pacmanPos in foods:
        foods.pop(foods.index(pacmanPos))
        maze[pacmanPos[0]][pacmanPos[1]] = 0
    return maze, foods


def handleAStar(maze, start, goal, foods, ghosts):
    pacmanPos = start
    pathSolution = [pacmanPos]
    ghostsPath = [ghosts]
    while pacmanPos != goal:
        pacmanPath = astar(maze, pacmanPos, goal)
        while pacmanPath == False:
            newPacmanPos = changePath(maze, pacmanPos, ghosts)
            if newPacmanPos == -1:
                return maze, pathSolution, foods, ghostsPath, "dead"

            maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
            ghostsPath.append(ghosts)
            pathSolution.append(newPacmanPos)
            pacmanPath = astar(maze, newPacmanPos, goal)
            pacmanPos = newPacmanPos
            maze, foods = eatFood(maze, pacmanPos, foods)

        pacmanPos = pacmanPath.pop(0)
        maze, foods = eatFood(maze, pacmanPos, foods)
        newPacmanPos = pacmanPath[0]
        moveablePos = get_neighbors(pacmanPos, maze)
        if (newPacmanPos in moveablePos) and (check_safe_move(newPacmanPos, ghosts)):
            maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
            ghostsPath.append(ghosts)
            pacmanPos = pacmanPath.pop(0)
            pathSolution.append(pacmanPos)
        else:
            newPacmanPos = changePath(maze, pacmanPos, ghosts)
            if newPacmanPos == -1:
                return maze, pathSolution, foods, ghostsPath, "dead"

            maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
            ghostsPath.append(ghosts)

            pathSolution.append(newPacmanPos)
            pacmanPos = newPacmanPos
            maze, foods = eatFood(maze, pacmanPos, foods)

        if pacmanPos == goal:
            maze, foods = eatFood(maze, pacmanPos, foods)

    return maze, pathSolution, foods, ghostsPath, "alive"


def handleMainLv4(maze, start):
    ghosts = find_object(maze, 3)
    foods = find_object(maze, 2)
    pacmanPos = tuple(start)
    pacmanRes = []
    ghostsRes = []

    while foods:
        foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
        maze, pacmanPath, foods, ghostsPath, status = handleAStar(
            maze, pacmanPos, foods[0], foods, ghosts
        )
        pacmanPos = pacmanPath[len(pacmanPath) - 1]
        pacmanRes += pacmanPath
        ghostsRes += ghostsPath
        if status == "dead":
            print("dead")
            break
    print("PAC", pacmanRes)
    print("GHO", ghostsRes)
    return pacmanRes, ghostsRes
