import pygame
import main
from itertools import combinations


# Need to put in the chessboard backtracking algorithm to find all possible queen permutations
def n_queens(draw, grid):

    finished = False

    def is_diagonal(point1, point2):
        y_difference = abs(point2[0] - point1[0])
        x_difference = abs(point2[1] - point1[1])
        return x_difference == y_difference

    def check_board(lst_of_cols):
        queen_positions = [(i, lst_of_cols[i]) for i in range(8)]
        correct_board = True
        for comb in combinations(queen_positions, 2):
            if is_diagonal(comb[0], comb[1]):
                correct_board = False
                break
        return correct_board

    def draw_valid_board(lst_of_cols):
        for i in range(8):
            grid[i][lst_of_cols[i]].make_queen_correct_board()

    def draw_invalid_board(lst_of_cols):
        for i in range(8):
            grid[i][lst_of_cols[i]].make_queen_incorrect_board()

    def helper(cur_cols):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        nonlocal finished
        if not finished:
            if len(cur_cols) == 8:
                main.clear_grid(grid)
                if check_board(cur_cols):
                    draw_valid_board(cur_cols)
                    finished = True
                else:
                    draw_invalid_board(cur_cols)
                draw()
            else:
                for col in range(8):
                    if col not in cur_cols:
                        helper(cur_cols + [col])

    helper([])

