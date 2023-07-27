import tkinter as tk
import time
import level1

def get_maze_name():
    level = input("Choose game level (1-4): ")
    map = input("Choose map (1-5): ")
    maze_name = f"level{level}_map{map}.txt"
    return maze_name, int(level)

if __name__ == '__main__':
    maze_name, level = get_maze_name()
    if level == 1:
        level1.Solve(maze_name)
    