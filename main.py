import pygame
from algorithms import astar, bfs, dfs, backtracking

pygame.font.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Breadth First Search Pathfinding Algorithm")
FONT = pygame.font.SysFont("comicsansms", 32)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (130, 0, 130)
ORANGE = (255, 130, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, num_of_rows):
        self.row = row
        self.col = col
        self.width = width
        self.num_of_rows = num_of_rows
        self.x = width * row
        self.y = width * col
        self.color = BLACK
        self.neighbors = []
        self.parent = None
        self.distance = None
        self.manhattan_distance = None  # Used for A Star only

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == WHITE

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = WHITE

    def make_queen_incorrect_board(self):
        self.color = RED

    def make_queen_correct_board(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        if self.row < self.num_of_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.num_of_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def draw_path(draw, end_node):
    current_node = end_node
    while current_node.parent:
        current_node.color = YELLOW
        current_node = current_node.parent
        draw()
    end_node.make_end()
    return True


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def clear_grid(grid):
    for row in grid:
        for node in row:
            node.color = BLACK


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i*gap))
    for i in range(rows):
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def run_simulation(win, width, algorithm):
    rows = 50 if algorithm != "Backtracking" else 8
    grid = make_grid(rows, width)

    start = None if algorithm != "Backtracking" else True
    end = None if algorithm != "Backtracking" else True

    run = True

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif start and end and node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    if algorithm == 'BFS':
                        bfs.bfs(lambda: draw(win, grid, rows, width), grid, start, end)
                    elif algorithm == 'A Star':
                        astar.astar(lambda: draw(win, grid, rows, width), grid, start, end)
                    elif algorithm == 'DFS':
                        dfs.dfs(lambda: draw(win, grid, rows, width), grid, start, end)
                    elif algorithm == 'Backtracking':
                        backtracking.n_queens(lambda: draw(win, grid, rows, width), grid)

                if event.key == pygame.K_RETURN:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu(win)

    pygame.quit()


def main_menu(win):
    click = False
    while True:
        win.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(230, 150, 350, 50)
        button_2 = pygame.Rect(230, 300, 350, 50)
        button_3 = pygame.Rect(230, 450, 350, 50)
        button_4 = pygame.Rect(230, 600, 350, 50)
        text_1 = FONT.render('Breadth First Search', True, GREEN)
        text_2 = FONT.render('A Star Pathfinding', True, GREEN)
        text_3 = FONT.render('Depth First Search', True, GREEN)
        text_4 = FONT.render('N Queens', True, GREEN)
        if button_1.collidepoint((mx, my)):
            text_1 = FONT.render('Breadth First Search', True, BLUE)
            if click:
                run_simulation(win, WIDTH, algorithm='BFS')
        if button_2.collidepoint((mx, my)):
            text_2 = FONT.render('A Star Pathfinding', True, BLUE)
            if click:
                run_simulation(win, WIDTH, algorithm='A Star')
        if button_3.collidepoint((mx, my)):
            text_3 = FONT.render('Depth First Search', True, BLUE)
            if click:
                run_simulation(win, WIDTH, algorithm='DFS')
        if button_4.collidepoint((mx, my)):
            text_4 = FONT.render('N Queens', True, BLUE)
            if click:
                run_simulation(win, WIDTH, algorithm='Backtracking')
        pygame.draw.rect(win, (0, 0, 0), button_1)
        pygame.draw.rect(win, (0, 0, 0), button_2)
        pygame.draw.rect(win, (0, 0, 0), button_3)
        pygame.draw.rect(win, (0, 0, 0), button_4)
        win.blit(text_1, (250, 150))
        win.blit(text_2, (270, 300))
        win.blit(text_3, (255, 450))
        win.blit(text_4, (330, 600))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


if __name__ == "__main__":
    main_menu(WIN)









