from .colors import COLORS


def COMMON_STYLE():
    return {
        'fg': COLORS['text'],
        'bg': COLORS['main'],
    }


def COMMON_BUTTON_STYLE():
    return {
        'borderwidth': 0,
        'highlightthickness': 0,
    }


def RADIO_BUTTON_STYLE():
    return COMMON_STYLE() | COMMON_BUTTON_STYLE() | {
        'activeforeground': COLORS['text'],
        'activebackground': COLORS['main'],
        'selectcolor': COLORS['buttons.dot'],
    }


def PUSH_BTTON_STYLE():
    return COMMON_STYLE() | COMMON_BUTTON_STYLE() | {
        'bg': COLORS['buttons.bg'],
        'fg': COLORS['buttons.fg'],
        'activebackground': COLORS['buttons.hover-bg'],
        'activeforeground': COLORS['buttons.hover-text']
    }
