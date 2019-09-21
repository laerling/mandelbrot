import random
import math
import draw


class Frame:

    _x_min = -2
    _x_max = 1
    _y_min = -1.5
    _y_max = 1.5

    def __init__(self, min=(_x_min,_y_min), max=(_x_max,_y_max)):
        self._x_min = min[0]
        self._y_min = min[1]
        self._x_max = max[0]
        self._y_max = max[1]

    def __str__(self):
        return "( x:({}, {}), y:({}, {}) )".format(
            self._x_min, self._x_max, self._y_min, self._y_max)

    def rectify(self, width, height):
        x_middle = self._x_min + (self._x_max - self._x_min) / 2
        frame_width = (self._y_max - self._y_min) / height * width
        self._x_min = x_middle - frame_width / 2
        self._x_max = x_middle + frame_width / 2


class Mandelbrot:

    _iter = 100
    _max_val = 2

    frame = Frame()

    def __init__(self, iter=_iter, max_val=_max_val):
        self._iter = iter
        self._max_val = max_val

    def calc_point(self, point):
        x = (0,0)
        for i in range(self._iter):
            x = ( x[0]**2 - x[1]**2 + point[0],
                  2 * x[0] * x[1] + point[1] )
            if x[0] > self._max_val or x[1] > self._max_val:
                break
        return i / (self._iter-1)

    def draw(self, width, height, steps=500000):
        for count in range(steps):
                # initialize variables for this round
            pos = (random.randrange(width), random.randrange(height))
            c = (self.frame._x_min + (self.frame._x_max - self.frame._x_min) * (pos[0] / width),
                 self.frame._y_min + (self.frame._y_max - self.frame._y_min) * (pos[1] / height))

            val = self.calc_point(c)

            # calculate colors
            r = max(0, math.sin(1.5 * math.pi * val                 )) * 255
            g = max(0, math.sin(1.5 * math.pi * val - 0.25 * math.pi)) * 255
            b = max(0, math.sin(1.5 * math.pi * val - 0.5  * math.pi)) * 255
            update = random.randrange(1000) == 0

            # draw to screen
            #draw.pixel(pos, color=(r,g,b), update=update)
            draw.partial_square(pos, min(width, height),
                                (count/1000+1),
                                #color=(v,v,v),
                                color=(r,g,b),
                                update=(count%1000==0))
