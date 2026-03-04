#!/usr/bin/env nix-shell
#!nix-shell -i bash -p gettext

if [[ "$1" == "translate" ]]; then
    xgettext --language=Python --keyword=_ --output=zut_calendar.pot src/zut_calendar/*.py
    msgmerge -U src/zut_calendar/locales/pl/LC_MESSAGES/zut_calendar.po zut_calendar.pot
    rm zut_calendar.pot 
fi

if [[ "$1" == "gen" ]]; then
    msgfmt -o src/zut_calendar/locales/pl/LC_MESSAGES/zut_calendar.mo src/zut_calendar/locales/pl/LC_MESSAGES/zut_calendar.po
fi
