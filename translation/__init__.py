import gettext
import configparser


def getConfigLang():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['settings']['language']


def _(string):
    global _ru, _eng
    if LANGUAGE == 'Russian':
        return _ru(string)
    return _eng(string)


def setLang(language):
    global LANGUAGE
    LANGUAGE = language


if 'LANGUAGE' not in globals():
    LANGUAGE = getConfigLang()
    ruTrans = gettext.translation('messages', 'translation', languages=('ru',))
    engTrans = gettext.translation('messages', 'translation', fallback=True)
    _ru = ruTrans.gettext
    _eng = engTrans.gettext
