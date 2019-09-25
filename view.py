from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class View:
    "Represents the view and manages it's coordinates."

    def __init__(self, canvas, x=(-2,2), y=(-2,2)):
        self.canvas = canvas
        self.x = x # corresponds to width
        self.y = y # corresponds to height

    def __str__(self):
        return "( x:({}, {}), y:({}, {}) )".format(
            min(self.x), max(self.x), min(self.y), max(self.y))

    def rectify(self):
        "Adjusts view to match canvas proportion."
        view_width = self.size_y() / self.canvas.height * self.canvas.width
        self.x = (self.middle_x() - view_width / 2,
                  self.middle_x() + view_width / 2)

    def size_x(self):
        "Width and height of view (not canvas!)."
        return max(self.x) - min(self.x)

    def size_y(self):
        "Width and height of view (not canvas!)."
        return max(self.y) - min(self.y)

    def middle_x(self):
        "Coordinates of center point."
        return min(self.x) + self.size_x() / 2

    def middle_y(self):
        "Coordinates of center point."
        return min(self.y) + self.size_y() / 2

    def zoom(self, factor=2, point=None):
        """Zoom in or out, depending on the factor.
        
        Values greater than 1 zoom in, values between 0 and 1 zoom
        out.

        """
        if point == None:
            point = (self.middle_x(), self.middle_y())
        if factor <= 0:
            return # do nothing. Same as factor=1
        new_size_x = self.size_x() / factor
        new_size_y = self.size_y() / factor
        print("View after zoom (factor={}): {} x {}"
              .format(factor, new_size_x, new_size_y))
        self.x = (point[0] - new_size_x / 2, point[0] + new_size_x / 2)
        self.y = (point[1] - new_size_y / 2, point[1] + new_size_y / 2)

    def move(self, direction=None, factor=0.25):
        """Move view a specific distance into one of four directions.
        
        The distance is a fraction of the view's width or height,
        depending on the direction of movement.

        """
        size_x = self.size_x()
        size_y = self.size_y()
        if direction == Direction.UP:
            self.y = (min(self.y) - size_y * factor, max(self.y) - size_y * factor)
        elif direction == Direction.DOWN:
            self.y = (min(self.y) + size_y * factor, max(self.y) + size_y * factor)
        elif direction == Direction.LEFT:
            self.x = (min(self.x) - size_x * factor, max(self.x) - size_x * factor)
        elif direction == Direction.RIGHT:
            self.x = (min(self.x) + size_x * factor, max(self.x) + size_x * factor)
