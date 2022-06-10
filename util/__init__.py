from PIL import ImageTk, Image
from .coord import Coord
from .point import Point


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def loadImage(imgPath, attrs={}):
    if attrs[ 'size' ] is None:
        return ImageTk.PhotoImage(Image.open(imgPath))
    if isinstance(attrs['size'], int):
        size = (attrs['size'], attrs['size'])
    return ImageTk.PhotoImage(Image.open(imgPath).resize(size))
