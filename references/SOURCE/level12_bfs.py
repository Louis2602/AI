from utils import get_maze
import collections


def food_pos(Map):
    for index_i, i in enumerate(Map):
        for index_j, j in enumerate(i):
            if j == 2:
                return [index_i, index_j]  # vị trí thức ăn


def path_G(Map):
    temp = []
    for i in range(len(Map)):
        for j in range(len(Map[i])):
            if Map[i][j] == 0 or Map[i][j] == 2:
                temp.append((i, j))
    # print(temp)
    list = {}
    temp2 = []
    for i in range(len(temp)):
        for j in range(len(temp)):
            if (
                (temp[i][0] + 1 == temp[j][0] and temp[i][1] == temp[j][1])
                or (temp[i][1] + 1 == temp[j][1] and temp[i][0] == temp[j][0])
                or (temp[i][0] - 1 == temp[j][0] and temp[i][1] == temp[j][1])
                or (temp[i][1] - 1 == temp[j][1] and temp[i][0] == temp[j][0])
            ):
                # print(temp[i])
                # print(temp[j])
                temp2.append(temp[j])

        list[tuple(temp[i])] = temp2
        temp2 = []

    return list


def BFS(path):  # path= link dan
    Map, _, Pacman_pos = get_maze(path)
    Food_pos = food_pos(Map)

    graph = path_G(Map)
    start = tuple(Pacman_pos)  # list
    goal = tuple(Food_pos)  # list

    if start == goal:
        return [start]
    visited = {start}
    queue = collections.deque([(start, ())])

    Time = 0
    while queue:
        current, path = queue.popleft()

        visited.add(current)

        Time = Time + 1
        for neighbor in graph[current]:
            if neighbor == goal:
                a = []
                for i in range(0, len(path), 2):
                    a.append((path[i], path[i + 1]))
                a.append(current)
                a.append(neighbor)
                kq = a
                return kq

            if neighbor in visited:
                continue
            queue.append((neighbor, path + current))  # sai dday
            visited.add(neighbor)

    return False
