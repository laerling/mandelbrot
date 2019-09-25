#!/usr/bin/env python3.7

import mandelbrot
import math
import pygame
import canvas
import view


canvas = canvas.Canvas(800, 600, [
    pygame.K_q,
    pygame.K_SPACE,
    pygame.K_j,
    pygame.K_r,
    pygame.K_PLUS,
    pygame.K_MINUS,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_PERIOD,
    pygame.K_COMMA,
    pygame.K_w,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d
])

mb = mandelbrot.Mandelbrot(canvas)
mb.view.rectify()

while True:
    events = mb.render()
    # handle events, mainly keys
    for e in events:

        # quit
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

        # keys
        elif e.type == pygame.KEYDOWN:

            # quit
            if e.key == pygame.K_q:
                pygame.quit()
                quit()

            # pause/unpause rendering
            elif e.key == pygame.K_SPACE:
                mb.toggle_pause()

            # julia on/off
            elif e.key == pygame.K_j:
                mb.toggle_julia()

            # reset
            elif e.key == pygame.K_r:
                julia = mb._juliamode
                mb = mandelbrot.Mandelbrot(canvas)
                mb._juliamode = julia
                mb.view.rectify()

            # zooming
            elif e.key == pygame.K_PLUS:
                mb.view.zoom(factor=2)
            elif e.key == pygame.K_MINUS:
                mb.view.zoom(factor=0.5)

            # moving around
            elif e.key == pygame.K_UP:
                mb.view.move(view.Direction.UP)
            elif e.key == pygame.K_DOWN:
                mb.view.move(view.Direction.DOWN)
            elif e.key == pygame.K_LEFT:
                mb.view.move(view.Direction.LEFT)
            elif e.key == pygame.K_RIGHT:
                mb.view.move(view.Direction.RIGHT)

            # changing depth
            elif e.key == pygame.K_PERIOD:
                # Round to ceiling, else e. g. (2 * 1.1) = 2.2 becomes 2 again.
                mb.set_depth(math.ceil(mb._depth * 1.1))
                print("Set depth to", mb._depth)
            elif e.key == pygame.K_COMMA:
                # Round to floor, else e. g. (2 / 1.1) 1.818 becomes 2 again.
                mb.set_depth(math.floor(mb._depth / 1.1))
                print("Set depth to", mb._depth)

            # moving julia constant
            elif e.key == pygame.K_w:
                mb.julia_move(view.Direction.UP)
            elif e.key == pygame.K_s:
                mb.julia_move(view.Direction.DOWN)
            elif e.key == pygame.K_a:
                mb.julia_move(view.Direction.LEFT)
            elif e.key == pygame.K_d:
                mb.julia_move(view.Direction.RIGHT)
