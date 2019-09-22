import random
import math
import draw


class Frame:
    "Represents the view and manages it's coordinates."

    x = (-2, 1)
    y = (-1.5, 1.5)

    def __init__(self, x=x, y=y):
        self.x = x
        self.y = y

    def __str__(self):
        return "( x:({}, {}), y:({}, {}) )".format(
            min(self.x), max(self.x), min(self.y), max(self.y))

    def rectify(self, width, height):
        "Adjusts the view's width to a certain proportion."
        frame_width = self.size_y() / height * width
        self.x = (self.middle_x() - frame_width / 2,
                  self.middle_x() + frame_width / 2)

    def size_x(self):
        "Distance from left to right border"
        return max(self.x) - min(self.x)

    def size_y(self):
        "Distance from upper to lower border"
        return max(self.y) - min(self.y)

    def middle_x(self):
        "X coordinate of center point."
        return min(self.x) + self.size_x() / 2

    def middle_y(self):
        "Y coordinate of center point."
        return min(self.y) + self.size_y() / 2

    def zoom(self, factor=2, point=None):
        """Zoom in or out, depending on the factor.
        
        Values greater than 1 zoom in, values between 0 and 1 zoom
        out.

        """
        if point == None:
            point = (self.middle_x(), self.middle_y())
        new_size_x = self.size_x() / factor
        new_size_y = self.size_y() / factor
        self.x = (point[0] - new_size_x / 2, point[0] + new_size_x / 2)
        self.y = (point[1] - new_size_y / 2, point[1] + new_size_y / 2)

    def move(self, user_action=None, factor=0.25):
        """Move view a specific distance into one of four directions.
        
        The distance is a fraction of the view's width or height,
        depending on the direction of movement.

        """
        size_x = self.size_x()
        size_y = self.size_y()
        if user_action == draw.UserAction.MOVE_UP:
            self.y = (min(self.y) - size_y * factor, max(self.y) - size_y * factor)
        elif user_action == draw.UserAction.MOVE_DOWN:
            self.y = (min(self.y) + size_y * factor, max(self.y) + size_y * factor)
        elif user_action == draw.UserAction.MOVE_LEFT:
            self.x = (min(self.x) - size_x * factor, max(self.x) - size_x * factor)
        elif user_action == draw.UserAction.MOVE_RIGHT:
            self.x = (min(self.x) + size_x * factor, max(self.x) + size_x * factor)


class Mandelbrot:
    "Represents a mandelbrot set and all julia sets contained in it."

    _depth = 100
    _threshold = 10

    _julia = False
    _julia_x = 0.7
    _julia_y = 0.3

    _paused = False

    frame = Frame()

    def __init__(self, depth=_depth, threshold=_threshold, julia=_julia):
        self._depth = depth
        self._threshold = threshold
        self._julia = julia
        self._paused = False

    def get_depth(self):
        return self._depth;

    def set_depth(self, depth):
        """Set new depth to DEPTH or to 2, if DEPTH is smaller than 2.
        
        DEPTH must not be smaller than 2, because the mandelbrot algorithm divides by (depth - 1).
        """
        self._depth = max(2, depth)

    def toggle_julia(self):
        """Toggle between showing the mandelbrot set and a julia set.
        
        Chooses a random julia seed when switching to julia mode.

        """
        self._paused = False
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

    def is_julia(self):
        "Are we in julia mode? I. e., is a julia set displayed?"
        return self._julia

    def set_julia(self, julia):
        "Enter or leave julia mode."
        self._julia = julia

    def julia_move(self, user_action=None, factor=0.1):
        """Move the julia seed around in the mandelbrot set.
        
        The distance of movement is a fraction of the view's width or
        height, depending on the direction of movement.

        """
        delta_x = self.frame.size_x() * factor
        delta_y = self.frame.size_y() * factor
        if user_action == draw.UserAction.JULIA_MOVE_UP:
            self._julia_y += delta_y
        elif user_action == draw.UserAction.JULIA_MOVE_DOWN:
            self._julia_y -= delta_y
        elif user_action == draw.UserAction.JULIA_MOVE_LEFT:
            self._julia_x -= delta_x
        elif user_action == draw.UserAction.JULIA_MOVE_RIGHT:
            self._julia_x += delta_x

    def toggle_pause(self):
        "Pause or unpause the rendering process."
        self._paused = not self._paused

    def calc_point(self, point, constant):
        "Calculate if POINT is within the mandelbrot set or a specific julia set, depending on CONSTANT."
        for i in range(self._depth):
            point = ( point[0]**2 - point[1]**2 + constant[0],
                  2 * point[0] * point[1] + constant[1] )
            if point[0] > self._threshold or point[1] > self._threshold:
                break
        return i / (self._depth-1)

    def draw(self, width, height, steps=500_000):
        "Render the mandelbrot set or a julia set."

        # do nothing if paused
        if self._paused:
            return draw.idle()

        # clear canvas
        draw.rectangle((0,0), (width,height), draw.black)

        for count in range(steps):

            # check for user action
            user_action = draw.getUserAction()
            if user_action != None:
                return user_action

            # initialize variables for this round
            point = (random.randrange(width), random.randrange(height))
            c = (min(self.frame.x) + self.frame.size_x() * (point[0] / width),
                 min(self.frame.y) + self.frame.size_y() * (point[1] / height))

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
            # Update every update_after steps
            update_after = 1000
            # refining_speed: Lower values make the picture stay
            # coarse, higher values make it too long to get
            # finer. Values between 500 and 1000 are good.
            refining_speed = 750
            # How much should the squares be shrinked in the beginning?
            initial_shrink_f = 10
            draw.partial_square(point, min(width, height),
                                count / refining_speed + initial_shrink_f,
                                color=(r,g,b),
                                #color=(val*255,val*255,val*255), # black and white
                                update_display=(count % update_after == 0))
        self._paused = True
