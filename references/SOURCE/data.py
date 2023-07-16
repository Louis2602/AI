import os

"""
The function get maze will return a 2D array, maze size (m x n) and pos of pacman (x, y)
This is a coordinate and each element hold a value, present it is empty (0), wall (1), monster (3) or food (@)
Ex maze:
    0 0 1 0
    0 0 1 2
    0 0 3 0
    0 0 0 0
--> maze[2][2] will be 3
"""
def string_to_number(str):
    return [int(i) for i in str] 

def get_maze(filename):
    f = open(filename, 'r')
    maze, pos, size = [],[],[]
    size = f.readline()
    temp = f.readlines()
    for index in range(len(temp)):
        maze.append(string_to_number(temp[index].split()))
    pos = maze.pop(-1)
    size = string_to_number(size.split())
    return maze, size, pos
