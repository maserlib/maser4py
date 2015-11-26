#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""maser main settings module"""

import os

settings_dir = os.path.dirname(os.path.realpath(__file__))

logconf = os.path.join(settings_dir, "..", "config", "logging.conf")
