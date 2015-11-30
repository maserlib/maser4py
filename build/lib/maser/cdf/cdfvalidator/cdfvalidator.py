#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python 3 module to validate a CDF format file
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import json
import argparse
import subprocess
import logging

from spacepy import pycdf

from ...tools import which, setup_logging
from .istp_globals import FILLVALL

# ________________ HEADER _________________________

# Mandatory
__version__ = "0.1.0"
__author__ = "Xavier Bonnin"
__date__ = "30-NOV-2015"

# Optional
__institute__ = "LESIA, Observatoire de Paris, CNRS"
__project__ = "MASER"
__license__ = ""
__credit__ = [""]
__maintainer__ = "Xavier Bonnin"
__email__ = "xavier.bonnin@obspm.fr"
__change__ = {"version": "change"}

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)


# ________________ Class Definition __________
# (If required, define here classes)
class Validate():

    """Class that provides tools to validate a CDF format file"""

    def __init__(self, cdf_file,
                 verbose=False,
                 debug=False):

        # Setup the logging
        setup_logging(
            filename=None, quiet=False,
            verbose=verbose, debug=debug)

        self.cdf_file = cdf_file
        self.cdf = self.open_cdf(cdf_file)

    def open_cdf(self, cdf_file):

        """Open the input cdf file"""

        try:
            cdf = pycdf.CDF(cdf_file)
            cdf.readonly(True)
        except pycdf.CDFError as e:
            logger.error(e)
            raise
        else:
            return cdf

    def close_cdf(self):
        """ Close current cdf file"""
        self.cdf.close()

    def check_istp(self,
                    zvars=None):

        """Check that the input CDF is compliant with
            ISTP guidelines"""
        cdf = self.cdf

        if zvars is None:
            zvars = cdf.keys()

        for zvar in zvars:
            vattrs = cdf[zvar].attrs
            for vattr in vattrs:
                print(vattr)

    def check_vattrs(self, vattrs,
                     zvars=None):

        """Check consistency of given variable attributes"""
        cdf = self.cdf

        if (zvars is None):
            zvars = cdf.keys()

        for zvar in zvars:
            zvattrs = zvar.attrs
            for vattr in zvattrs.keys():
                if (vattr in vattrs):
                    if (zvattrs[vattr] != vattrs[vatrr]):
                        print("TBD")

    def check_model(self, model_file):

        """Check the CDF content compared to
        the input mode file"""

        # Read CDF file
        cdf = self.cdf

        # Read JSON format model file
        with open(model_file, 'r') as fbuff:
            mfile = json.load(fbuff)

    def cdfvalidate(self, program=None):

        """Run the cdfvalidate program of the GSFC CDF distribution"""

        if program is None:
            program = which("cdfvalidate")
            if program is None:
                return False, "cdfvalidate program has not been found!"

        pro = subprocess.Popen([program, self.cdf_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (output, error) = pro.communicate()
        if (pro.wait() == 0):
            return True, output
        else:
            return False, error


# ________________ Global Functions __________
# (If required, define here gobal functions)
def main():

    """cdfvalidator main program"""

    parser = argparse.ArgumentParser(
        description='Validate a CDF format file',
        add_help=True)
    parser.add_argument('cdf_file', nargs='?',
                        default=None,
                        help='Path of the CDF format file to validate')
    parser.add_argument('-m', '--model_file', nargs='?',
                        default=None,
                        help='Path to the model file in JSON format')
    parser.add_argument('-c', '--cdfvalidate', nargs='?',
                        default=None,
                        help='Path of the cdfvalidate program')
    parser.add_argument('-O', '--Overwrite', action='store_true',
                        help='Overwrite existing output files')
    parser.add_argument('-V', '--Verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-D', '--Derbose', action='store_true',
                        help='Debug mode')
    parser.add_argument('-A', '--All', action='store_true',
                        help='Perform all of the validations')
    parser.add_argument('--version', action='store_true',
                        help='Show version')
    parser.add_argument('--change', action='store_true',
                        help='Show change')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.change:
        print(__change__)
        sys.exit(0)

    if not args.cdf_file:
        parser.print_help()
        sys.exit(0)

    cdfval = Validate(args.cdf_file,
                          verbose=args.Verbose,
                          debug=args.Debug)

    if args.ALL or args.model_file:
        cdfval.check_model(args.model_file)

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
