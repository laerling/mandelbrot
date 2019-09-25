import pygame


BLACK = (0,0,0)
WHITE = (255,255,255)

class Canvas():
    """Represents a window with a certain WIDTH and HEIGHT.
    
    Wraps pygame and offers primitives for drawing in that area.
    If WIDTH or HEIGHT changes, don't change object members, but
    create a new Canvas object altogether.

    """

    def __init__(self, width, height):
        # init pygame
        pygame.init()
        self._game_display = pygame.display.set_mode((width,height))
        # init drawing surface
        self.width = width
        self.height = height
        self._sf = pygame.Surface((width, height))
        self.fill()

    def set_title(self, title):
        "Set the window title."
        pygame.display.set_caption(title)

    def update(self):
        "Update the display."
        self._game_display.blit(self._sf, (0,0))
        pygame.display.update()

    def pixel(self, pos, color=BLACK):
        "Color one pixel."
        self._sf.set_at(pos, color)

    def rectangle(self, pos_from, pos_to, color=BLACK):
        "Color a rectangle starting at POS_FROM and ending at POS_TO."
        rect = pygame.Rect(pos_from, (abs(pos_to[0] - pos_from[0]),
                                      abs(pos_to[1] - pos_from[1])))
        self._sf.fill(color, rect)

    def fill(self, color=WHITE):
        "Fill the entire canvas with one color."
        self._sf.fill(color)

    def square(self, pos, size, color=BLACK):
        "Color a square at POS with a size of SIZE x SIZE pixel."
        pos_from = (pos[0] - size / 2, pos[1] - size / 2)
        pos_to = (pos[0] + size / 2, pos[1] + size / 2)
        self.rectangle(pos_from, pos_to, color=color)
