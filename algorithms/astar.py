import pygame
import main


def astar(draw, grid, start_node, end_node):
    start_node.parent = None
    start_node.distance = 0
    start_node.manhattan_distance = calculate_manhattan_distance(start_node.row, end_node.row, start_node.col, end_node.col)
    sorted_queue = [(start_node.manhattan_distance, start_node)]

    while len(sorted_queue) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current_node = sorted_queue.pop(0)[-1]
        for neighbor in current_node.neighbors:
            if not neighbor.is_closed() and not neighbor.is_start():
                neighbor.parent = current_node
                neighbor.distance = current_node.distance + 1
                neighbor.manhattan_distance = calculate_manhattan_distance(neighbor.row, end_node.row, neighbor.col, end_node.col)
                sorted_queue.append((neighbor.distance + neighbor.manhattan_distance, neighbor))
                sorted_queue.sort()
                neighbor.make_closed()
            if neighbor == end_node:
                main.draw_path(draw, end_node)
                return True

        draw()

    return False


def calculate_manhattan_distance(x1, x2, y1, y2):
    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    return x_distance + y_distance
