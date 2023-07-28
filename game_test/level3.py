import random

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
    res = []

    while queue:
        distance, current_node, score = queue.pop(0)
        res.append(current_node)

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

    return res 


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


def changePath(maze, pacmanPos, ghosts, mazePacman):
    moveablePos = get_neighbors(pacmanPos, mazePacman)
    for pos in moveablePos:
        if check_safe_move(pos, ghosts) == True:
            pacmanPos = pos
            break
    return pacmanPos


def ghostMove(maze, pacmanPos, ghosts, mazePacman):
    ghostsPos = []
    for ghost in ghosts:
        move = random.choice(get_ghost_neighbors(ghost, maze))
        #print("move", move)
        maze[move[0]][move[1]] = 3
        maze[ghost[0]][ghost[1]] = 0
        ghostsPos.append(move)
    return maze, ghostsPos, mazePacman        
    # for ghost in ghosts:
    #     ghostPath = ghostAstart(maze, ghost, pacmanPos)
    #     if (len(ghostPath) > 1): 
    #         maze[ghostPath[0][0]][ghostPath[0][1]] = 0
    #         maze[ghostPath[1][0]][ghostPath[1][1]] = 3
    #         mazePacman[ghostPath[0][0]][ghostPath[0][1]] = 0
    #         mazePacman[ghostPath[1][0]][ghostPath[1][1]] = 3
    #         ghostsPos.append(ghostPath[1])
    #     else:
    #         ghostsPos.append(ghostPath[0])
    # return maze, ghostsPos, mazePacman
    


def eatFood(maze, pacmanPos, foods, countFood, mazePacman):
    if pacmanPos in foods:
        foods.pop(foods.index(pacmanPos))
        maze[pacmanPos[0]][pacmanPos[1]] = 0
        mazePacman[pacmanPos[0]][pacmanPos[1]] = 0
        countFood = countFood - 1
    return maze, foods, mazePacman, countFood

def changeGoal(maze, pacmanPos, foods, ghosts, invisibility, mazePacman):
    foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    invisibility1 = [coord for coord in invisibility if mazePacman[coord[0]][coord[1]] == 4]
    invisibility1 = sorted(invisibility1, key=lambda inv: heuristic(pacmanPos, inv))
    if foods:
        res = foods[0]
    else:
        res = invisibility1[0]
    return res

def initMazePacmanView(maze):
    rows = len(maze)
    cols = len(maze[0])

    # Khởi tạo mảng  2 chiều mới với kích thước và giá trị như yêu cầu
    mazePacman = [[4 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                mazePacman[i][j] = 1
    return mazePacman

def updateMazePacman(maze, mazePacman, pacmanPos):
    rows = len(maze)
    cols = len(maze[0])

    for i in range(rows):
        for j in range(cols):
            if abs(i - pacmanPos[0]) + abs(j - pacmanPos[1]) <= 3:
                mazePacman[i][j] = maze[i][j]
    return mazePacman

def handleAStar(maze, start, goal, foods, ghosts, countFood, invisibility, mazePacman):
    pacmanPos = start
    pathSolution = [pacmanPos]
    ghostsPath = [ghosts]
    while True:
        foods = find_object(mazePacman, 2)
        print("pacmanPos: ", pacmanPos)
        #print("mazePacman: ", mazePacman)
        print(countFood)
        if (countFood == 0):
            break
        if pacmanPos == goal:
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman)
            if (countFood == 0):
                break

        goal = changeGoal(maze, pacmanPos, foods, ghosts, invisibility, mazePacman)
        print("goal1", goal)
        print("food", foods)
        pacmanPath = astar(maze, pacmanPos, goal)
        print(pacmanPath)
        if (len(pacmanPath) == 1):
            
            maze, ghosts, mazePacman = ghostMove(maze, pacmanPos, ghosts, mazePacman)
            ghostsPath.append(ghosts)
            pacmanPos = pacmanPath[0]
            mazePacman = updateMazePacman(maze, mazePacman, pacmanPos)
            pathSolution.append(pacmanPos)
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman)
        else:
            pacmanPos = pacmanPath.pop(0)
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman)
            newPacmanPos = pacmanPath[0]
            moveablePos = get_neighbors(pacmanPos, maze)
            if (newPacmanPos in moveablePos) and (check_safe_move(newPacmanPos, ghosts)):
                maze, ghosts, mazePacman = ghostMove(maze, pacmanPos, ghosts, mazePacman)
                ghostsPath.append(ghosts)
                pacmanPos = newPacmanPos
                mazePacman = updateMazePacman(maze, mazePacman, pacmanPos)
                pathSolution.append(pacmanPos)
            else:
                maze, ghosts, mazePacman = ghostMove(maze, pacmanPos, ghosts, mazePacman)
                ghostsPath.append(ghosts)
                pacmanPos = changePath(maze, pacmanPos, ghosts, mazePacman)
                mazePacman = updateMazePacman(maze, mazePacman, pacmanPos)
                maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman)
                pathSolution.append(pacmanPos)
                if (pacmanPos in ghosts):
                    return maze, pathSolution, foods, ghosts, ghostsPath, "dead", countFood, mazePacman

    return maze, pathSolution, foods, ghosts, ghostsPath, "alive", countFood, mazePacman



def handleMainLv3(maze, start):
   
    mazePacman = initMazePacmanView(maze)
    pacmanPos = tuple(start)
    pacmanRes = [start]
    mazePacman = updateMazePacman(maze, mazePacman, pacmanPos)

    ghosts = find_object(maze, 3)
    ghostsRes = [ghosts]
    
    foods = find_object(maze, 2)
    countFood = len(foods)

    invisibility = find_object(mazePacman, 4)
    foods = find_object(mazePacman, 2)
    
    while countFood:
        foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
        invisibility = sorted(invisibility, key=lambda inv: heuristic(pacmanPos, inv))
        
        if foods:
            value = foods[0]
        else:
            value = invisibility[0]

        maze, pacmanPath, foods, ghosts, ghostsPath, status, countFood, mazePacman = handleAStar(
            maze, pacmanPos, value, foods, ghosts, countFood, invisibility, mazePacman
        )
        print(1)
        pacmanPos = pacmanPath[len(pacmanPath) - 1]
        pacmanRes += pacmanPath[1:]
        ghostsRes += ghostsPath[1:]
        if status == "dead":
            break
    
    print("PACMAN", pacmanRes)
    print("GHOSTS", ghostsRes)
    
    return pacmanRes, ghostsRes