import fractal
import view

class Julia(fractal.Fractal):
    "Represents julia sets."

    def __init__(self, super, canvas, depth=100, constant=(0.7,0.3),
                 threshold=2, allowed_keyevents=[]):
        self.paused = False
        # set parameters
        self._depth = depth
        self.generate_colortable()
        self.threshold = threshold
        self.constant = constant
        # make view
        self.view = view.View(canvas, x=(-1.5,1.5), y=(-1.5,1.5))
        self.allowed_keyevents = allowed_keyevents
        self.set_title("Julia")
        # log
        self.print_constant()

    def set_title(self, rendering=False):
        "Sets the window title, indicating if rendering is in process."
        if rendering:
            self.view.canvas.set_title("Julia (rendering)")
        else:
            self.view.canvas.set_title("Julia")

    def calc_point(self, point):
        "Calculate whether POINT is within the julia set."
        for colortable_index in range(self._depth):
            point = ( point[0]**2 - point[1]**2 + self.constant[0],
                  2 * point[0] * point[1] + self.constant[1] )
            if point[0] > self.threshold or point[1] > self.threshold:
                break
        return colortable_index

    def print_constant(self):
        "Print julia constant."
        print("Julia constant: ({}, {})"
              .format(self.constant[0], self.constant[1]))

    def move_constant(self, direction=None, factor=0.01):
        """Move the julia constant around in the mandelbrot set.
        
        The distance of movement is a fraction of the view's width or
        height, depending on the direction of movement.

        """
        delta = (self.view.size_x() * factor,
                 self.view.size_y() * factor)
        if direction == view.Direction.UP:
            self.constant = (self.constant[0], self.constant[1] + delta[1])
        elif direction == view.Direction.DOWN:
            self.constant = (self.constant[0], self.constant[1] - delta[1])
        elif direction == view.Direction.LEFT:
            self.constant = (self.constant[0] - delta[0], self.constant[1])
        elif direction == view.Direction.RIGHT:
            self.constant = (self.constant[0] + delta[0], self.constant[1])
