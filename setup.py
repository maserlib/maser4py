# -*- coding: utf-8 -*-

# we have to keep a (light version of the) setup.py because
# pyproject.toml is not supporting editable installs via pip

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import toml

# the absolute path of this file
ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PYPROJECT_FILE = os.path.join(ROOT_DIRECTORY, 'pyproject.toml')
REQ_FILE = os.path.join(ROOT_DIRECTORY, 'requirements.txt')

# Load pyproject.toml metadata
metadata = toml.load(PYPROJECT_FILE)

def get_reqs(req_file):
    """Get module dependencies from requirements.txt."""
    if not os.path.isfile(req_file):
        raise BaseException('No requirements.txt file found, aborting!')
    else:
        with open(req_file, 'r') as fr:
            requirements = fr.read().splitlines()

    return requirements

setup(
    name=metadata['tool']['poetry']['name'],
    version=metadata['tool']['poetry']['version'],
    packages=['maser'],
    package_dir={'': '.'},
    package_data={},
    setup_requires=['toml'],
    install_requires=get_reqs(REQ_FILE),
    entry_points={
        'console_scripts': [
            'maser=maser.script:main']
    },
)
