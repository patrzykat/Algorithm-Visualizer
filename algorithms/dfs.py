import pygame
import main


def dfs(draw, grid, start_node, end_node):
    start_node.parent = None
    queue = [start_node]

    while len(queue) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current_node = queue.pop()
        for neighbor in current_node.neighbors:
            if not neighbor.is_closed() and not neighbor.is_start():
                neighbor.parent = current_node
                queue.append(neighbor)
                neighbor.make_closed()
            if neighbor == end_node:
                main.draw_path(draw, end_node)
                return True

        draw()

    return False

