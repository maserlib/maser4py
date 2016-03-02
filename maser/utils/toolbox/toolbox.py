#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Toolbox module for maser-py package
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging
import subprocess

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
DEF_INDENT = " " * 16

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)


def setup_logging(filename=None,
                  quiet=False, verbose=False, debug=False):

    """Method to set up logging"""

    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)-8s: %(message)s')
    elif verbose:
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)-8s: %(message)s')
    else:
        logging.basicConfig(level=logging.ERROR,
                            format='%(levelname)-8s: %(message)s')

    if quiet:
        logging.root.handlers[0].setLevel(logging.CRITICAL + 10)
    elif verbose:
        logging.root.handlers[0].setLevel(logging.INFO)
    elif debug:
        logging.root.handlers[0].setLevel(logging.DEBUG)
    else:
        logging.root.handlers[0].setLevel(logging.ERROR)

    if filename:
        fh = logging.FileHandler(filename, delay=True)
        fh.setFormatter(logging.Formatter('%(asctime)s %(name)-\
                        12s %(levelname)-8s %(funcName)-12s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'))
        if debug:
            fh.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)

        logging.root.addHandler(fh)


def run_command(cmd):

    """ run a command with subprocess"""

    logger = logging.getLogger(__name__)

    try:
        logger.info(" ".join(cmd))
        res = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    except TypeError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)
    except subprocess.TimeoutExpired as e:
        logger.error("TIME OUT EXPIRED:  %i SEC.", e.timeout)

    return res


def which(program, path="PATH"):

    """which function"""

    def is_exe(fpath):
        """is_exe function"""
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, __ = os.path.split(program)

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ[path].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def uniq(seq, not_none=False):

    """Get list of unique elements from an input sequence of list type"""

    seen = set()
    seen_add = seen.add
    if not_none:
        return [x for x in seq if not (x in seen or seen_add(x) or x is None)]
    else:
        return [x for x in seq if not (x in seen or seen_add(x))]


def quote(string, unquote=False):

    """Double quote a given string"""

    if string is not None:
        if not isinstance(string, str):
            string = str(string)
        if string.startswith("\""):
            string = string[1:]
        if string.endswith("\""):
            string = string[:-1]
        if unquote:
            return string
        return "\"" + string + "\""


def truncate_str(string, max_length,
                 gap=DEF_INDENT,
                 min_length=3):

    """ truncate a too long CDF_CHAR value"""

    nstr = len(string)
    new_string = ""
    for i, val_c in enumerate(string):
        if i > nstr - min_length:
            new_string += string[i:]
            break
        new_string += val_c
        if (i % max_length == 0) and (i != 0):
            new_string += "\" - \n" + gap + "\""

    return new_string


def insert_char(string, char, pos):

    """ Insert substring in a string """

    return string[:pos] + char + string[pos:]


# _________________ Main ____________________________
if __name__ == "__main__":
    print("tools for maser package")
