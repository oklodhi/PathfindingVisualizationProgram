import pygame
import math
from queue import PriorityQueue

# Defining Pygame window
WINDOWRES = 800
WINDOW = pygame.display.set_mode((WINDOWRES, WINDOWRES))
pygame.display.set_caption("A* Pathfinding Visualization")

# Color codes for GUI visuals
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GREY = (220,220,220)


# Class container for a single node on the grid
class Space:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.column

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == YELLOW

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == PINK

    def is_finish(self):
        return self.color == CYAN

    def reset(self):
        self.color = WHITE

    def make_open(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = RED

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = PINK

    def make_finish(self):
        self.color = CYAN

    def make_path(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # keeps track of the neighboring nodes
    # in the up, down, left, right direction
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row+1][self.column].is_wall(): # down
            self.neighbors.append(grid[self.row+1][self.column])

        if self.row > 0 and not grid[self.row-1][self.column].is_wall(): # up
            self.neighbors.append(grid[self.row-1][self.column])

        if self.column < self.total_rows-1 and not grid[self.row][self.column+1].is_wall(): # right
            self.neighbors.append(grid[self.row][self.column+1])

        if self.column > 0 and not grid[self.row][self.column-1].is_wall(): # left
            self.neighbors.append(grid[self.row][self.column-1])

    def __lt__(self, other):
        return False

# Heuristic function returning absolute distance for estimate
def h(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 - y2)

# Backtracks on the shortest available path
# and draws it at the end of traversal
def reconstruct_path(previous_node, current, draw):
    while current in previous_node:
        current = previous_node[current]
        current.make_path()
        draw()

# A* algorithm implementation
# that evaluates the heuristic cost and exact cost to each node.
# Uses a Priority Queue to keep track of nodes
def a_star_algorithm(draw, grid, start, finish):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    previous_node = {}
    g_score = {space: float("inf") for row in grid for space in row}
    g_score[start] = 0
    f_score = {space: float("inf") for row in grid for space in row}
    f_score[start] = h(start.get_pos(), finish.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == finish:
            reconstruct_path(previous_node, finish, draw)
            finish.make_finish()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                previous_node[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), finish.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False

# Defining a 2D array for the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            space = Space(i, j, gap, rows)
            grid[i].append(space)
    return grid

# Drawing the 2D grid array in Pygame
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

# Drawing each node or "space" in the Pygame
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for space in row:
            space.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# Captures the coordinate of wherever the mouse pointer was clicked
def get_mouse_click_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    column = x // gap
    return row, column

# Main program logic
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    finish = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, column = get_mouse_click_position(pos, ROWS, width)
                space = grid[row][column]
                if not start and space != finish:
                    start = space
                    start.make_start()
                elif not finish and space != start:
                    finish = space
                    finish.make_finish()
                elif space != start and space != finish:
                    space.make_wall()
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, column = get_mouse_click_position(pos, ROWS, width)
                space = grid[row][column]
                space.reset()
                if space == start:
                    start = None
                elif space == finish:
                    finish = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and finish:
                    for row in grid:
                        for space in row:
                            space.update_neighbors(grid)
                    a_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, finish)
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    finish = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

# Run
main(WINDOW, WINDOWRES)