"""Get text translation."""

import gettext
from minesweeper.util import Config


def _(string):
    global _ru, _eng
    if LANGUAGE == "Russian":
        return _ru(string)
    return _eng(string)


def setLang(language):
    """Set current translation language."""
    global LANGUAGE
    LANGUAGE = language


if "LANGUAGE" not in globals():
    LANGUAGE = Config.get()["language"]
    ruTrans = gettext.translation(
        "messages", "minesweeper/translation", languages=("ru",)
    )
    engTrans = gettext.translation("messages", "minesweeper/translation", fallback=True)
    _ru = ruTrans.gettext
    _eng = engTrans.gettext
