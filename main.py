#!/usr/bin/env python3.7

import draw
import mandelbrot
import math


# initialize canvas
_width = 800
_height = 600
draw.init(_width, _height)

# initialize variables
mb = mandelbrot.Mandelbrot()
mb.frame.rectify(_width, _height)

def handle_user_action(user_action):
    global mb
    if user_action == draw.UserAction.PAUSE:
        mb.toggle_pause()
    elif user_action == draw.UserAction.ZOOM_IN:
        mb.frame.zoom()
    elif user_action == draw.UserAction.ZOOM_OUT:
        mb.frame.zoom(factor=0.5)
    elif (user_action == draw.UserAction.MOVE_LEFT or
          user_action == draw.UserAction.MOVE_RIGHT or
          user_action == draw.UserAction.MOVE_UP or
          user_action == draw.UserAction.MOVE_DOWN):
        mb.frame.move(user_action)
    elif (user_action == draw.UserAction.JULIA_MOVE_LEFT or
          user_action == draw.UserAction.JULIA_MOVE_RIGHT or
          user_action == draw.UserAction.JULIA_MOVE_UP or
          user_action == draw.UserAction.JULIA_MOVE_DOWN):
        if mb.is_julia():
            mb.julia_move(user_action)
    elif user_action == draw.UserAction.JULIA:
        mb.toggle_julia()
    elif user_action == draw.UserAction.RESET:
        mb = mandelbrot.Mandelbrot(julia=mb.is_julia())
        mb.frame.rectify(_width, _height)
    elif user_action == draw.UserAction.INCREASE_DEPTH:
        # Round to ceiling, else e. g. (2 * 1.1) = 2.2 becomes 2 again.
        mb.set_depth(math.ceil(mb.get_depth() * 1.1))
        print("Set depth to", mb.get_depth())
    elif user_action == draw.UserAction.DECREASE_DEPTH:
        # Round to floor, else e. g. (2 / 1.1) 1.818 becomes 2 again.
        mb.set_depth(math.floor(mb.get_depth() / 1.1))
        print("Set depth to", mb.get_depth())

# start
while True:
    handle_user_action(mb.draw(_width, _height))
