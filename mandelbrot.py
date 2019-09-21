#!/usr/bin/env python3.7

import draw
import random
import math

_width = 800
_height = 600

draw.init(_width, _height)

# initialize variables
iter, max_value, counter = 100, 2, 10
frame = ((-2,1), (-1.5,1.5))

# rectify frame
x_middle = frame[0][0] + (frame[0][1] - frame[0][0]) / 2
frame_width = (frame[1][1] - frame[1][0]) / _height * _width
frame = ((x_middle - frame_width / 2, x_middle + frame_width / 2),
         (frame[1][0], frame[1][1]))

# clear canvas
draw.rectangle((0,0), (_width,_height), draw.black)

# start drawing
for counter in range(500000):

    # initialize variables for this round
    pos = (random.randrange(_width), random.randrange(_height))
    c = (frame[0][0] + (frame[0][1]-frame[0][0]) * (pos[0] / _width),
         frame[1][0] + (frame[1][1]-frame[1][0]) * (pos[1] / _height))

    # calculate round
    x = (0,0)
    for i in range(iter):
        x = ( x[0]**2 - x[1]**2 + c[0], 2 * x[0] * x[1] + c[1] )
        if x[0] > max_value or x[1] > max_value:
            break

    # calculate colors
    val = (i / (iter-1))
    r = max(0, math.sin(1.5 * math.pi * val                 )) * 255
    g = max(0, math.sin(1.5 * math.pi * val - 0.25 * math.pi)) * 255
    b = max(0, math.sin(1.5 * math.pi * val - 0.5  * math.pi)) * 255
    update = random.randrange(1000) == 0

    # draw to screen
    #draw.pixel(pos, color=(r,g,b), update=update)
    draw.partial_square(pos, min(_width, _height),
                        (counter/1000+1),
                        #color=(v,v,v),
                        color=(r,g,b),
                        update=(counter%1000==0))

draw.idle()
