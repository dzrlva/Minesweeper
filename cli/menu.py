"""Menu module for cli app."""

from cli.screen import Screen, Color
from blessed import Terminal
from cli.app import App as CLIAPP
from cli.box import Box
from util import Point
from logic.field import Field
from logic.gamestat import Stat


KEYS = {
    "up": "w",
    "down": "s",
    "open": " ",
}
OFFSET = 2  # head of menu

screen = Screen()
stat = Stat()

if __name__ == '__main__':
    stat.assignFile("Gamer1")
    stat.readStatistic()


class Menu:
    """Cli menu baseclass."""

    def __init__(self, item_numb, items, field):
        """Create abstract menu."""
        self.oldPos = None
        self.pos = Point(0, 0)
        self.box = Box(field.width + 1, field.height + 1, "soft")
        self.redraw = True
        self.fullredraw = True
        self.item_numb = item_numb
        self.items = items
        self.field = field

    def draw(self):
        """Draw menu."""
        if self.fullredraw:
            self.fullredraw = False
            self.redraw = True
            self.box.draw([0, 0])
        if self.redraw:
            self.redraw = False
        self.drawCursor([1, 1 + OFFSET])
        screen[2, 1, Color.white].print('Hello, Gamer1!')
        for i, j in zip(self.items, range(2, len(self.items) + OFFSET)):
            screen[2, 1 + j, Color.white].print(i)

    def drawCursor(self, offset):
        """Draw cursor in current position."""
        offset = Point(offset)
        screen.drawPixel(self.pos + offset, ">", Color.white)
        if self.oldPos is not None:
            screen.drawPixel(self.oldPos + offset, " ", Color.white)

    def move(self, direct):
        """Move cursor at certain direction."""
        if self.pos.y + direct.y >= 0 and self.pos.y + direct.y < self.item_numb:
            self.oldPos = Point(self.pos.x, self.pos.y)
            self.pos += direct


class Startmenu(Menu):
    """Start menu for cli app."""

    def __init__(self, item_numb, items, field):
        """Init startmenu."""
        Menu.__init__(self, item_numb, items, field)

    def keyAction(self, key):
        """React to key press."""
        if key == KEYS["up"]:
            self.move(Point(0, -1))
        elif key == KEYS["down"]:
            self.move(Point(0, 1))
        elif key == KEYS["open"]:
            if self.pos.y == 0:
                CLIAPP().mainloop()
                exit()
            elif self.pos.y == 1:
                stat.print()
            elif self.pos.y == 2:
                # settingsmenu()
                pass
            elif self.pos.y == 3:
                exit()


def startmenu():
    """Crete startmenu."""
    startmenu_item = ["Game", "Statistics", "Settings", "Exit"]
    term = Terminal()
    field = Field(30, len(startmenu_item) + OFFSET, 0.15)
    startmenu = Startmenu(4, startmenu_item, field)

    with term.cbreak(), term.hidden_cursor():
        screen.clear()
        startmenu.draw()
        key = ""

        while key != "q":
            key = term.inkey(timeout=3)
            if not key:
                continue
            startmenu.keyAction(key)
            startmenu.draw()
