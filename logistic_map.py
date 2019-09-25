import fractal
import math
import view

class LogisticMap(fractal.Fractal):
    "Represents the bifurcation diagram of the logistic map."

    def __init__(self, canvas, depth=None, allowed_keyevents=[],
                 color=False):
        if depth == None:
            depth = 10 * canvas.height
        self.paused = False
        # set parameters
        self._depth = depth
        self.color = color
        # make view
        self.view = view.View(canvas, x=(3.5,4.0), y=(0,1))
        self.allowed_keyevents = allowed_keyevents
        self.set_title(rendering=False)

    def set_title(self, rendering=False):
        "Sets the window title, indicating if rendering is in process."
        if rendering:
            self.view.canvas.set_title("Logistic Map (rendering)")
        else:
            self.view.canvas.set_title("Logistic Map")

    def render(self):
        "Render the logistic map"

        # update window title
        self.set_title(rendering=True)

        # idle if paused
        if self.paused:
            return self.idle()

        for column in range(self.view.canvas.width):

            # check for events
            events = self.get_keyevents()
            if events != None:
                return events

            # calculate x
            column_width = self.view.size_x() / self.view.canvas.width
            r = min(self.view.x) + column * column_width

            # calculate column
            x = 0.5
            col = [0] * self.view.canvas.height
            for d in range(self._depth):
                x = r * x * (1 - x)
                row = math.floor((max(self.view.y) - x) / self.view.size_y() * self.view.canvas.height)
                if row >= 0 and row < len(col):
                    col[row] += 1

            # calculate color
            max_value = max(col)
            for row in range(len(col)):
                val = col[row] / max_value

                if self.color:
                    color = (
                        math.floor(max(0, math.sin(1.5 * math.pi * val                 )) * 255), # red
                        math.floor(max(0, math.sin(1.5 * math.pi * val - 0.25 * math.pi)) * 255), # green
                        math.floor(max(0, math.sin(1.5 * math.pi * val - 0.5  * math.pi)) * 255), # blue
                    )
                else:
                    color = ((1 - val) * 255,
                             (1 - val) * 255,
                             (1 - val) * 255)

                # draw pixel
                self.view.canvas.pixel((column, row), color=color)

                # Update every update_after steps
                update_after = 1000
                if (column * self.view.canvas.height + row) % update_after == 0:
                    self.view.canvas.update()

        self.view.canvas.update()
        return self.idle()
