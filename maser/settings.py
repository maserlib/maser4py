#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""maser main settings module."""

import os

__all__ = ['ROOT_DIRECTORY',
           'MASER_VERSION',
           'MASER_LIB_DIR',
           'DATA_DIR',
           'SERVICE_DIR',
           'UTILS_DIR',
           'SUPPORT_DIR']

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

from maser.version import __version__
MASER_VERSION = __version__

MASER_LIB_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MASER_LIB_DIR, 'data')
SERVICE_DIR = os.path.join(MASER_LIB_DIR, 'services')
UTILS_DIR = os.path.join(MASER_LIB_DIR, 'utils')
SUPPORT_DIR = os.path.join(MASER_LIB_DIR, 'support')
