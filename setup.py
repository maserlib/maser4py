# -*- coding: utf-8 -*-

# we have to keep a (light version of the) setup.py because
# pyproject.toml is not supporting editable installs via pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='maser4py',
    packages=['maser'],
    package_dir={'': '.'},
    package_data={},
)
