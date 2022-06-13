"""Use colors in terminal with ease."""

DefaultColors = {
    'white':   7,    # noqa: E241
    'black':   232,  # noqa: E241
    'grey':    244,  # noqa: E241
    'purple':  99,   # noqa: E241
    'orange':  208,  # noqa: E241
    'lime':    82,   # noqa: E241
    'banana':  226,  # noqa: E241
    'cyan':    50,   # noqa: E241
    'grass':   40,   # noqa: E241
    'red':     160,  # noqa: E241
    'green':   34,   # noqa: E241
    'blue':    33,   # noqa: E241
    'yellow':  220,  # noqa: E241
    'pink':    213,  # noqa: E241
    'magenta': 198,  # noqa: E241
    'lavanda': 141,  # noqa: E241
}


class Color:
    """Color class to handle terminal color with escape sequence."""

    def __init__(self, fg=None, bg=None):
        """
        Create new terminal color.

        fg/bg can be string - one of default colors
        fg/bg can be int - represents 0-256 ascii colorid
        fg/bg can be None - in this case fg/bg is not set
        bg also can be bool - then provided color becomes background only.
        """
        if isinstance(fg, str):
            if fg not in DefaultColors:
                raise ValueError(f'Unknown default color: "{fg}"')
            self.__fg = DefaultColors[fg]
        elif isinstance(fg, int) or fg is None:
            self.__fg = fg
        else:
            raise TypeError(f'Unknown type for Color foreground: {type(fg)}')

        if isinstance(bg, str):
            if bg not in DefaultColors:
                raise ValueError(f'Unknown default color: "{bg}"')
            self.__bg = DefaultColors[bg]
        elif isinstance(bg, bool):
            self.__fg, self.__bg = None, self.__fg
        elif isinstance(bg, int) or bg is None:
            self.__bg = bg
        else:
            raise TypeError(f'Unknown type for Color background: {type(bg)}')

    def __wrap(self):
        """Wrap colorid with escape sequence."""
        fgw = f'38;5;{self.__fg}' if self.__fg is not None else None
        bgw = f'48;5;{self.__bg}' if self.__bg is not None else None
        if fgw is not None and bgw is not None:
            return f'[{fgw};{bgw}m'
        elif fgw is not None:
            return f'[{fgw}m'
        elif bgw is not None:
            return f'[{bgw}m'
        return ''

    def __str__(self):
        """To use color as terminal color."""
        res = self.__wrap()
        return '\x1b' + res if res else res

    def __repr__(self):
        """Print color to console without actually applying it."""
        res = self.__wrap()
        return '\\x1b' + res if res else '<No color>'

    def __add__(self, oth):
        """Fill unused fg/bg in each color if possible, second color overwrites first."""
        if isinstance(oth, str):
            return str(self) + oth
        if not isinstance(oth, Color):
            raise TypeError(f'Cannot combine color and {type(oth)}')
        fg = oth.__fg if oth.__fg is not None else self.__fg
        bg = oth.__bg if oth.__bg is not None else self.__bg
        return Color(fg, bg)

    def __radd__(self, oth):
        """Fill unused fg/bg in each color if possible, first color overwrites second."""
        if isinstance(oth, str):
            return oth + str(self)
        if not isinstance(oth, Color):
            raise TypeError(f'Cannot combine color and {type(oth)}')
        fg = self.__fg if self.__fg is not None else oth.__fg
        bg = self.__bg if self.__bg is not None else oth.__bg
        return Color(fg, bg)

    def __invert__(self):
        """Flip bg and fg of Color."""
        return Color(self.__bg, self.__fg)


class ColorMetaClass:
    """Class for .bg attr in Color."""

    pass


Color.bg = ColorMetaClass
for name, cid in DefaultColors.items():
    setattr(Color, name, Color(cid))
    setattr(Color.bg, name, Color(bg=cid))
Color.reset = '\x1b[0m'
