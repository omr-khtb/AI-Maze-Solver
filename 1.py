import pygame
import sys
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from queue import Queue  
from queue import PriorityQueue
from collections import deque
GRID_SIZE = 20
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (0, 255, 0)
START_COLOR = (0, 0, 255)
END_COLOR = (255, 0, 0)

class MazeSizeInputScreen:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((500, 350))
        pygame.display.set_caption("Maze Size Input")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)
        self.rows = 0
        self.cols = 0
        self.create_button = pygame.Rect(350, 170, 120, 50)

        self.input_boxes = [pygame.Rect(150, 80, 200, 50), pygame.Rect(150, 150, 200, 50)]
        self.labels = ["Rows:", "Cols:"]
        self.texts = ["", ""]
        self.active_input = 0

        self.background_image = pygame.image.load(os.path.join("img", "bubble.png")).convert()

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event)

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.start_maze_creation()
        elif event.key == pygame.K_TAB:
            self.active_input = (self.active_input + 1) % len(self.input_boxes)

        if event.type == pygame.KEYDOWN and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.texts[self.active_input] = self.texts[self.active_input][:-1]
            else:
                self.texts[self.active_input] += event.unicode

    def handle_mouse_click(self, event):
        for i, box in enumerate(self.input_boxes):
            if box.collidepoint(event.pos):
                self.active_input = i

        if self.create_button.collidepoint(event.pos):
            self.start_maze_creation()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), self.create_button)
        text = self.font.render("Create", True, (0, 0, 0))
        self.screen.blit(text, (380, 185))

        for i, (label, box) in enumerate(zip(self.labels, self.input_boxes)):
            pygame.draw.rect(self.screen, (255, 255, 255), box, 2)
            label_text = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(label_text, (box.x - 70, box.y + 5))
            input_text = self.font.render(self.texts[i], True, (255, 255, 255))
            self.screen.blit(input_text, (box.x + 5, box.y + 5))

        instruction_font = pygame.font.Font(None, 20)
        instruction_text = [
            "Instructions:",
            "'w': Walls",
            "'e': End Point",
            "'s': Start Point",
            "'z': Depth First Search",
            "'x': Breadth First Search ,",
            "'c': A* Search,'v': Clear Screen",
        ]
        for i, text in enumerate(instruction_text):
            instruction_rendered = instruction_font.render(text, True, (255, 255, 255))
            self.screen.blit(instruction_rendered, (50, 220 + i * 20 -20))

        pygame.display.flip()

    def start_maze_creation(self):
        try:
            self.rows = int(self.texts[0])
            self.cols = int(self.texts[1])
            if self.rows > 0 and self.cols > 0:
                pygame.quit()
                maze_solver = MazeSolverApp(self.rows, self.cols)
                maze_solver.solve_maze(maze_solver.convert_to_matrix())
        except ValueError:
            self.show_alert("Error", "Please enter valid numbers for rows and columns.")

    def show_alert(self, title, message):
        root = tk.Tk()
        root.withdraw()  
        messagebox.showinfo(title, message)
        root.destroy()  

