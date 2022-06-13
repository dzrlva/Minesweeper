"""Module with common used utils."""

from PIL import ImageTk, Image
from .coord import Coord
from .point import Point  # noqa: F401
from os.path import exists
import configparser

CONFIG_FILE = 'config.ini'


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


class Config:
    """Wrap around configparser."""

    file = None

    @staticmethod
    def load():
        """Load config file, generate default if current dosen't exist."""
        if not exists(CONFIG_FILE):
            Config.createDefault()
        Config.file = configparser.ConfigParser()
        Config.file.read(CONFIG_FILE)

    @staticmethod
    def save(value, field='settings'):
        """Save config file."""
        if Config.file is None:
            Config.load()
        Config.file[field] = value
        with open(CONFIG_FILE, 'w') as configFile:
            Config.file.write(configFile)

    @staticmethod
    def get(field='settings'):
        """Get config values and load config if needed."""
        if Config.file is None:
            Config.load()
        return Config.file[field]

    @staticmethod
    def createDefault():
        """Create defautl config file."""
        with open(CONFIG_FILE, 'w') as configFile:
            configFile.write(
                "[settings]\n"
                "resolution = 700x600\n"
                "colorscheme = octopus\n"
                "language = English\n"
                "fullscreen = False\n"
            )
