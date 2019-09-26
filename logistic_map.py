import fractal
import math
import random
import view

class LogisticMap(fractal.Fractal):
    "Represents the bifurcation diagram of the logistic map."

    def __init__(self, canvas, depth=10, allowed_keyevents=[],
                 color=False):
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

        iterations = self.view.canvas.width * self._depth
        for col_iter in range(iterations):

            # check for events
            events = self.get_keyevents()
            if events != None:
                return events

            # choose column
            column = random.randrange(self.view.canvas.width)
            column_width = self.view.size_x() / self.view.canvas.width
            r = min(self.view.x) + column * column_width

            # calculate column
            x = 0.5
            col = [0] * self.view.canvas.height
            for d in range(self.view.canvas.height * self._depth):
                x = r * x * (1 - x)
                # for r > 4, x escapes to -inf
                if abs(x) > 100:
                    break
                row = math.floor((max(self.view.y) - x) /
                                 self.view.size_y() * self.view.canvas.height)
                if row >= 0 and row < len(col):
                    col[row] += 1

            # draw column
            max_value = max(1, max(col))
            for row in range(len(col)):

                # calculate color
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

                # line size
                max_size = self.view.canvas.width / 10
                speed = 30
                size = (abs(col_iter - iterations / 2) / (iterations / 2)) ** speed * (max_size - 0.5) + 0.5
                #size = max(0.5, (1 - (0.5 / iterations) ** 1.1) * (max_size - 0.5) + 0.5)

                # draw line
                self.view.canvas.rectangle(
                    (math.floor(column-size/2), row),
                    (math.floor(column+size/2), row+1), color=color)

                # Update every update_after steps
                update_after = 2000
                if (column * self.view.canvas.height + row) % update_after == 0:
                    self.view.canvas.update()

        self.view.canvas.update()
        return self.idle()
