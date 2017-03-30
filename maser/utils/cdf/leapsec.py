#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
leapsec.py.

Python module to load and handle a NAIF SPICE LeapSecond Kernels (lsk) file.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import logging
import urllib.request
import argparse
from datetime import datetime

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


# ________________ Class Definition __________
# (If required, define here classes)
class Lstable:
    """Class for the leapsec table."""

    def __init__(self, file=None):
        """Leapsec __init__ method."""
        self.file = file
        self.date = []
        self.leapsec = []
        self.drift = []
        self.lstable = None
        self._parse_lstable()

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
            self._parse_lstable()

        if date < self.date[0]:
            return 0.0
        elif date >= self.date[-1]:
            return self.leapsec[-1]
        else:
            for i, lsdate in enumerate(self.date[:-1]):
                if date >= lsdate and date < self.date[i + 1]:
                    return self.leapsec[i]

        return None

    def get_lstable(self, target_dir=None, overwrite=False):
        """Download the Leapsec table file into the target_dir."""
        if target_dir is None and ENVAR in os.environ:
            target_dir = os.path.dirname(os.environ[ENVAR])
        elif target_dir is None and ENVAR not in os.environ:
            target_dir = os.curdir

        if os.path.isdir(target_dir):
            target_file = os.path.join(target_dir, LS_FILENAME)

            if os.path.isfile(target_file) and not overwrite:
                logger.warning("{0} already exists!".format(
                                            target_file))
                return False
            elif os.path.isfile(target_file) and overwrite:
                logger.warning("{0} will be replaced!".format(
                                            target_file))
                os.remove(target_file)

            with open(target_file, 'w') as fw:
                fw.write(self.lstable)

            if os.path.isfile(target_file):
                logger.info("{0} saved".format(target_file))
                return True
            else:
                logger.error("{0} has been saved correctly!".format(
                                                            target_file))
        else:
            logger.error("{0} directory does not exist!".format(
                                                target_dir))

        return False

    def _load_lstable(self):
        """Load NASA CDF leapsec table CDFLeapSeconds.txt."""
        if self.file is None and ENVAR in os.environ:
            self.file = os.environ[ENVAR]
        else:
            self.file = URL

        if (self.file.startswith("http") or
                self.file.startswith("ftp")):
            buff = urllib.request.urlopen(self.file)
            data = buff.read().decode("utf-8")
        else:
            buff = open(self.file, 'rt')
            data = buff.read()

        return data

    def _parse_lstable(self):
        """Parse the CDF leap second table file."""
        data = self._load_lstable()

        for row in data.split("\n"):
            row = str(row).rstrip()
            if row.startswith(";"):
                continue
            else:
                if row.strip() == "":
                    continue
                self._add(row)

        self.lstable = data

    def set_file(self, file):
        """Use a new CDF leapsec file."""
        self.file = file
        self._parse_lstable()

    def __str__(self):
        """__str__ method."""
        if self.lstable is None:
            self._parse_lstable()
        string = ("Date -- Leap Sec. -- Drift\n")
        for i, row in enumerate(self.date):
            string += ("{0} -- {1} -- {2}\n".format(
                        self.date[i],
                        self.leapsec[i],
                        self.drift[i]))
        return string


# ________________ Global Functions __________
# (If required, define here gobal functions)
def main():
    """Main program."""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-f", "--filepath",
                        nargs=1, default=[URL],
                        help="CDFLeapSeconds.txt filepath.\n "
                        "Default is [${0}]".format(ENVAR))
    parser.add_argument("-d", "--date", nargs=1,
                        default=[None],
                        help="Return the leap seconds for "
                            "a given date and time."
                            "(Expected format is \"YYYY-MM-DDThh:mm:ss\")")
    parser.add_argument("-g", "--get-file", nargs='?',
                        help="Download the CDFLeapSeconds.txt"
                        "from the NASA CDF site. "
                        "If the [GET_FILE] optional argument"
                        " is provided, then it must be a valid"
                        " directory where the file will be saved.")
    parser.add_argument("-S", "--SHOW-TABLE", action='store_true',
                        help="Show the leap sec. table")
    parser.add_argument("-O", "--Overwrite", action='store_true',
                        help="Overwrite existing file")

    args = parser.parse_args()
    lst = Lstable(file=args.filepath[0])

    if hasattr(args, 'get_file'):
        lst.get_lstable(target_dir=args.get_file,
                        overwrite=args.Overwrite)
        sys.exit(0)

    if args.date[0] is not None:
        date = datetime.strptime(args.date[0], INPUT_DATE)
        print("{0} sec.".format(lst.get_leapsec(date=date)))
    elif args.SHOW_TABLE is True:
        print(lst)
    else:
        parser.print_help()

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
