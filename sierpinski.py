import fractal
import random
import view
import canvas


class Sierpinski(fractal.Fractal):
    "Represents the mandelbrot set."

    def __init__(self, canvas, depth=500_000, allowed_keyevents=[]):
        self.paused = False
        self._depth = depth
        # make view
        self.view = view.View(canvas, x=(0,1), y=(0,1))
        self.allowed_keyevents = allowed_keyevents
        self.set_title(rendering=False)

    def set_title(self, rendering=False):
        "Sets the window title, indicating if rendering is in process."
        if rendering:
            self.view.canvas.set_title("Sierpinski (rendering)")
        else:
            self.view.canvas.set_title("Sierpinski")

    def render(self):
        """Render the sierpinski triangle.
        
        The difference between Fractal.render and Sierpinski.render
        is, that the latter does not calculate a set of points that
        don't escape to infinity, but just iterates one single point.

        """

        # update window title
        self.set_title(rendering=True)

        # idle if paused
        if self.paused:
            return self.idle()

        # draw background
        self.view.canvas.rectangle((0,0), (self.view.canvas.width,
                                           self.view.canvas.height),
                                   color=canvas.WHITE)
        point = (0,0)
        for count in range(self._depth):

            # check for events
            events = self.get_keyevents()
            if events != None:
                return events

            # choose attracting point
            attractors = [(0,0), (1,0), (0.5,1)]
            attractor = attractors[random.randrange(len(attractors))]

            # move point towards attractor
            point = (point[0]+0.5*(attractor[0]-point[0]),
                     point[1]+0.5*(attractor[1]-point[1]))

            # draw pixel
            self.view.canvas.pixel(self.view.point_to_pixel(point))

            # Update every update_after steps
            update_after = 10000
            if count % update_after == 0:
                self.view.canvas.update()

        self.view.canvas.update()
        return self.idle()
