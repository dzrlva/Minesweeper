"""Styles for gui app."""

from .colors import COLORS


def COMMON_STYLE():
    """Text and background colors."""
    return {
        "fg": COLORS["text"],
        "bg": COLORS["main"],
    }


def COMMON_BUTTON_STYLE():
    """Remove button border styles."""
    return {
        "borderwidth": 0,
        "highlightthickness": 0,
    }


def OPTION_MENU_STYLE():
    """OPTION button styles."""
    return {
        "bg": COLORS["buttons.bg"],
        "fg": COLORS["buttons.fg"],
        "activebackground": COLORS["buttons.hover-bg"],
        "activeforeground": COLORS["buttons.hover-text"],
    }


def RADIO_BUTTON_STYLE():
    """Radio button styles."""
    return (
        COMMON_STYLE()
        | COMMON_BUTTON_STYLE()
        | {
            "activeforeground": COLORS["text"],
            "activebackground": COLORS["main"],
            "selectcolor": COLORS["buttons.dot"],
        }
    )


def PUSH_BTTON_STYLE():
    """Regular button styles."""
    return (
        COMMON_STYLE()
        | COMMON_BUTTON_STYLE()
        | {
            "bg": COLORS["buttons.bg"],
            "fg": COLORS["buttons.fg"],
            "activebackground": COLORS["buttons.hover-bg"],
            "activeforeground": COLORS["buttons.hover-text"],
        }
    )
