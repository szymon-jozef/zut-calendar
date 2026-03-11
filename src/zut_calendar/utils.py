def get_locale_thing():
    import os
    import gettext
    current_dir = os.path.abspath(os.path.dirname(__file__))
    localedir = os.path.join(current_dir, 'locales')
    t = gettext.translation('zut_calendar', localedir=localedir, fallback=True)
    _ = t.gettext
    return _
