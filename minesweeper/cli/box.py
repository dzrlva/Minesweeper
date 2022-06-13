"""Draw different boxes with ease."""
from .screen import Screen
from minesweeper.util.point import Point

SIDES = {
    "light": {"hor": "─", "ver": "│"},
    "bold": {"hor": "━", "ver": "┃"},
    "dashed": {"hor": "┄", "ver": "┆"},
    "dashedbold": {"hor": "┅", "ver": "┇"},
    "double": {"hor": "═", "ver": "║"},
}

CORNERS = {
    "light": {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘"},
    "round": {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯"},
    "bold": {"tl": "┏", "tr": "┓", "bl": "┗", "br": "┛"},
    "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝"},
}

screen = Screen()


class Box:
    """Box class to create boxes in terminal."""

    styles = {
        "sharp": ["light", "light"],
        "soft": ["light", "round"],
        "double": ["double", "double"],
        "dashed": ["dashed", "light"],
        "soft dashed": ["dashed", "round"],
        "bold dashed": ["dashed", "bold"],
    }

    def __init__(self, width, height, style="sharp", color=None):
        """Init box with width and height, one of N styles and color."""
        self.width, self.height = width, height
        self.style = style
        self.color = color

    @property
    def style(self):
        """Get current style."""
        return self.__style

    @style.setter
    def style(self, style):
        """Set one of N styles."""
        if style not in Box.styles:
            raise ValueError(f"Unknown Box style: {style}")
        self.__style = style
        sides, corners = Box.styles[style]
        self.sides = SIDES[sides]
        self.corners = CORNERS[corners]

    def draw(self, topleft=Point(0, 0)):
        """Draw the box at some coordinates."""
        topleft = Point(topleft)
        botleft = [0, self.height] + topleft
        botright = [self.width, self.height] + topleft
        topright = [self.width, 0] + topleft

        for x in range(1, self.width):
            screen.drawPixel([x, 0] + topleft, self.sides["hor"], self.color)
            screen.drawPixel([x, 0] + botleft, self.sides["hor"], self.color)
        for y in range(1, self.height):
            screen.drawPixel([0, y] + topleft, self.sides["ver"], self.color)
            screen.drawPixel([0, y] + topright, self.sides["ver"], self.color)
        screen.drawPixel(topleft, self.corners["tl"], self.color)
        screen.drawPixel(topright, self.corners["tr"], self.color)
        screen.drawPixel(botleft, self.corners["bl"], self.color)
        screen.drawPixel(botright, self.corners["br"], self.color)
