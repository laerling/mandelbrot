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
        julia = mb.is_julia()
        mb = mandelbrot.Mandelbrot()
        mb.set_julia(julia)
    elif user_action == draw.UserAction.INCREASE_DEPTH:
        mb.set_depth(mb.get_depth() + 10)
    elif user_action == draw.UserAction.DECREASE_DEPTH:
        mb.set_depth(mb.get_depth() - 10)

# start
while True:
    handle_user_action(mb.draw(_width, _height))
