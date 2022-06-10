from PIL import ImageTk, Image
from .coord import Coord
from .point import Point


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def loadImage(path, size):
    image = Image.open(path)
    ext = path.split('.')[-1]
    size = Coord(size, size)

    if ext == 'gif':
        frames = []
        for i in range(image.n_frames):
            frames.append(ImageTk.PhotoImage(
                image.copy().resize(size).convert('RGBA')
            ))
            image.seek(i)
        return {
            'size': Coord(size),
            'count': image.n_frames,
            'delay': image.info['duration'],
            'frames': frames
        }
    return ImageTk.PhotoImage(image.resize(size))
