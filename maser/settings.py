#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""maser main settings module."""

import os

from maser.utils.toolbox import get_version

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

MASER_LIB_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MASER_LIB_DIR, "data")
SERVICE_DIR = os.path.join(MASER_LIB_DIR, "services")
UTILS_DIR = os.path.join(MASER_LIB_DIR, "utils")
SUPPORT_DIR = os.path.join(MASER_LIB_DIR, "support")

if os.path.isfile(os.path.join(ROOT_DIRECTORY, "CHANGELOG.md")):
    MASER_VERSION = get_version(os.path.join(ROOT_DIRECTORY, "CHANGELOG.md"))
elif os.path.isfile(os.path.join(ROOT_DIRECTORY, "..", "CHANGELOG.md")):
    MASER_VERSION = get_version(os.path.join(ROOT_DIRECTORY, "..", "CHANGELOG.md"))
else:
    print("WARNING: CHANGELOG.md not found or invalid, version unknown!")
    MASER_VERSION = "unknown"