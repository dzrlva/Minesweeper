from PIL import ImageTk, Image
from .coord import Coord
from .point import Point


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def loadImage(attrs, scale):
    path = attrs['path']
    size = Coord(attrs['size'] * scale, dtype=int)

    image = Image.open(path)
    ext = path.split('.')[-1]

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
