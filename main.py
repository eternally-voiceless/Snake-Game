import sys
import pygame
from tools import GameObject, Grid, SnakeBlock

pygame.init()

window_size = window_width, window_height = 1280, 610 # should be 1280, 720 instead
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
dt = 0

test_snake_block = GameObject("./snake-parts/head.svg", (10, 10))

margin = 1
layer = Grid(window, (10, 10), (20, 60))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    window.fill("#0D1B2A")
    layer.draw()

    test_snake_block.set_speed_by_click(100, dt).damping(10, dt).update(dt)
    test_snake_block.restrict(layer).draw(window)

    pygame.display.update()
    dt = clock.tick(60)/1000