#!/usr/bin/env python3

import glob


def task_html():
    """Make HTML documentation"""
    return {
        "actions": ["sphinx-build -M html docs docs/_build"],
        "file_dep": glob.glob("*py") + glob.glob("*rst"),
        "targets": ["_build"],
        "clean": True,
    }


def task_test():
    """Test Module"""
    pass
