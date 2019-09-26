import fractal
import math
import random
import view

class LogisticMap(fractal.Fractal):
    "Represents the bifurcation diagram of the logistic map."

    def __init__(self, canvas, depth=1, allowed_keyevents=[],
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

    def set_depth(self, depth):
        "Set new depth to DEPTH or to 1, if DEPTH is smaller than 1."
        self._depth = max(1, depth)
        self.generate_colortable()

    def render(self):
        "Render the logistic map"

        # update window title
        self.set_title(rendering=True)

        # idle if paused
        if self.paused:
            return self.idle()

        # calculate maximum bar_width
        max_bar_width = 1
        while max_bar_width < self.view.canvas.width:
            max_bar_width *= 2

        # decrease bar width over time
        bar_width = max_bar_width
        count = 0
        while bar_width > 1:
            bar_width /= 2

            # draw bars
            for col_num in range(int(self.view.canvas.width // bar_width + 1)):

                # check for events
                events = self.get_keyevents()
                if events != None:
                    return events

                # choose column
                column = int(bar_width * col_num)

                # skip column if already calculated
                skip_width = 2 * bar_width
                skip = False
                while skip_width < self.view.canvas.width:
                    if column % skip_width == 0:
                        skip = True
                        break
                    skip_width *= 2
                if skip:
                    continue

                # calculate column position in view
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

                        # draw line
                        self.view.canvas.rectangle(
                            (math.floor(column), row),
                            (math.floor(column+bar_width), row+1), color=color)

                # Update every update_after steps
                update_after = 50
                if count % update_after == 0:
                    self.view.canvas.update()
                count += 1

            # update every time the whole canvas has been filled with bars
            self.view.canvas.update()

        return self.idle()
