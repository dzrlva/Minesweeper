"""Get text translation."""

import gettext
from minesweeper.util import Config
import minesweeper.resources as resources


def _(string):
    global _ru
    if LANGUAGE == "Russian":
        return _ru(string)
    return string


def setLang(language):
    """Set current translation language."""
    global LANGUAGE
    LANGUAGE = language


if "LANGUAGE" not in globals():
    LANGUAGE = Config.get()["language"]
    ruTrans = gettext.translation(
        "messages", resources.translation, languages=("ru",)
    )
    _ru = ruTrans.gettext
