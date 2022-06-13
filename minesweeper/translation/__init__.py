import gettext
import configparser
from minesweeper.util import Config


def getConfigLang():
    return Config.get()["language"]


def _(string):
    global _ru, _eng
    if LANGUAGE == "Russian":
        return _ru(string)
    return _eng(string)


def setLang(language):
    global LANGUAGE
    LANGUAGE = language


if "LANGUAGE" not in globals():
    LANGUAGE = getConfigLang()
    ruTrans = gettext.translation(
        "messages", "minesweeper/translation", languages=("ru",)
    )
    engTrans = gettext.translation("messages", "minesweeper/translation", fallback=True)
    _ru = ruTrans.gettext
    _eng = engTrans.gettext
