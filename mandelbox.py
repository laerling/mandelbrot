import fractal
import random
import view


class Mandelbox(fractal.Fractal):
    "Represents the mandelbox set."

    def __init__(self, canvas, depth=100, scale=1.5, color=True,
                 threshold=2, allowed_keyevents=[]):
        self.paused = False
        # set parameters
        self._depth = depth
        self.generate_colortable()
        self.scale = scale
        self.threshold = threshold
        self.color = color
        # make view
        self.view = view.View(canvas, x=(-2,2), y=(-2,2))
        self.allowed_keyevents = allowed_keyevents
        self.set_title(rendering=False)

    def set_title(self, rendering=False):
        "Sets the window title, indicating if rendering is in process."
        if rendering:
            self.view.canvas.set_title("Mandelbox (rendering)")
        else:
            self.view.canvas.set_title("Mandelbox")

    def boxfold(self, point):
        "Applies the boxfold operation to POINT."
        x, y = point
        if x < -1:
            x = -2 - x
        elif x > 1:
            x = 2 - x
        if y < -1:
            y = -2 - y
        elif y > 1:
            y = 2 - y
        return (x,y)

    def ballfold(self, point):
        "Applies the ballfold operation to POINT."
        x, y = point
        magnitude = x**2 + y**2
        if magnitude < 0.25:
            x *= 4
            y *= 4
        elif magnitude < 1:
            x /= magnitude
            y /= magnitude
        return (x,y)

    def calc_point(self, point):
        "Calculate whether POINT is within the mandelbox set."
        constant = point
        for colortable_index in range(self._depth):
            # fold
            point = self.ballfold(self.boxfold(point))
            # scale
            point = (point[0] * self.scale,
                     point[1] * self.scale)
            # add constant
            point = (point[0] + constant[0],
                     point[1] + constant[1])
            # check for escape
            if point[0] > self.threshold \
            or point[1] > self.threshold:
                break
        return colortable_index

    def render(self, steps=500_000):
        """Render the mandelbox.
        
        The difference between Fractal.render and Mandelbox.render is,
        that the latter leverages mandelbox's perfect symmetry by
        calculating only one quadrant of the coordinate system and
        mirroring it to all other quadrants. If all four quadrants are
        in view, this increases the percepted rendering speed
        fourfold.

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

            # move point to negative quadrant
            point = (-abs(point[0]), -abs(point[1]))

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

            # draw squares into all four quadrants
            for y_mul in range(-1,2,2):
                for x_mul in range(-1,2,2):
                    p = (point[0] * x_mul, point[1] * y_mul)
                    self.view.square(p, color, size=size)

            # Update every update_after steps
            update_after = 1000
            if count % update_after == 0:
                self.view.canvas.update()

        self.view.canvas.update()
        return self.idle()
