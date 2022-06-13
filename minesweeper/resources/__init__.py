import os


def setResource(root, path):
    return os.path.join(root, *path.split('/'))


def setImage(path):
    global IMGPATH
    return setResource(IMGPATH, path)


PKGHOME = os.path.dirname(os.path.abspath(__file__ + f'{os.sep}..'))
RSCPATH = os.path.join(PKGHOME, 'resources')
TRSPATH = os.path.join(PKGHOME, 'translation')
IMGPATH = os.path.join(RSCPATH, 'images')

# General
appIcon = setImage('icon.png')
font = setResource(RSCPATH, 'fonts/Purisa_Bold.ttf')

# gui/board releated
flag = setImage('flag.png')
explosion = setImage('explosion1.gif')
bomb = setImage('bomb.png')

statFolder = setResource(PKGHOME, 'stat')

translation = setResource(PKGHOME, 'translation')

config = setResource(PKGHOME, 'config.ini')