class MazeSolverApp:
    def __init__(self, rows, cols):
        pygame.init()

        self.width, self.height = cols, rows

        self.screen = pygame.display.set_mode((self.width * GRID_SIZE, self.height * GRID_SIZE))
        pygame.display.set_caption("Maze Solver")

        self.clock = pygame.time.Clock()

        self.maze = [[0] * self.width for _ in range(self.height)]
        self.heuristic = [[0] * self.width for _ in range(self.height)]
        self.start_point = None
        self.end_points = []

        self.draw_mode = "wall"

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event)

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_keydown(self, event):
        if event.key == pygame.K_e:
            self.draw_mode = "end"
        elif event.key == pygame.K_s:
            self.draw_mode = "start"
        elif event.key == pygame.K_w:
            self.draw_mode = "wall"
        elif event.key == pygame.K_d:
            self.draw_mode = "delete"
        elif event.key == pygame.K_z:
            if self.check_points():
                self.solve_maze()
        elif event.key == pygame.K_x:
            if self.check_points():
                self.solve_maze2()
        elif event.key == pygame.K_c:
            if self.check_points():
                self.solve_maze3()
        elif event.key == pygame.K_v:
            self.clear_visited_and_fringe()


        elif event.key == pygame.K_h:
            self.draw_mode = "heuristic"

    def handle_mouse_click(self, event):
        row = event.pos[1] // GRID_SIZE
        col = event.pos[0] // GRID_SIZE

        if event.button == 1: 
            if self.draw_mode == "start":
                self.start_point = (row, col)
            elif self.draw_mode == "end":
                self.end_points.append((row, col))
            elif self.draw_mode == "wall":
                self.maze[row][col] = 1
            elif self.draw_mode == "delete":
                self.maze[row][col] = 0
                self.end_points = [point for point in self.end_points if point != (row, col)]
            elif self.draw_mode == "heuristic":
                self.set_heuristic_value(row, col)

    def set_heuristic_value(self, row, col):
        value = simpledialog.askinteger("Heuristic Value", "Enter heuristic value:")
        if value is not None:
            self.heuristic[row][col] = value
    def clear_visited_and_fringe(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == 4 or self.maze[row][col] == 5:
                    self.maze[row][col] = 0
                    pygame.draw.rect(self.screen, BACKGROUND_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.maze[row][col] == 2:
                    pygame.draw.rect(self.screen, START_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif (row, col) in self.end_points:
                    self.maze[row][col] = 3
                    pygame.draw.rect(self.screen, END_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.maze[row][col] == 3:  
                    pygame.draw.rect(self.screen, END_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    

    def solve_maze(self):
        print("THIS IS DEPTH FIRST:")
        self.clear_visited_and_fringe()
        numeric_matrix = self.convert_to_matrix()
        print("Heuristic Matrix:")
        for row in self.heuristic:
            print(row)
        print("Maze Size:", (self.width, self.height))
        print("Start Point:", self.start_point)
        print("End Points:", self.end_points)
        print("Numeric Matrix:")
        
        for row in numeric_matrix:
            print(row)

        def perform_dfs(matrix, start, goals):
            rows, cols = len(matrix), len(matrix[0])
            visited = set()
            fringe = [start]
            visited_nodes = []
            fringe_nodes = [start]
            path = {start: None}

            def is_valid(cell):
                i, j = cell
                return 0 <= i < rows and 0 <= j < cols and matrix[i][j] in [0, 3] and cell not in visited

            while fringe:
                current_cell = fringe.pop()  
                visited_nodes.append(current_cell)
                visited.add(current_cell)

                if current_cell in goals:
                    break

                neighbors = [(current_cell[0] + di, current_cell[1] + dj) for di, dj in [(0, 1), (0, -1), (-1, 0), (1, 0)]]
                for neighbor in neighbors:
                    if is_valid(neighbor):
                        fringe.append(neighbor) 
                        fringe_nodes.append(neighbor)
                        path[neighbor] = current_cell

            correct_path = []
            current = current_cell
            while current is not None:
                correct_path.insert(0, current)
                current = path.get(current, None)

            print("Visited Nodes:", visited_nodes)
            print("Fringe Nodes:", fringe_nodes)
            print("Correct Path:", correct_path)

            return visited_nodes, fringe_nodes, correct_path

        visited_nodes, fringe_nodes, correct_path = perform_dfs(numeric_matrix, self.start_point, self.end_points)

        for node in visited_nodes:
            if node == self.start_point or node in self.end_points:
                continue
            self.maze[node[0]][node[1]] = 4 
            self.draw()
            pygame.draw.rect(self.screen, (173, 216, 230), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            pygame.time.delay(10)  

        for node in correct_path:
            if node == self.start_point or node in self.end_points:
                continue

            self.maze[node[0]][node[1]] = 5  
            self.draw()
            pygame.draw.rect(self.screen, (31, 81, 255), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            pygame.time.delay(10)  
    def solve_maze2(self):
        print("THIS IS BREADTH FIRST:")
        self.clear_visited_and_fringe()
        numeric_matrix = self.convert_to_matrix()
        print("Heuristic Matrix:")
        for row in self.heuristic:
            print(row)
        print("Maze Size:", (self.width, self.height))
        print("Start Point:", self.start_point)
        print("End Points:", self.end_points)
        print("Numeric Matrix:")

        for row in numeric_matrix:
            print(row)

        pygame.display.flip()
        def bfs(matrix, start, goals):
            
            matrix[start[0]][start[1]] = 2
            for goal in goals:
                matrix[goal[0]][goal[1]] = 3

            rows, cols = len(matrix), len(matrix[0])
            visited = set()
            fringe = Queue()
            fringe.put(start)
            visited_nodes = []
            fringe_nodes = [start] 
            path = {start: None}
          
            def is_valid(cell):
                i, j = cell
                return 0 <= i < rows and 0 <= j < cols and matrix[i][j] in [0, 2, 3] and cell not in visited and cell not in fringe_nodes
          
            while not fringe.empty():
                current_cell = fringe.get()
          
                visited.add(current_cell)
                visited_nodes.append(current_cell)
                fringe_nodes.remove(current_cell)
          
                if current_cell in goals:
                    print("Goal Reached!")
                    break  
          
                neighbors = [(current_cell[0] + di, current_cell[1] + dj) for di, dj in [(0, 1), (0, -1), (-1, 0), (1, 0)]]
          
                for neighbor in neighbors:
                    if is_valid(neighbor):
                        fringe.put(neighbor)
                        fringe_nodes.append(neighbor)
                        path[neighbor] = current_cell
          
            goal_reached = current_cell in goals
            if goal_reached:
                current = current_cell
                path_to_goal = []
                while current is not None:
                    path_to_goal.append(current)
                    current = path.get(current, None)
          
                path_to_goal.reverse()  
            else:
                print("Goal not reached.")
          
 
            print("Visted Nodes:", visited_nodes)
            print("path to goal Nodes:", path_to_goal)
            return visited_nodes, path_to_goal

        

        visited_nodes, correct_path = bfs(numeric_matrix, self.start_point, self.end_points)

        for node in visited_nodes:
            if node == self.start_point or node in self.end_points:
                continue
            self.maze[node[0]][node[1]] = 4  
            self.draw()
            pygame.draw.rect(self.screen, (255, 255, 255), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            pygame.time.delay(10) 

        for node in correct_path:
            if node == self.start_point or node in self.end_points:
                continue
            self.maze[node[0]][node[1]] = 5 
            self.draw()
            pygame.draw.rect(self.screen, (192, 192, 192), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            pygame.time.delay(10)  
   
    def solve_maze3(self):
     print("THIS IS A*:")
     self.clear_visited_and_fringe()
     numeric_matrix = self.convert_to_matrix()
     print("Heuristic Matrix:")
     for row in self.heuristic:
         print(row)
     print("Maze Size:", (self.width, self.height))
     print("Start Point:", self.start_point)
     print("End Points:", self.end_points)
     print("Numeric Matrix:")
 
     for row in numeric_matrix:
         print(row)
 
     pygame.display.flip()
     def aStar(maze_matrix, start, goals):
            def h(cell, goals):
                return min(abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) for goal in goals)
        
            def get_cells(matrix):
                return {(i, j) for i, row in enumerate(matrix) for j, cell in enumerate(row)}
        
            def get_neighbors(cell, matrix):
                i, j = cell
                neighbors = []
        
                for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] != 1:
                        neighbors.append((x, y))
        
                return neighbors
        
            start = tuple(start[0])  
            goals = [tuple(goal) for goal in goals]  
        
            g_score = {cell: float('inf') for cell in get_cells(maze_matrix)}
            g_score[start] = 0
        
            f_score = {cell: float('inf') for cell in get_cells(maze_matrix)}
            f_score[start] = h(start, goals)
        
            open_set = PriorityQueue()
        
            tie_breaker = 0
        
            open_set.put((h(start, goals), tie_breaker, start))
            aPath = {}
            visited_cells = []
        
            while not open_set.empty():
                currCell = open_set.get()[2]
        
                if currCell in goals:
                    break
        
                visited_cells.append(currCell) 
        
                for neighbor in get_neighbors(currCell, maze_matrix):
                    temp_g_score = g_score[currCell] + 1
                    temp_f_score = temp_g_score + h(neighbor, goals)
        
                    if temp_f_score < f_score[neighbor]:
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_f_score
        
                        tie_breaker += 1
        
                        open_set.put((temp_f_score, tie_breaker, neighbor))
                        aPath[neighbor] = currCell
        
            fwdPath = {}
            cell = min(goals, key=lambda goal: f_score[goal]) 
            while cell != start:
                fwdPath[aPath[cell]] = cell
                cell = aPath[cell]
            reversed_path = {v: k for k, v in fwdPath.items()}
            PathList = []
            for key in list(fwdPath.keys()):
                PathList.append(key)
            PathList.reverse()
        
            return visited_cells, PathList
     start_point_list = [self.start_point]  
     end_points_list = [list(point) for point in self.end_points] 
 
     visited_nodes, correct_path = aStar(numeric_matrix, start_point_list, end_points_list)
 
     for node in visited_nodes:
         if node == self.start_point or node in self.end_points:
             continue
         self.maze[node[0]][node[1]] = 4
         self.draw()
         pygame.draw.rect(self.screen, (255, 255, 255), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
         pygame.display.flip()
         pygame.time.delay(10)
 
     for node in correct_path:
         if node == self.start_point or node in self.end_points:
             continue
         self.maze[node[0]][node[1]] = 5
         self.draw()
         pygame.draw.rect(self.screen, (192, 192, 192), (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
         pygame.display.flip()
         pygame.time.delay(10)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(self.screen, (255, 255, 255), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if self.start_point == (row, col):
                    pygame.draw.rect(self.screen, START_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                for end_point in self.end_points:
                    if end_point == (row, col):
                        pygame.draw.rect(self.screen, END_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if self.maze[row][col] == 4:
                    pygame.draw.rect(self.screen, (255, 255, 255), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.maze[row][col] == 5:
                    pygame.draw.rect(self.screen, (192, 192, 192), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

                heuristic_value = self.heuristic[row][col]
                if heuristic_value > 0:
                    font = pygame.font.Font(None, 20)
                    text = font.render(str(heuristic_value), True, (255, 255, 255))
                    self.screen.blit(text, (col * GRID_SIZE + GRID_SIZE // 2 - 5, row * GRID_SIZE + GRID_SIZE // 2 - 5))

    def check_points(self):
        if self.start_point is None:
            self.show_alert("Error", "Please set a start point.")
            return False
        elif len(self.end_points) == 0:
            self.show_alert("Error", "Please set at least one end point.")
            return False
        return True

    def convert_to_matrix(self):
        matrix = [[0] * self.width for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) == self.start_point:
                    matrix[row][col] = 2
                elif (row, col) in self.end_points:
                    matrix[row][col] = 3
                else:
                    matrix[row][col] = self.maze[row][col]
        return matrix

    def show_alert(self, title, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()

if __name__ == "__main__":
    size_input_screen = MazeSizeInputScreen()
