import math
import pygame
import random


class Fractal():
    """Represents a generic fractal with universal parameters and a rendering function.
    
    This class shall not be instantiated directly.
    The class deriving from Fractal must define the following
    functions: set_title, calc_point

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

            # calculate point
            pix = (random.randrange(self.view.canvas.width),
                   random.randrange(self.view.canvas.height))
            pos = (min(self.view.x) + self.view.size_x() * (pix[0] / self.view.canvas.width),
                   min(self.view.y) + self.view.size_y() * (pix[1] / self.view.canvas.height))

            # calculate color for point
            colorindex = self.calc_point(pos)

            # draw to canvas
            # Update every update_after steps
            update_after = 1000
            # refining_speed: Lower values make the picture stay
            # coarse, higher values make it too long to get
            # finer. Values between 500 and 1000 are good.
            refining_speed = 750
            # How much should the squares be shrinked in the beginning?
            initial_shrink_f = 10
            self.view.canvas.shrunken_square(
                pix, min(self.view.canvas.width, self.view.canvas.height),
                count / refining_speed + initial_shrink_f,
                color=self._colortable[colorindex]
            )
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
