#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autofill module for the xlsx2skt program.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import argparse
from datetime import datetime
import subprocess
import shutil

from .xlsx2skt import parse_xlsx

# ________________ HEADER _________________________

# Mandatory
__version__ = "1.0.0"
__author__ = "Xavier Bonnin"
__date__ = "16-JUL-2015"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__institute__ = "LESIA, Observatoire de Paris"
__project__ = "RPW Operation Centre (ROC)"

# ________________ Global Variables _____________

# ________________ Class Definition __________

# ________________ Global Functions __________


def fill_vattrs(xlsx_file, conf_file):

    """
        Function to help variable attributes completion
        in a given xlsx file (list of zvariables must be provided)
    """

    xlsx_data = parse_xlsx(xlsx_file)





# _________________ Main ____________________________
if __name__ == "__main__":
    main()