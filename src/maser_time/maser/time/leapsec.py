#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
leapsec.py.

Python module to load and handle the
NASA CDF LeapSecond table.


"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import logging
import argparse
from datetime import datetime

from ..toolbox.toolbox import setup_logging, download_data, print_exception

__all__ = ["Lstable"]

# ________________ HEADER _________________________

# Mandatory
__version__ = "0.2.0"
__author__ = "X.Bonnin"
__date__ = "2017-03-30"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = "MASER"
__institute__ = "LESIA"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

URL = "https://cdf.gsfc.nasa.gov/html/CDFLeapSeconds.txt"
ENVAR = "CDF_LEAPSECONDSTABLE"

LS_FILENAME = "CDFLeapSeconds.txt"

INPUT_DATE = "%Y-%m-%dT%H:%M:%S"

CURDIR = os.path.dirname(os.path.abspath(__file__))
LS_FILE_DEF_DIR = os.path.join(CURDIR,
                               "..", "..",
                                     "support", "data")
if not os.path.isdir(LS_FILE_DEF_DIR):
    os.makedirs(LS_FILE_DEF_DIR)
LS_FILE_DEF_PATH = os.path.join(LS_FILE_DEF_DIR, LS_FILENAME)

# ________________ Class Definition __________
# (If required, define here classes)


class LstableException(Exception):
    pass


class Lstable:
    """Class for the leapsec table."""

    def __init__(self, file=None):
        """Leapsec __init__ method."""
        self.file = None
        self.date = []
        self.leapsec = []
        self.drift = []
        self.lstable = None

        # Setting the CDFLeapSeconds.txt filepath
        # and loading table
        self.set_file(file=file, reload=True)

    def _add(self, row):
        """Add a new set of data to the leapsec table."""
        fields = row.split()
        if len(fields) != 6:
            logger.error("Input row is not valid!")
            return

        date = datetime(int(fields[0]),
                        int(fields[1]),
                        int(fields[2]))
        self.date.append(date)
        self.leapsec.append(float(fields[3]))
        self.drift.append([float(fields[4]), float(fields[5])])

    def get_leapsec(self, date=datetime.now()):
        """Return the leapseconds for a given datetime."""
        if self.lstable is None:
            self.load_lstable()

        if date < self.date[0]:
            return 0.0
        elif date >= self.date[-1]:
            return self.leapsec[-1]
        else:
            for i, lsdate in enumerate(self.date[:-1]):
                if date >= lsdate and date < self.date[i + 1]:
                    return self.leapsec[i]

        return None

    @staticmethod
    def get_lstable_file(target_dir=None, overwrite=False,
                         url=URL):
        """Download the CDFLeapSeconds.txt leapsec table file into the target_dir.

        If target_dir is None and the $CDF_LEAPSECONDSTABLE env. variable
        is defined, then the file is saved into $CDF_LEAPSECONDSTABLE path.
        If target_dir is None and the $CDF_LEAPSECONDSTABLE env. variable
        is not defined, then file is copied in LS_FILE_DEF_PATH default path.

        Default file url is https://cdf.gsfc.nasa.gov/html/CDFLeapSeconds.txt.
        However, it can be changed using the url input keyword.

        overwrite input keyword allows program to replace existing file
        """
        if target_dir is None and ENVAR in os.environ:
            target_filepath = os.environ[ENVAR]
        elif target_dir is None and ENVAR not in os.environ:
            target_filepath = LS_FILE_DEF_PATH
        elif target_dir is not None:
            target_filepath = os.path.join(target_dir, LS_FILENAME)

        if os.path.isfile(target_filepath):
            logger.info("{0} already exists!".format(target_filepath))
            if overwrite:
                logger.warning("{0} will be replaced!".format(target_filepath))
                os.remove(target_filepath)
            else:
                return False

        try:
            if download_data(url, target_file=target_filepath) is not None:
                logger.info("{0} saved".format(target_filepath))
            else:
                raise LstableException(
                    "Downloading {0} has failed!".format(url))
        except:
            print_exception()
        else:
            return True

    def set_file(self, file=None, reload=True):
        """Check if the leapsec table file exists on the local disk."""
        if file is not None:
            self.file = file
        elif file is None and ENVAR in os.environ:
            self.file = os.environ[ENVAR]
        elif (file is None and ENVAR not in os.environ and
              os.path.isfile(LS_FILE_DEF_PATH)):
            self.file = LS_FILE_DEF_PATH
        else:
            self.file = URL

        # Reloading the lstable with file
        if reload:
            self.load_lstable(reload=True)

    def load_lstable(self, reload=False):
        """Load NASA CDF leapsec table CDFLeapSeconds.txt."""
        if self.lstable is not None and not reload:
            logger.info("Leapsec. table is already loaded, aborting!")
            return False
        elif self.lstable is not None and reload:
            logger.warning("Leapsec. table will be reloaded!")

        if (self.file.startswith("http") or
                self.file.startswith("ftp")):
            data = download_data(self.file)
            self.lstable = self._parse_lstable(data)
            return True
        elif os.path.isfile(self.file):
            buff = open(self.file, 'rt')
            data = buff.read()
            self.lstable = self._parse_lstable(data)
            return True
        else:
            logger.error("CDFLeapSeconds.txt cannot be loaded!")
            return False

    def _parse_lstable(self, data):
        """Parse the CDF leap second table file."""
        for row in data.split("\n"):
            row = str(row).rstrip()
            if row.startswith(";"):
                continue
            else:
                if row.strip() == "":
                    continue
                self._add(row)

        return data

    def __str__(self):
        """__str__ method."""
        if self.file is None:
            self.set_file()

        self.load_lstable()
        if self.lstable is None:
            return ""
        string = ("Date -- Leap Sec. -- Drift\n")
        for i, row in enumerate(self.date):
            string += ("{0} -- {1} -- {2}\n".format(
                self.date[i],
                self.leapsec[i],
                self.drift[i]))
        return string


# ________________ Global Functions __________
# (If required, define here gobal functions)


# _________________ Main ____________________________
#if (__name__ == "__main__"):
#    main()
