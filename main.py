#!/usr/bin/env python3.7

import draw
import mandelbrot


# initialize canvas
_width = 800
_height = 600
draw.init(_width, _height)

# initialize variables
mb = mandelbrot.Mandelbrot()
mb.frame.rectify(_width, _height)

def handleUserAction(user_action):
    global mb
    if user_action == draw.UserAction.PAUSE:
        mb.toggle_pause()
    elif user_action == draw.UserAction.JULIA:
        mb.toggle_julia()
    elif user_action == draw.UserAction.RESET:
        mb = mandelbrot.Mandelbrot()

# start
while True:
    handleUserAction(mb.draw(_width, _height))
