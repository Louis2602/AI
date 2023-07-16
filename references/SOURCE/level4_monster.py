import level3_monster
import random
import data

monster_init_pos = []
monster_cur_pos = []
monster_path = []
monster_random_number = []
monster_temp_path = []
monster_overlap = []

def init_monster(maze, size):
    for i in range(size[0]):
        for j in range(size[1]):
            if maze[i][j] == 3:
                monster_init_pos.append((i, j))
                monster_cur_pos.append((i, j))
    for i in range(len(monster_init_pos)):
        monster_path.append([monster_init_pos[i]])
        monster_random_number.append(random.choice([3, 4, 5]))
        monster_temp_path.append([])
        monster_overlap.append(0)

    print(monster_random_number)
    return monster_path

def solution(trace,v,start):
    path_list=[]
    while(trace[v[0]][v[1]]!=-1):
        path_list.append(v)
        v=trace[v[0]][v[1]]
    path_list.append(start)
    path_list.reverse()
    return path_list



def Manhattan(u,v):
    return abs(u[0]-v[0])+abs(u[1]-v[1])


def AddNode(v,x):
    #0 hang-1,cot
    #1 hang,cot-1
    #2 hang+1,cot
    #3 hang,cot+1
    if x==0:
        return (v[0]-1, v[1])
    elif x==1: 
        return (v[0], v[1]-1)
    elif x==2: 
        return (v[0]+1, v[1])
    elif x==3: 
        return (v[0],v[1]+1)
    else: return -1

def findValue(l,v):
    for index,i in enumerate(l):
        if i[1] == v:
            return index
    return -1


def smart_monster(maze, pacman_pos, index, size):
    start = monster_cur_pos[index]
    temp = (pacman_pos[0], pacman_pos[1])
    goal = temp
    frontier=[(Manhattan(start,goal),start)]
    explored=[]
    trace=[]
    for i in range(size[0]):
        temp=[-1]*size[1]
        trace.append(temp)
            
    while(len(frontier)>0):
        frontier=sorted(frontier, key=lambda element: (element[0], element[1]))
        u=frontier.pop(0)
        u_Fcost=u[0]
        u_node=u[1]
        explored.append(u_node)
        if u_node==goal:
            return solution(trace,u_node,start)
        path_cost=u_Fcost-Manhattan(u_node,goal)
        check=False
        for v in range(4):
            #hang-1,cot
            if (u_node[0]>0) and (v==0):
                temp=AddNode(u_node,v)
                check=True
            #hang,cot-1
            if (u_node[1]>0) and (v==1):
                temp=AddNode(u_node,v)
                check=True
            #hang+1,cot
            if (u_node[0]<size[0]-1) and (v==2):
                temp=AddNode(u_node,v)
                check=True
            #hang,cot+1
            if (u_node[1]<size[1]-1) and (v==3):
                temp=AddNode(u_node,v)
                check=True
            if (check) and (maze[temp[0]][temp[1]]!=1):
                pos_frontier = findValue(frontier,temp)
                if (temp not in explored) and (pos_frontier == -1):
                    trace[temp[0]][temp[1]]=(u_node[0],u_node[1])
                    frontier.append((path_cost+1+Manhattan(temp,goal),temp))
                elif pos_frontier != -1:
                    if frontier[pos_frontier][0]> path_cost+1+Manhattan(temp,goal):
                        trace[temp[0]][temp[1]]=(u_node[0],u_node[1])
                        frontier[pos_frontier]=(path_cost+1+Manhattan(temp,goal),temp)
    return [monster_cur_pos[index]]

def A_star_monster(maze, pacman_pos,index, size):
    return smart_monster(maze, pacman_pos, index, size)


def monster_move(maze,pacman_pos,size):
    for i in range(len(monster_init_pos)):
        if not monster_temp_path[i]: 
            path = A_star_monster(maze, pacman_pos, i, size)
            if len(path) - 1 >= monster_random_number[i]:
                for j in range(1, monster_random_number[i] + 1):
                    monster_temp_path[i].append(path[j])
            else:
                for j in range(1, len(path)):
                    monster_temp_path[i].append(path[j])
                for j in range(monster_random_number[i] - len(path) - 1):
                    monster_temp_path[i].append(path[j])
                    
        monster_path[i].append(monster_temp_path[i][0])
        monster_cur_pos[i] = monster_temp_path[i][0]
        monster_temp_path[i].pop(0)

        if monster_overlap[i] == 0:
            maze[monster_path[i][-2][0]][monster_path[i][-2][1]] = 0 #vi tri truoc do la 0
        elif monster_overlap[i] == 2:
            maze[monster_path[i][-2][0]][monster_path[i][-2][1]] = 2 #vi tri truoc do la 0

        if maze[monster_cur_pos[i][0]][monster_cur_pos[i][1]] == 0:
            monster_overlap[i] = 0
        elif maze[monster_cur_pos[i][0]][monster_cur_pos[i][1]] == 2:
            monster_overlap[i] = 2 
        elif maze[monster_cur_pos[i][0]][monster_cur_pos[i][1]] == 3:
            monster_overlap[i] = 3
        maze[monster_cur_pos[i][0]][monster_cur_pos[i][1]] = 3

    return monster_path, maze

