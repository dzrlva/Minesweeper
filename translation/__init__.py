import gettext
translation = gettext.translation('messages', 'translation', fallback=True)
_, ngettext = translation.gettext, translation.ngettext
