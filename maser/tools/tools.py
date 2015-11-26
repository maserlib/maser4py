#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools Python 3 module for maser-py package
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = ""
__date__ = ""

# Optional
__institute__ = ""
__project__ = ""
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__change__ = {"version": "change"}

# ________________ Global Variables _____________
# (define here the global variables)


# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)

def setup_logging(filename=None,
                  quiet=False, verbose=False, debug=False):

    """Method to set up logging"""

    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s: %(message)s')
    elif verbose:
        logging.basicConfig(level=logging.INFO, format='%(levelname)-8s: %(message)s')
    else:
        logging.basicConfig(level=logging.CRITICAL, format='%(levelname)-8s: %(message)s')

    if quiet:
        logging.root.handlers[0].setLevel(logging.CRITICAL + 10)
    elif verbose:
        logging.root.handlers[0].setLevel(logging.INFO)
    elif debug:
        logging.root.handlers[0].setLevel(logging.DEBUG)
    else:
        logging.root.handlers[0].setLevel(logging.CRITICAL)

    if filename:
        fh = logging.FileHandler(filename, delay=True)
        fh.setFormatter(logging.Formatter('%(asctime)s %(name)-\
                        12s %(levelname)-8s %(funcName)-12s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        if debug:
            fh.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)

        logging.root.addHandler(fh)


def which(program):

    """which function"""

    def is_exe(fpath):
        """is_exe function"""
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# _________________ Main ____________________________
if __name__ == "__main__":
    print("tools for maser package")
