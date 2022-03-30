from .screen import Screen
from util.coord import Coord

SIDES = {
    'light':      { 'hor': '─', 'ver': '│' },
    'bold':       { 'hor': '━', 'ver': '┃' },
    'dashed':     { 'hor': '┄', 'ver': '┆' },
    'dashedbold': { 'hor': '┅', 'ver': '┇' },
    'double':     { 'hor': '═', 'ver': '║' },
}

CORNERS = {
    'light':  { 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘' },
    'round':  { 'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯' },
    'bold':   { 'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛' },
    'double': { 'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝' },
}

screen = Screen()


class Box:
    styles = {
        'sharp':       ['light', 'light'],
        'soft':        ['light', 'round'],
        'double':      ['double', 'double'],
        'dashed':      ['dashed', 'light'],
        'soft dashed': ['dashed', 'round'],
        'bold dashed': ['dashed', 'bold'],
    }

    def __init__(self, width, height, style='sharp'):
        self.width, self.height = width, height
        self.setStyle(style)

    def setStyle(self, style):
        if style not in Box.styles:
            raise ValueError(f'Unknown Box style: {style}')
        sides, corners = Box.styles[style]
        self.sides = SIDES[sides]
        self.corners = CORNERS[corners]

    def draw(self, topleft=Coord(0, 0)):
        topleft = Coord(topleft)
        botleft = [0, self.height] + topleft
        botright = [self.width, self.height] + topleft
        topright = [self.width, 0] + topleft

        for x in range(1, self.width):
            screen.drawPixel([x, 0] + topleft, self.sides['hor'])
            screen.drawPixel([x, 0] + botleft, self.sides['hor'])
        for y in range(1, self.height):
            screen.drawPixel([0, y] + topleft, self.sides['ver'])
            screen.drawPixel([0, y] + topright, self.sides['ver'])
        screen.drawPixel(topleft, self.corners['tl'])
        screen.drawPixel(topright, self.corners['tr'])
        screen.drawPixel(botleft, self.corners['bl'])
        screen.drawPixel(botright, self.corners['br'])
