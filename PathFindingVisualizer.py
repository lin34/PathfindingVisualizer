# ECE457A Assignment 2 Maze path finding
# Michael Lin
from maze import maze

# Each node in the maze is represented by an object
import pygame
import math
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH + 100))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

BFS = 0
DFS = 1
ASTAR = 2

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		# DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		# RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False
# pygame's x,y starts at top left
# Maze's co-ordinates start at bottom left


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	minimumPathCost=0
	while current in came_from:
		minimumPathCost += 1
		current = came_from[current]
		current.make_path()
		draw()
	return minimumPathCost + 1#include end node

#Three algorithms used:
#BFS
#DFS
#A* search
#output: complete path, its cost and the number of nodes explored

#bfs uses a queue to store its open set
def algorithm_bfs(draw, grid, start, end):
	

	return False
#dfs uses a stack 
def algorithm_dfs(draw, grid, start, end):
	count = 0
	open_set = []
	open_set.append(start)

	return False
#A* uses a priority queue, and a cost function f = g + h
#h is the heuristic function, using Manhattan distance
def algorithm_astar(draw, grid, start, end):
	count = 0
	minimumCost_=-1
	nodesExplored=-1
	open_set = PriorityQueue()#Fringe nodes to be visited
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}#Visited nodes

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			minimumCost_ = reconstruct_path(came_from, end, draw)
			nodesExplored=count
			end.make_end()
			return minimumCost_, nodesExplored

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()
	
	return -1, -1


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, pathCost=-1, nodesExplored=-1):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.font.init()
	myFont = pygame.font.Font("./OpenSans-VariableFont_wdth,wght.ttf", 15)
	if pathCost != -1:
		label = myFont.render("Minimum path cost: " + str(pathCost), 1, BLACK)
		WIN.blit(label, (100, WIDTH + 20))
	if nodesExplored!=-1:
		label2 = myFont.render("Nodes explored: " + str(nodesExplored), 1, BLACK)
		WIN.blit(label2, (100, WIDTH + 50))
	
	label3 = myFont.render("Press space to begin search ", 1, BLACK)
	WIN.blit(label3, (300, WIDTH + 20))
	label4 = myFont.render("Press c to clear board", 1, BLACK)
	WIN.blit(label4, (300, WIDTH + 50))
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 25
	algo = ASTAR
	minimumCost = -1
	nodesExplored = -1
	grid = make_grid(ROWS, width)
    # note, pygame uses top left as (0,0) but data is given as bottom left first
    # using pygame coordinate as master
	start = grid[2][13]
	start.make_start()#orange
	end = grid[23][5]  # E1: 5, 23  E2: 2, 3
	end.make_end()#blue
	for j in range(ROWS):  # col
		for i in range(ROWS):  # row
			i_ = ROWS - 1 - i
			node = grid[j][i]
			if maze[i_][j] == 1:
				node.make_barrier()
    
	run = True
	while run:
		draw(win, grid, ROWS, width, minimumCost, nodesExplored)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					if algo == ASTAR:
						minimumCost, nodesExplored= algorithm_astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == BFS:
						algorithm_bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == DFS:
						algorithm_dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_c:
					start = None
					end = None
					minimumCost = -1
					nodesExplored = -1
					grid = make_grid(ROWS, width)

	pygame.quit()


main(WIN, WIDTH)
