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

from spacepy import pycdf

from ...tools import which, setup_logging
from .istp_globals import FILLVALL

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
class CDFValidator():

    def __init__(self, cdf_file):
        self.cdf_file = cdf_file

        try:
            self.cdf = pycdf.CDF(self.cdf_file)
            self.cdf.readonly(True)
        except pycdf.CDFError as e:
            print(e)
            return None

    def check_istp(self,
                    zvars=None):

        """Check that the input CDF is compliant with
            ISTP guidelines"""
        cdf = self.cdf

        if (zvars is None):
            zvars = cdf.keys()

        for zvar in zvars:



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
    parser.add_argument('-A', '--All', action='store_true',
                        help='Perform all of the validations')
    parser.add_argument('--version', action='store_true',
                        help='Show version')
    parser.add_argument('--change', action='store_true',
                        help='Show change')
    args = parser.parse_args()

    if (args.version):
        print(__version__)
        sys.exit(0)

    if (args.change):
        print(__change__)
        sys.exit(0)

    if not (args.cdf_file):
        parser.print_help()
        sys.exit(1)

    # Setup the logging
    setup_logging(
        filename=None, quiet=False,
        verbose=verbose, debug=debug)

    cdfval = CDFValidator(args.cdf_file)

    if args.ALL or args.model_file:
        cdfval.check_model(args.model_file)

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
