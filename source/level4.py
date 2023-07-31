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
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != 1:
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

    return reconstruct_path(came_from, current_node)


def ghostAstart(maze, start, goal):
    queue = [(0, start, 0)]  # Using a queue: (total_cost, current_node, score)
    visited = set()
    came_from = {}
    res = []

    while queue:
        distance, current_node, score = queue.pop(0)
        res.append(current_node)

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

    return res


def changePath(maze, pacmanPos, ghosts):
    moveablePos = get_neighbors(pacmanPos, maze)
    for pos in moveablePos:
        if check_safe_move(pos, ghosts) == True:
            pacmanPos = pos
            break
    return pacmanPos


def ghostMove(maze, pacmanPos, ghosts):
    ghostsPos = []
    for ghost in ghosts:
        ghostPath = ghostAstart(maze, ghost, pacmanPos)
        if len(ghostPath) > 1:
            maze[ghostPath[0][0]][ghostPath[0][1]] = 0
            maze[ghostPath[1][0]][ghostPath[1][1]] = 3
            ghostsPos.append(ghostPath[1])
        else:
            ghostsPos.append(ghostPath[0])
    return maze, ghostsPos


def eatFood(maze, pacmanPos, foods):
    if pacmanPos in foods:
        foods.pop(foods.index(pacmanPos))
        maze[pacmanPos[0]][pacmanPos[1]] = 0
    return maze, foods


def changeGoal(maze, pacmanPos, foods, ghosts):
    foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    res = foods[0]

    for food in foods:
        path = astar(maze, pacmanPos, food)
        if path[len(path) - 1] == food:
            res = food
            break
    return res


def is_blocked(maze, pacmanPos):
    stack = [pacmanPos]
    visited = set()

    while stack:
        x, y = stack.pop()
        visited.add((x, y))

        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for nx, ny in neighbors:
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 1 and (nx, ny) not in visited:
                stack.append((nx, ny))


    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (maze[i][j] == 2 and (i, j) in visited):
                return False

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 0 and (i, j) not in visited:
                return True

    return False



def handleAStar(maze, start, goal, foods, ghosts):
    pacmanPos = start
    pathSolution = [pacmanPos]
    ghostsPath = [ghosts]
    while True:
        if len(foods) == 0:
            break
        if pacmanPos == goal:
            maze, foods = eatFood(maze, pacmanPos, foods)
            if len(foods) == 0:
                break
            if (is_blocked(maze, pacmanPos) == True):
                return maze, pathSolution, foods, ghosts, ghostsPath, "blocked"
                # break

        goal = changeGoal(maze, pacmanPos, foods, ghosts)
        pacmanPath = astar(maze, pacmanPos, goal)

        if len(pacmanPath) == 1:
            maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
            ghostsPath.append(ghosts)
            pacmanPos = pacmanPath[0]
            pathSolution.append(pacmanPos)
            maze, foods = eatFood(maze, pacmanPos, foods)
        else:
            pacmanPos = pacmanPath.pop(0)
            maze, foods = eatFood(maze, pacmanPos, foods)
            newPacmanPos = pacmanPath[0]
            moveablePos = get_neighbors(pacmanPos, maze)
            if (newPacmanPos in moveablePos) and (
                check_safe_move(newPacmanPos, ghosts)
            ):
                maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
                ghostsPath.append(ghosts)
                pacmanPos = newPacmanPos
                pathSolution.append(pacmanPos)
            else:
                maze, ghosts = ghostMove(maze, pacmanPos, ghosts)
                ghostsPath.append(ghosts)
                pacmanPos = changePath(maze, pacmanPos, ghosts)
                maze, foods = eatFood(maze, pacmanPos, foods)
                pathSolution.append(pacmanPos)
                if pacmanPos in ghosts:
                    return maze, pathSolution, foods, ghosts, ghostsPath, "dead"

    return maze, pathSolution, foods, ghosts, ghostsPath, "alive"


def handleMainLv4(maze, start):
    ghosts = find_object(maze, 3)
    foods = find_object(maze, 2)
    pacmanPos = tuple(start)
    pacmanRes = [start]
    ghostsRes = [ghosts]

    

    # while foods:
    #     foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    #     maze, pacmanPath, foods, ghosts, ghostsPath, status = handleAStar(
    #         maze, pacmanPos, foods[0], foods, ghosts
    #     )
    #     pacmanPos = pacmanPath[len(pacmanPath) - 1]
    #     pacmanRes += pacmanPath[1:]
    #     ghostsRes += ghostsPath[1:]
    #     if status == "dead":
    #         break

    foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    maze, pacmanPath, foods, ghosts, ghostsPath, status = handleAStar(maze, pacmanPos, foods[0], foods, ghosts)
    pacmanPos = pacmanPath[len(pacmanPath) - 1]
    pacmanRes += pacmanPath[1:]
    ghostsRes += ghostsPath[1:]

    print("PACMAN", pacmanRes)
    print("GHOSTS", ghostsRes)

    return pacmanRes, ghostsRes, status
