from PIL import ImageTk, Image
from .coordBase import Coord as CoordBase


class Point(CoordBase):
    def __init__(self, x, y=None):
        super.__init__(x, y, dtype=int)


class Coord(CoordBase):
    def __init__(self, x, y=None):
        super.__init__(x, y, dtype=float)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def loadImage(imgPath, size=None):
    if size is None:
        return ImageTk.PhotoImage(Image.open(imgPath))
    if isinstance(size, int):
        size = (size, size)
    return ImageTk.PhotoImage(Image.open(imgPath).resize(size))
