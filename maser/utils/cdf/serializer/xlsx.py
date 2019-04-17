#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""Skt2xlsx module

Program to convert an input CDF skeleton table file
into an Excel format file (xlsx).

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging
from collections import OrderedDict

from openpyxl import load_workbook

from maser.utils.toolbox import uniq
from maser.utils.cdf.serializer.exceptions import InvalidFile

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)

# ________________ Class Definition __________
# (If required, define here classes)
class Xlsx:

    def __init__(self):
        self.cdf_items = {}




# ________________ Global Functions __________




# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)