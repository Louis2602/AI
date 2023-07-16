import tkinter as tk
from pil import Image, ImageTk
import time
import data 

size_of_block = 50 

class PacmanGame(tk.Frame):
    def __init__(self, maze_name, master = None):
        super().__init__(master)
        master.resizable(width = False, height = False)
        self.score = 0
        self.maze, self.size, self.pacman_pos = data.get_maze(maze_name)
        self.pacman = None
        self.food = []
        self.monster = []
        self.maze_frame = tk.Canvas(width = self.size[1] * size_of_block + 200, height = self.size[0] * size_of_block, bg = "black")
        self.maze_frame.pack() 
    
    def draw_maze(self):
        wall_block_image = Image.open("../IMAGE/wall_block.png")
        wall_block_image = wall_block_image.resize((size_of_block, size_of_block), Image.ANTIALIAS)
        wall_block_image = ImageTk.PhotoImage(wall_block_image)

        food_image = Image.open("../IMAGE/food.png")
        food_image = food_image.resize((size_of_block, size_of_block), Image.ANTIALIAS)
        food_image = ImageTk.PhotoImage(food_image)

        ghost_image = Image.open("../IMAGE/ghost.png")
        ghost_image = ghost_image.resize((size_of_block, size_of_block), Image.ANTIALIAS)
        ghost_image = ImageTk.PhotoImage(ghost_image)

        score_image = Image.open("../IMAGE/score.png")
        score_image = score_image.resize((180, 130), Image.ANTIALIAS)
        score_image = ImageTk.PhotoImage(score_image)

        score_image_frame = self.maze_frame.create_image(self.size[1] * size_of_block + 20, (self.size[0] * size_of_block)//2 - 50, anchor='nw', image=score_image)

        for row in range(self.size[0]):
            for column in range(self.size[1]):
                if self.maze[row][column] == 1:
                    self.maze_frame.create_image(column * size_of_block, row * size_of_block, anchor='nw', image=wall_block_image)
                if self.maze[row][column] == 2:
                    self.food.append([self.maze_frame.create_image(column * size_of_block, row * size_of_block, anchor='nw', image=food_image), (row, column)])
        
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                if self.maze[row][column] == 3:
                    self.monster.append([self.maze_frame.create_image(column * size_of_block, row * size_of_block, anchor='nw', image=ghost_image), (row, column)])
        
        self.maze_frame.image = [wall_block_image, food_image, ghost_image, score_image]

    def draw_pacman(self):
        pacman_image = Image.open("../IMAGE/pacman.png")
        pacman_image = pacman_image.resize((size_of_block, size_of_block), Image.ANTIALIAS)
        pacman_image = ImageTk.PhotoImage(pacman_image)

        self.pacman = self.maze_frame.create_image(self.pacman_pos[1] * size_of_block, self.pacman_pos[0] * size_of_block, anchor='nw', image=pacman_image)
        self.maze_frame.image.append(pacman_image)
    
    def show_score(self):
        self.score_text = self.maze_frame.create_text(self.size[1] * size_of_block + 170, (self.size[0] * size_of_block)//2 , fill = "white", font = "Times 30 italic bold", text = self.score, anchor = "ne")
        
        
        
    def pacman_move(self, pacman_path, monster_path, index_path, speed):
        #stop
        self.score -= 1
        self.maze_frame.itemconfigure(self.score_text, text=self.score)
        if index_path == len(pacman_path):
            return self.score

        #check food
        if self.maze[pacman_path[index_path][0]][pacman_path[index_path][1]] == 2:
            for i in range(len(self.food)):
                if self.food[i][1] == pacman_path[index_path]:
                    del_image = self.food[i][0]
                    self.score += 20
                    self.maze_frame.itemconfigure(self.score_text, text=self.score)
                    self.maze_frame.delete(del_image)
                    self.maze[pacman_path[index_path][0]][pacman_path[index_path][1]] = 0
                    break
 
        #continue
        self.maze_frame.move(self.pacman, (pacman_path[index_path][1] - pacman_path[index_path - 1][1]) * size_of_block,  (pacman_path[index_path][0] - pacman_path[index_path - 1][0]) * size_of_block )
        self.maze_frame.after(speed)
        self.maze_frame.update()

        if not monster_path:
            return self.pacman_move(pacman_path, monster_path, index_path + 1, speed)
            
        return self.monster_move(pacman_path, monster_path, index_path, speed)

    def monster_move(self, pacman_path, monster_path, index_path, speed):
        if index_path == len(monster_path[0]):
            return self.score

        for i in range(len(monster_path)):
            self.maze_frame.move(self.monster[i][0], (monster_path[i][index_path][1] - monster_path[i][index_path - 1][1]) * size_of_block,  (monster_path[i][index_path][0] - monster_path[i][index_path - 1][0]) * size_of_block )
        
        self.maze_frame.after(speed)
        self.maze_frame.update()

        return self.pacman_move(pacman_path, monster_path, index_path + 1, speed)

