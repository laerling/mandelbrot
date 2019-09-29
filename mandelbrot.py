import fractal
import random
import view


class Mandelbrot(fractal.Fractal):
    "Represents the mandelbrot set."

    def __init__(self, canvas, depth=100, color=True,
                 threshold=2, allowed_keyevents=[]):
        self.paused = False
        # set parameters
        self._depth = depth
        self.generate_colortable()
        self.threshold = threshold
        self.color = color
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

    def render(self, steps=500_000):
        """Render the mandelbrot.
        
        The difference between Fractal.render and Mandelbrot.render
        is, that the latter leverages mandelbrot's symmetry along the
        Y axis by calculating only two quadrants of the coordinate
        system and mirroring it to the other two quadrants. When two
        quadrants with different signage of Y are in view, this
        increases the percepted rendering speed twofold.

        """

        # update window title
        self.set_title(rendering=True)

        # idle if paused
        if self.paused:
            return self.idle()

        for count in range(steps):

            # check for events
            events = self.get_keyevents()
            if events != None:
                return events

            # choose point
            point = (min(self.view.x) + random.random() * self.view.size_x(),
                     min(self.view.y) + random.random() * self.view.size_y())

            # move point to 1st or 2nd quadrant
            point = (point[0], abs(point[1]))

            # calculate color
            colorindex = self.calc_point(point)

            # Lower values for shrinking_speed make the picture stay
            # coarse, higher values make it too long to get
            # finer. Values between 500 and 1000 are good.
            shrinking_speed = 750

            # square size
            max_size = min(self.view.canvas.width, self.view.canvas.height)
            scale = 1 / (count / shrinking_speed + 10)
            size = scale * max_size

            # choose color
            if self.color:
                color = self._colortable[colorindex]
            else:
                v = (colorindex / self._depth) * 255
                color = (v,v,v)

            # draw squares for y>=0 and y<=0
            for y_mul in range(-1,2,2):
                p = (point[0], point[1] * y_mul)
                self.view.square(p, color, size=size)

            # Update every update_after steps
            update_after = 1000
            if count % update_after == 0:
                self.view.canvas.update()

        self.view.canvas.update()
        return self.idle()
