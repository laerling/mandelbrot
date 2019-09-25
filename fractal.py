import math
import pygame
import random


class Fractal():
    """Represents a generic fractal with universal parameters and a rendering function.
    
    This class shall not be instantiated directly.
    The class deriving from Fractal must define the functions
    set_title and calc_point or overwrite the render function.

    """

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

    def set_depth(self, depth):
        """Set new depth to DEPTH or to 2, if DEPTH is smaller than 2.
        
        DEPTH must not be smaller than 2, because the mandelbrot
        algorithm divides by (depth - 1).

        """
        self._depth = max(2, depth)
        self.generate_colortable()

    def get_keyevents(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT \
            or e.type == pygame.KEYDOWN \
            and e.key in self.allowed_keyevents:
                return events

    def toggle_pause(self):
        "Pause or unpause the rendering process."
        self.paused = not self.paused

    def render(self, steps=500_000):
        "Render the fractal."

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

            # draw square
            self.view.square(point, self._colortable[colorindex],
                             size=size)

            # Update every update_after steps
            update_after = 1000
            if count % update_after == 0:
                self.view.canvas.update()

        return self.idle()

    def idle(self):
        "Commit surface, set window title, and idle until next event."
        self.paused = True
        self.view.canvas.update()
        self.set_title(rendering=False)
        while True:
            events = self.get_keyevents()
            if events != None:
                return events
            pygame.display.update()
            pygame.time.Clock().tick(60)
