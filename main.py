#!/usr/bin/env python3.7

import draw
import mandelbrot


# initialize canvas
_width = 800
_height = 600
draw.init(_width, _height)
draw.rectangle((0,0), (_width,_height), draw.black)

# initialize variables
m = mandelbrot.Mandelbrot()
m.frame.rectify(_width, _height)

# start
m.draw(_width, _height)
draw.idle()
