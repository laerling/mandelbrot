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

    _julia = False
    _julia_x = 0.7
    _julia_y = 0.3

    frame = Frame()

    def __init__(self, iter=_iter, max_val=_max_val, julia=_julia):
        self._iter = iter
        self._max_val = max_val
        self._julia = julia

    def toggle_julia(self):
        self._julia = not self._julia
        if self._julia:
            x = -2 + random.random() * 3
            if x == 0:
                y = -2 + random.random() * 4
            else:
                y = random.random() * 1 / (100 * abs(x))
            print("Julia: ({}, {})".format(x, y))
            self._julia_x = x
            self._julia_y = y

    def calc_point(self, point, constant):
        for i in range(self._iter):
            point = ( point[0]**2 - point[1]**2 + constant[0],
                  2 * point[0] * point[1] + constant[1] )
            if point[0] > self._max_val or point[1] > self._max_val:
                break
        return i / (self._iter-1)

    def draw(self, width, height, steps=500_000):

        # clear canvas
        draw.rectangle((0,0), (width,height), draw.black)

        for count in range(steps):

            # check for user action
            user_action = draw.getUserAction()
            if user_action != None:
                return user_action

            # initialize variables for this round
            pos = (random.randrange(width), random.randrange(height))
            c = (self.frame._x_min + (self.frame._x_max - self.frame._x_min) * (pos[0] / width),
                 self.frame._y_min + (self.frame._y_max - self.frame._y_min) * (pos[1] / height))

            if self._julia:
                val = self.calc_point(c, (self._julia_x, self._julia_y))
            else:
                val = self.calc_point(c, c)

            # calculate colors
            r = max(0, math.sin(1.5 * math.pi * val                 )) * 255
            g = max(0, math.sin(1.5 * math.pi * val - 0.25 * math.pi)) * 255
            b = max(0, math.sin(1.5 * math.pi * val - 0.5  * math.pi)) * 255
            update = random.randrange(1000) == 0

            # draw to screen
            update_after = 1000 # update every update_after steps
            # lower values for refining_speed make the picture stay coarse,
            # higher values make it too long to get finer.
            refining_speed = 750 # values between 500 and 1000 are good
            initial_shrink_f = 10
            draw.partial_square(pos, min(width, height),
                                count / refining_speed + initial_shrink_f,
                                color=(r,g,b),
                                #color=(val*255,val*255,val*255), # black and white
                                update_display=(count % update_after == 0))

        return draw.idle()
