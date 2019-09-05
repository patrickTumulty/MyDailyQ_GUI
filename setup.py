"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['My Daily Q.py']
DATA_FILES = ['assignments.pkl', 'completed_assignments.pkl']
OPTIONS = {
    'iconfile':'MDQ_Logo.icns'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)