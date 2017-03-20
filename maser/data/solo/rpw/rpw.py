#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""MASER: SolO/RPW main module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import argparse
import logging

from .tools import cdf_info, get_dataset_id, file2cdf
from .globals import RPW_PLOT_FUNC

from ....utils import toolbox as tb


__all__ = ["Rpw", "main"]

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
__project__ = "MASER, RPW"
__institute__ = "LESIA, Obs.Paris, CNRS"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)


class Rpw:
    """Rpw class."""

    def __init__(self, cdf):
        """__init__ method."""
        self.file = cdf
        self.data = file2cdf(cdf)
        self.ds = get_dataset_id(self.data)

    def plot(self, *args, **kwargs):
        """Plot RPW CDF file."""
        for key, func in RPW_PLOT_FUNC.items():
            if key in self.ds:
                func(self.data, *args, **kwargs)


# ________________ Global Functions __________
# (If required, define here gobal functions)
def main():
    """Main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("cdf_file", nargs=1, type=str,
                        help="SOLO RPW CDF file to load",
                        default=[""])
    parser.add_argument("--args", nargs='+',
                        help="Extra input arguments",
                        default=[None])
    parser.add_argument("--kargs", nargs='+',
                        help="Extra input keyword arguments",
                        default=[None])
    parser.add_argument("-p", "--plot", action='store_true',
                        help="Plot data inside input CDF")
    parser.add_argument("-l", "--logfile", nargs=1,
                        default=[None], help="Log file")
    parser.add_argument("-q", "--quiet", action='store_true',
                        help="Quiet mode")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Verbose mode")

    args = parser.parse_args()

    tb.setup_logging(filename=args.logfile[0],
                     quiet=args.quiet, debug=args.verbose)

    cdf = args.cdf_file[0]
    if os.path.isfile(cdf):
        # Get RPW DATASET ID
        rpw = Rpw(cdf)
        if args.plot is True:
            rpw.plot(args.args, args.kargs)
        if args.quiet is False:
            logger.info(cdf_info(cdf))

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
