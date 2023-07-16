import random

monster_init_pos = [] 
monster_cur_pos = []
monster_possible_pos = []
monster_over_food = []

def get_monster_init_pos(maze, size):
    for i in range(size[0]):
        for j in range(size[1]):
            if maze[i][j] == 3:
                monster_init_pos.append((i, j))
                monster_over_food.append(0)

def monster_possible_move(maze, size):
    a_monster_move = []
    for monster in monster_init_pos:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if monster[0] + i >= 0 and monster[0] + i < size[0] and monster[1] + j >= 0 and  monster[1] + j < size[1]:
                    if maze[monster[0] + i][monster[1] + j] == 0 or maze[monster[0] + i][monster[1] + j] == 2:
                        a_monster_move.append((monster[0] + i, monster[1] + j))
        monster_possible_pos.append(a_monster_move)
        a_monster_move = []

def possible_choice(maze, monster_number, direction):
    if direction == "up":
        pos = (monster_cur_pos[monster_number][0] + 1, monster_cur_pos[monster_number][1])
        if pos in monster_possible_pos[monster_number] and maze[pos[0]][pos[1]] != 3:
            return pos
        else:
            return "up"
    elif direction == "down":
        pos = (monster_cur_pos[monster_number][0] - 1, monster_cur_pos[monster_number][1])
        if pos in monster_possible_pos[monster_number] and maze[pos[0]][pos[1]] != 3:
            return pos
        else:
            return "down"
    elif direction == "left":
        pos = (monster_cur_pos[monster_number][0], monster_cur_pos[monster_number][1] - 1)
        if pos in monster_possible_pos[monster_number] and maze[pos[0]][pos[1]] != 3:
            return pos
        else:
            return "left"
    elif direction == "right":
        pos = (monster_cur_pos[monster_number][0], monster_cur_pos[monster_number][1] + 1)
        if pos in monster_possible_pos[monster_number] and maze[pos[0]][pos[1]] != 3:
            return pos
        else:
            return "right"

monster_cur_pos = monster_init_pos
def init_monster(maze, size):
    get_monster_init_pos(maze, size)
    monster_possible_move(maze, size)
    
    monster_path = []
    for i in range(len(monster_init_pos)):
        monster_path.append([monster_init_pos[i]])
    return monster_path

def monster_move(maze, monster_path):
    for monster_number in range(len(monster_init_pos)):
        available_direction = ["up", "down", "left", "right"]
        while len(available_direction) > 0:
            direction = random.choice(available_direction)
            pos = possible_choice(maze, monster_number, direction)
            if isinstance(pos, tuple):
                monster_path[monster_number].append(pos)

                if monster_over_food[monster_number] == 1:
                    maze[monster_cur_pos[monster_number][0]][monster_cur_pos[monster_number][1]] = 2
                else:
                    maze[monster_cur_pos[monster_number][0]][monster_cur_pos[monster_number][1]] = 0

                if maze[pos[0]][pos[1]] == 2:
                    monster_over_food[monster_number] = 1
                else:
                    monster_over_food[monster_number] = 0

                maze[pos[0]][pos[1]] = 3
                    
                monster_cur_pos[monster_number] = pos
                break
            else:
                available_direction.pop(available_direction.index(pos))
        if len(available_direction) == 0:
            monster_path[monster_number].append(monster_cur_pos[monster_number])
    
    return monster_path, maze
