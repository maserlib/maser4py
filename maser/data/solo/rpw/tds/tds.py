#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
SolO/RPW/Tds MASER main module.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)

__all__ = ["TdsException"]

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = "X.Bonnin"
__date__ = "2016-10-15"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = "MASER"
__institute__ = "LESIA, Obs.Paris, CNRS"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)
class TdsException(Exception):
    pass


# ________________ Global Functions __________
# (If required, define here gobal functions)
def main():
    """Main program."""
    print("maser.data.solo.rpw.tds module")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
