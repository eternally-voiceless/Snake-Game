import sys
import pygame
from tools import GameObject, Grid, SnakeBlock

pygame.init()

window_size = window_width, window_height = 1280, 610 # should be 1280, 720 instead
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
dt = 0

margin = 1
layer = Grid(window, (10, 10), (28, 60))

test_snake_block_init_position = layer.get_nodes()[13][9]
test_snake_block = SnakeBlock("./snake-parts/head.svg", test_snake_block_init_position)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    window.fill("#0D1B2A")
    layer.draw()

    test_snake_block.interact_with_user(layer,50, dt)
    test_snake_block.point_closest_nodes(window, layer)
    test_snake_block.restrict(layer)
    test_snake_block.update(dt).draw(window)

    pygame.display.update()
    dt = clock.tick(60)/1000