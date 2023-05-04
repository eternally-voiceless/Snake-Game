import sys
import pygame
from tools import GameObject, Playground, SnakeBlock

pygame.init()

window_size = window_width, window_height = 1280, 610 # should be 1280, 720 instead
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
dt = 0

test_snake_block = GameObject("./snake-parts/head.svg", (10, 10))

margin = 1
layer_left = 10
layer_top = 10
layer = Playground(window, (layer_left, layer_top), (28, 60))
layer_right = layer_left+layer.get_width()-test_snake_block.get_size()[0]
layer_bottom = layer_top+layer.get_height()-test_snake_block.get_size()[1]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    window.fill("#0D1B2A")
    layer.draw()

    test_snake_block.interact_with_user(200, dt).update(dt)
    test_snake_block.restrict(window, layer_top, layer_bottom-margin, layer_left, layer_right-margin)
    test_snake_block.draw(window)

    pygame.display.update()
    dt = clock.tick(60)/1000