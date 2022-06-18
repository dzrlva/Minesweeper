#!/usr/bin/env python3
"""Do some good things."""

import glob


def task_html():
    """Make HTML documentation."""
    return {
        "actions": ["sphinx-build -M html docs docs/_build"],
        "file_dep": glob.glob("*py") + glob.glob("*rst"),
        "targets": ["_build"],
        "clean": True,
    }


def task_test():
    """Test Module."""
    return {
            'actions': ['python3 -m unittest discover tests']
           }


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o messages.pot minesweeper'],
            'file_dep': glob.glob('minesweeper/*.py') + glob.glob('minesweeper/*/*.py'),
            'targets': ['messages.pot'],
           }

def task_init_po():
    """Init translations."""
    return {
            'actions': ['pybabel init -D messages -d minesweeper/translation -i messages.pot -l ru'],
            'file_dep': ['messages.pot'],
           }

def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D messages -d minesweeper/translation -i messages.pot'],
            'file_dep': ['messages.pot'],
            'targets': ['minesweeper/translation/ru/LC_MESSAGES/messages.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': ['pybabel compile -D messages -l ru -i minesweeper/translation/ru/LC_MESSAGES/messages.po -d minesweeper/translation'],
            'file_dep': ['minesweeper/translation/ru/LC_MESSAGES/messages.po'],
            'targets': ['minesweeper/translation/ru/LC_MESSAGES/messages.mo'],
           }

