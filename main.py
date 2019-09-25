#!/usr/bin/env python3.7

import julia
import mandelbox
import mandelbrot

import canvas
import math
import pygame
import view


canvas = canvas.Canvas(800, 600)

general_keys = [
    pygame.K_q,      # quit
    pygame.K_SPACE,  # pause rendering
    pygame.K_f,      # cycle between fractals
    pygame.K_r,      # reset parameters
    pygame.K_PLUS,   # zoom in
    pygame.K_MINUS,  # zoom out
    pygame.K_UP,     # move up
    pygame.K_DOWN,   # move down
    pygame.K_LEFT,   # move left
    pygame.K_RIGHT,  # move right
    pygame.K_PERIOD, # increase depth
    pygame.K_COMMA,  # decrease depth
]

def make_mandelbrot():
    m = mandelbrot.Mandelbrot(
        canvas, allowed_keyevents=general_keys)
    m.view.rectify()
    return m

def make_julia():
    j = julia.Julia(
        make_mandelbrot(),
        canvas, allowed_keyevents=general_keys + [
            pygame.K_w,      # move julia constant up
            pygame.K_a,      # move julia constant left
            pygame.K_s,      # move julia constant down
            pygame.K_d,      # move julia constant right
        ])
    j.view.rectify()
    return j

def make_mandelbox():
    m = mandelbox.Mandelbox(
        canvas, allowed_keyevents=general_keys)
    m.view.rectify()
    return m

def make_fractals(fractal_i=None):
    global fractals
    # maybe initialize
    if len(fractals) != 3:
        fractals = [None, None, None]
        fractal_i = None
    # make all fractals
    if fractal_i == None:
        for i in range(3):
            make_fractals(fractal_i=i)
    # make mandelbrot
    elif fractal_i == 0:
        fractals[fractal_i] = make_mandelbrot()
    # make julia
    elif fractal_i == 1:
        fractals[fractal_i] = make_julia()
    # make mandelbox
    elif fractal_i == 2:
        fractals[fractal_i] = make_mandelbox()

# create fractals
fractals = []
make_fractals()
fractal_i = 0

# event loop
while True:
    events = fractals[fractal_i].render()
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
                fractals[fractal_i].toggle_pause()

            # cycle fractals
            elif e.key == pygame.K_f:
                fractal_i += 1
                if fractal_i >= len(fractals):
                    fractal_i = 0

            # reset
            elif e.key == pygame.K_r:
                make_fractals(fractal_i=fractal_i)

            # zooming
            elif e.key == pygame.K_PLUS:
                fractals[fractal_i].view.zoom(factor=2)
            elif e.key == pygame.K_MINUS:
                fractals[fractal_i].view.zoom(factor=0.5)

            # moving around
            elif e.key == pygame.K_UP:
                fractals[fractal_i].view.move(view.Direction.UP)
            elif e.key == pygame.K_DOWN:
                fractals[fractal_i].view.move(view.Direction.DOWN)
            elif e.key == pygame.K_LEFT:
                fractals[fractal_i].view.move(view.Direction.LEFT)
            elif e.key == pygame.K_RIGHT:
                fractals[fractal_i].view.move(view.Direction.RIGHT)

            # changing depth
            elif e.key == pygame.K_PERIOD:
                # Round to ceiling, else e. g. (2 * 1.1) = 2.2 becomes 2 again.
                fractals[fractal_i].set_depth(math.ceil(fractals[fractal_i]._depth * 1.1))
                print("Set depth to", fractals[fractal_i]._depth)
            elif e.key == pygame.K_COMMA:
                # Round to floor, else e. g. (2 / 1.1) 1.818 becomes 2 again.
                fractals[fractal_i].set_depth(math.floor(fractals[fractal_i]._depth / 1.1))
                print("Set depth to", fractals[fractal_i]._depth)

            # moving julia constant
            elif e.key == pygame.K_w:
                fractals[fractal_i].move_constant(view.Direction.UP)
            elif e.key == pygame.K_s:
                fractals[fractal_i].move_constant(view.Direction.DOWN)
            elif e.key == pygame.K_a:
                fractals[fractal_i].move_constant(view.Direction.LEFT)
            elif e.key == pygame.K_d:
                fractals[fractal_i].move_constant(view.Direction.RIGHT)
