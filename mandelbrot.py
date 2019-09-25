import fractal
import view


class Mandelbrot(fractal.Fractal):
    "Represents the mandelbrot set."

    def __init__(self, canvas, depth=100,
                 threshold=2, allowed_keyevents=[]):
        self.paused = False
        # set parameters
        self._depth = depth
        self.generate_colortable()
        self.threshold = threshold
        # make view
        self.view = view.View(canvas, x=(-2.1,0.9), y=(-1.1,1.1))
        self.allowed_keyevents = allowed_keyevents
        self.set_title(rendering=False)

    def set_title(self, rendering=False):
        "Sets the window title, indicating if rendering is in process."
        if rendering:
            self.view.canvas.set_title("Mandelbrot (rendering)")
        else:
            self.view.canvas.set_title("Mandelbrot")

    def calc_point(self, point):
        "Calculate whether POINT is within the mandelbrot set."
        constant = point
        for colortable_index in range(self._depth):
            point = ( point[0]**2 - point[1]**2 + constant[0],
                  2 * point[0] * point[1] + constant[1] )
            if point[0] > self.threshold or point[1] > self.threshold:
                break
        return colortable_index
