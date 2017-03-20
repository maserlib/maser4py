#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
leapsec.py.

Python module to load and handle a NAIF SPICE LeapSecond Kernels (lsk) file.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging
import urllib.request
import argparse
from datetime import datetime

__all__ = ["Lstable"]

# ________________ HEADER _________________________

# Mandatory
__version__ = "0.1.0"
__author__ = "X.Bonnin"
__date__ = "2017-03-17"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = "RPW Operation Centre (ROC)"
__institute__ = "LESIA"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

URL = "https://cdf.gsfc.nasa.gov/html/CDFLeapSeconds.txt"

INPUT_DATE = "%Y-%m-%dT%H:%M:%S"


# ________________ Class Definition __________
# (If required, define here classes)
class Lstable:
    """Class for the leapsec table."""

    def __init__(self, file=URL):
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
            self._parse_lstable(file=file)

        if date < self.date[0]:
            return 0.0
        elif date >= self.date[-1]:
            return self.leapsec[-1]
        else:
            for i, lsdate in enumerate(self.date[:-1]):
                if date >= lsdate and date < self.date[i + 1]:
                    return self.leapsec[i]

        return None

    def get_lstable(self, target_dir=os.curdir):
        """Download the Leapsec table file in the target_dir."""
        if os.path.isdir(target_dir):
            filename = os.path.basename(self.file)
            target_file = os.path.join(target_dir, filename)
            with open(target_file, 'rw') as fw:
                fw.write(self.lstable)
            if os.path.isfile(target_file):
                logger.info("{0} saved".format(target_file))
            else:
                logger.error("{0} has been saved correctly!".format(
                                                            target_file))

    def _load_lstable(self):
        """Load NASA CDF leapsec table CDFLeapSeconds.txt."""
        file = self.file
        if (file.startswith("http") or
                file.startswith("ftp")):
            buff = urllib.request.urlopen(file)
            data = buff.read().decode("utf-8")
        else:
            buff = open(file, 'rt')
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
                        "Default is [{0}]".format(URL))
    parser.add_argument("-d", "--date", nargs=1,
                        default=[None],
                        help="Return the leap seconds for "
                            "a given date and time."
                            "(Expected format is \"YYYY-MM-DDThh:mm:ss\")")
    parser.add_argument("-t", "--target-dir", nargs=1,
                        default=[None],
                        help="Download the CDFLeapSeconds.txt"
                        " in the target-dir")
    parser.add_argument("-S", "--SHOW-TABLE", action='store_true',
                        help="Show the leap sec. table")

    args = parser.parse_args()
    lst = Lstable(file=args.filepath[0])

    if args.target_dir[0] is not None:
        lst.get_lstable(target_dir=args.target_dir[0])

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
