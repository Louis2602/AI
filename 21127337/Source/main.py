from utils import readMazeFromFile
from breadth_first_search import bfs
from depth_first_search import dfs
from uniform_cost_search import ucs
from greedy_best_first_search import greedy_best_first_search
from a_star_search import a_star
import os


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(dir_path)

    files = os.listdir(f"{parent_dir}/Input")
    mazes = []
    for file in files:
        if file.split(".")[1] == "txt":
            mazes.append(file)
    print("Maze available:\n", mazes)
    filename = input("Enter filename (without .txt ext): ")

    adj_list, size, start, goal = readMazeFromFile(f"{parent_dir}/Input/{filename}.txt")
    print("Adjacency List:")
    for node, neighbors in adj_list.items():
        print(node, ":", neighbors)
    print(f"Go from vertex: {start} to vertex {goal}")
    print("\n\n====* Maze search using BFS *====\n", end="")
    bfs_path, explored, time = bfs(adj_list, start, goal)
    print("\nPath found: ", bfs_path)
    print("Explored Path: ", explored)
    print("Time to escape the maze: ", time)
    print("\n\n====* Maze search using DFS *====\n", end="")
    dfs_path, explored, time = dfs(adj_list, start, start, goal)
    print("\nPath found: ", dfs_path)
    print("Explored Path: ", explored)
    print("Time to escape the maze: ", time)
    print("\n\n====* Maze search using UCS *====\n", end="")
    ucs_path, explored, time = ucs(adj_list, start, goal)
    print("\nPath found: ", ucs_path)
    print("Explored Path: ", explored)
    print("Time to escape the maze: ", time)
    print("\n\n====* Maze search using GBFS *====\n", end="")
    gbfs_path, explored, explored_with_cost, time = greedy_best_first_search(
        adj_list, start, goal, size
    )
    print("\nPath found: ", gbfs_path)
    print("Explored Path: ", explored)
    print("Explored Path with H(n): ", explored_with_cost)
    print("Time to escape the maze: ", time)
    print("\n\n====* Maze search using A* *====\n", end="")
    a_star_path, explored, explored_with_cost, time = a_star(
        adj_list, start, goal, size
    )
    print("\nPath found: ", a_star_path)
    print("Explored Path: ", explored)
    print("Explored Path with F(n): ", explored_with_cost)
    print("Time to escape the maze: ", time)
