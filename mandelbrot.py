import math
import pygame
import random
import view


class Mandelbrot:
    "Represents a mandelbrot set and all julia sets contained in it."

    def __init__(self, canvas, depth=100, threshold=10):
        self._juliamode = False
        self.paused = False
        # set parameters
        self._depth = depth
        self.generate_colortable()
        self.threshold = threshold
        self._julia = (0.7,0.3)
        # make view
        self.view = view.View(canvas, x=(-2,1), y=(-1.5,1.5))
        self.view.canvas.set_title("Mandelbrot")
        # log stuff
        self.print_julia_params();

    def set_depth(self, depth):
        """Set new depth to DEPTH or to 2, if DEPTH is smaller than 2.
        
        DEPTH must not be smaller than 2, because the mandelbrot algorithm divides by (depth - 1).
        """
        self._depth = max(2, depth)
        self.generate_colortable()

    def generate_colortable(self):
        "Generate the table that maps values to colors."
        self._colortable = []
        for v in range(self._depth):
            val = v / (self._depth - 1) # [0; 1]
            self._colortable.append((
                math.floor(max(0, math.sin(1.5 * math.pi * val                 )) * 255), # red
                math.floor(max(0, math.sin(1.5 * math.pi * val - 0.25 * math.pi)) * 255), # green
                math.floor(max(0, math.sin(1.5 * math.pi * val - 0.5  * math.pi)) * 255), # blue
                ))

    def print_julia_params(self):
        "Print julia parameters."
        print("Julia: ({}, {})".format(self._julia[0], self._julia[1]))

    def toggle_julia(self):
        "Toggle between rendering the mandelbrot set and a julia set."
        self.set_juliamode(not self._juliamode)
        if self._juliamode:
            self.print_julia_params()

    def set_juliamode(self, juliamode):
        "Enter or leave julia mode."
        self._juliamode = juliamode
        if juliamode:
            self.view.canvas.set_title("Mandelbrot (julia)")

    def julia_move(self, direction=None, factor=0.1):
        """Move the julia seed around in the mandelbrot set.
        
        The distance of movement is a fraction of the view's width or
        height, depending on the direction of movement.

        """
        # only move constant when in julia mode
        if not self._juliamode:
            return
        delta = (self.view.size_x() * factor,
                 self.view.size_y() * factor)
        if direction == view.Direction.UP:
            self._julia = (self._julia[0], self._julia[1] + delta[1])
        elif direction == view.Direction.DOWN:
            self._julia = (self._julia[0], self._julia[1] - delta[1])
        elif direction == view.Direction.LEFT:
            self._julia = (self._julia[0] - delta[0], self._julia[1])
        elif direction == view.Direction.RIGHT:
            self._julia = (self._julia[0] + delta[0], self._julia[1])
        self.print_julia_params()

    def toggle_pause(self):
        "Pause or unpause the rendering process."
        self.paused = not self.paused

    def calc_color(self, point, constant):
        "Calculate whether POINT is within the mandelbrot set or a specific julia set, depending on CONSTANT."
        for colortable_index in range(self._depth):
            point = ( point[0]**2 - point[1]**2 + constant[0],
                  2 * point[0] * point[1] + constant[1] )
            if point[0] > self.threshold or point[1] > self.threshold:
                break
        return colortable_index

    def render(self, steps=500_000):
        "Render the mandelbrot set or a julia set."

        # update window title
        if self._juliamode:
            self.view.canvas.set_title("Mandelbrot (julia) (rendering)")
        else:
            self.view.canvas.set_title("Mandelbrot (rendering)")

        # idle if paused
        if self.paused:
            if self._juliamode:
                return self.idle("Mandelbrot (julia)")
            else:
                return self.idle("Mandelbrot")

        # clear canvas
        #self.view.canvas.rectangle((0,0), (width,height), self.view.canvas.BLACK)

        for count in range(steps):

            # check for events
            events = self.view.canvas.get_events()
            if events != None:
                return events

            # calculate point
            point = (random.randrange(self.view.canvas.width),
                     random.randrange(self.view.canvas.height))
            c = (min(self.view.x) + self.view.size_x() * (point[0] / self.view.canvas.width),
                 min(self.view.y) + self.view.size_y() * (point[1] / self.view.canvas.height))

            # calculate color for point
            constant = c
            if self._juliamode:
                constant = (self._julia[0], self._julia[1])
            colorindex = self.calc_color(c, constant)

            # draw to canvas
            # Update every update_after steps
            update_after = 1000
            # refining_speed: Lower values make the picture stay
            # coarse, higher values make it too long to get
            # finer. Values between 500 and 1000 are good.
            refining_speed = 750
            # How much should the squares be shrinked in the beginning?
            initial_shrink_f = 10
            self.view.canvas.shrunken_square(
                point, min(self.view.canvas.width, self.view.canvas.height),
                count / refining_speed + initial_shrink_f,
                color=self._colortable[colorindex]
            )
            if count % update_after == 0:
                self.view.canvas.update()
        self.paused = True

    def idle(self, title):
        "Commit surface, set window title, and idle until next event."
        self.view.canvas.update()
        self.view.canvas.set_title(title)
        while True:
            events = self.view.canvas.get_events()
            if events != None:
                return events
            pygame.display.update()
            pygame.time.Clock().tick(60)
