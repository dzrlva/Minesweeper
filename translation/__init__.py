import gettext
import configparser

if 'translation' not in globals():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if config['settings']['language'] == 'Russian':
        translation = gettext.translation('messages', 'translation', languages=('ru',))
    else:
        translation = gettext.translation('messages', 'translation', fallback=True)
    _, ngettext = translation.gettext, translation.ngettext
