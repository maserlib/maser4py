#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Global constants for the package."""

import os
from importlib import metadata


__all__ = ["ROOT_DIRECTORY", "MASER_LIB_DIR", "SUPPORT_DIR", "__version__"]

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

MASER_LIB_DIR = os.path.dirname(__file__)
SUPPORT_DIR = os.path.join(MASER_LIB_DIR, "support")
__version__ = metadata.version(__package__.replace(".", "-"))
