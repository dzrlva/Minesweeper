"""Module with common used utils."""

from PIL import ImageTk, Image
from .coord import Coord
from .point import Point  # noqa: F401


class dotdict(dict):
    """dot.notation access to dictionary attributes."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __hash__(self):
        """Hash for dictionary."""
        hashRes = 0
        for k, v in self.items():
            try:
                hashRes += hash(k)
            except TypeError:
                pass
            try:
                hashRes += hash(v)
            except TypeError:
                pass
        return hashRes % 4294967295 - 2147483648


def loadImage(path, size):
    """Load image for GUI app."""
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
