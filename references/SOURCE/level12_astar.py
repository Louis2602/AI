from utils import get_maze


def solution(trace, v, start):
    path_list = []
    while trace[v[0]][v[1]] != -1:
        path_list.append(v)
        v = trace[v[0]][v[1]]
    path_list.append(start)
    path_list.reverse()
    return path_list


def find_1_Food(Map):
    for index_i, i in enumerate(Map):
        for index_j, j in enumerate(i):
            if j == 2:
                return (index_i, index_j)
    # try except return none


def Manhattan(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def findValue(l, v):
    for index, i in enumerate(l):
        if i[1] == v:
            return index
    return -1


def AddNode(v, x):
    # 0 hang-1,cot
    # 1 hang,cot-1
    # 2 hang+1,cot
    # 3 hang,cot+1
    if x == 0:
        return (v[0] - 1, v[1])
    elif x == 1:
        return (v[0], v[1] - 1)
    elif x == 2:
        return (v[0] + 1, v[1])
    elif x == 3:
        return (v[0], v[1] + 1)
    else:
        return -1


def A_star(path):
    Mapdata = get_maze(path)  # "../INPUT/map1_lv2.txt"
    PacmanPos = Mapdata[2]
    MapLen = Mapdata[1]
    Map = Mapdata[0]
    Food_Pos = find_1_Food(Map)

    start = tuple(PacmanPos)
    goal = tuple(Food_Pos)
    frontier = [(Manhattan(start, goal), start)]
    explored = []
    trace = []
    for i in range(MapLen[0]):
        temp = [-1] * MapLen[1]
        trace.append(temp)

    while len(frontier) > 0:
        frontier = sorted(frontier, key=lambda element: (element[0]))
        u = frontier.pop(0)
        u_Fcost = u[0]
        u_node = u[1]
        explored.append(u_node)
        if u_node == goal:
            return solution(trace, u_node, start)
        path_cost = u_Fcost - Manhattan(u_node, goal)
        check = False
        for v in range(4):
            # hang-1,cot
            if (u_node[0] > 0) and (v == 0):
                temp = AddNode(u_node, v)
                check = True
            # hang,cot-1
            if (u_node[1] > 0) and (v == 1):
                temp = AddNode(u_node, v)
                check = True
            # hang+1,cot
            if (u_node[0] < MapLen[0] - 1) and (v == 2):
                temp = AddNode(u_node, v)
                check = True
            # hang,cot+1
            if (u_node[1] < MapLen[1] - 1) and (v == 3):
                temp = AddNode(u_node, v)
                check = True
            if (
                (check)
                and (Map[temp[0]][temp[1]] != 1)
                and (Map[temp[0]][temp[1]] != 3)
            ):
                pos_frontier = findValue(frontier, temp)
                if (temp not in explored) and (pos_frontier == -1):
                    trace[temp[0]][temp[1]] = (u_node[0], u_node[1])
                    frontier.append((path_cost + 1 + Manhattan(temp, goal), temp))
                elif pos_frontier != -1:
                    if frontier[pos_frontier][0] > path_cost + 1 + Manhattan(
                        temp, goal
                    ):
                        trace[temp[0]][temp[1]] = (u_node[0], u_node[1])
                        frontier[pos_frontier] = (
                            path_cost + 1 + Manhattan(temp, goal),
                            temp,
                        )
    return False


def A_star_run(path):
    # Level 2 - 1 food and monsters
    return A_star(path)
