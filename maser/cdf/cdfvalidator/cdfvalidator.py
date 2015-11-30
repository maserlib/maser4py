#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python 3 module to validate a CDF format file
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import sys
import json
import argparse
import logging

from spacepy import pycdf

from ...tools import which, setup_logging, run_command

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

ISTP_MOD_FILE = os.path.join(os.path.dirname(__file__),
                             "cdfvalidator_model_istp.json")


# ________________ Class Definition __________
# (If required, define here classes)
class Validate():

    """Class that provides tools to validate a CDF format file"""

    def __init__(self, cdf_file,
                 log_file=None,
                 verbose=False,
                 debug=False):

        # Setup the logging
        setup_logging(
            filename=log_file, quiet=False,
            verbose=verbose, debug=debug)

        self.cdf_file = cdf_file
        self.cdf = self.open_cdf()

    def open_cdf(self):

        """Open the input cdf file"""

        logger.info("Opening " + self.cdf_file)
        try:
            cdf = pycdf.CDF(self.cdf_file)
            cdf.readonly(True)
        except pycdf.CDFError as e:
            logger.error(e)
            raise pycdf.CDFError
        else:
            return cdf

    def close_cdf(self):
        """ Close current cdf file"""
        logger.info("Closing " + self.cdf_file)
        self.cdf.close()

    def is_istp_compliant(self,
                    zvars=None):

        """Check that the input CDF is compliant with
            ISTP guidelines"""

        issues = []

        cdf = self.cdf

        logging.info("Importing %s", ISTP_MOD_FILE)
        # Read JSON format model file for ISTP
        with open(ISTP_MOD_FILE, 'r') as fbuff:
            istpfile = json.load(fbuff)

        print(istpfile)
        sys.exit()

        if zvars is None:
            zvars = cdf.keys()

        # Check that input CDF has the primary Epoch variable
        if ("Epoch" not in zvars and
        "EPOCH" not in zvars and
        "epoch" not in zvars):
            issues.append("No Epoch primary variable found!")

        # Check the list of mandatory global attributes
        #gattrs =
        #for


        # Check the list of variable attributes
        for zvar_name in zvars:
            zvar = cdf[zvar_name]
            for vattr_name in zvar.attrs:
                vattr_entry = zvar.attrs[vattr_name]
                print(vattr_name)
                print(vattr_entry)
                vattr = pycdf.zAttr(cdf, vattr_name)
                #print(zvar_name + ":" + vattr_name)
                #print(vattr.has_entry())
                print(zvar.type())
                print(vattr.type(0))


    def check_vattrs(self, vattrs,
                     zvars=None):

        """Check consistency of given variable attributes"""
        cdf = self.cdf

        if zvars is None:
            zvars = cdf.keys()

        for zvar in zvars:
            zvattrs = zvar.attrs
            for vattr in zvattrs.keys():
                if vattr in vattrs:
                    if zvattrs[vattr] != vattrs[vattr]:
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

        cmd = []

        if program is None:
            program = which("cdfvalidate")

        if program is None:
            logger.error("skeletoncdf PROGRAM IS NOT"
                " IN THE $PATH VARIABLE!")
            return None
        cmd.append(program)

        res = run_command(cmd)
        output, errors = res.communicate()
        if res.wait() == 0:
            logger.info(output)
            return True
        else:
            logger.error("ERROR RUNNING COMMAND: ")
            logger.error(" ".join(cmd))
            logger.error("STDOUT - %s", str(output))
            logger.error("STDERR - %s", str(errors))
            return False


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
    parser.add_argument('-l', '--log_file', nargs='?',
                        default=None,
                        help='Path of the output log file')
    parser.add_argument('-I', '--ISTP', action='store_true',
                        help='Check the ISTP guidelines compliance')
    parser.add_argument('-C', '--CDFvalidate', action='store_true',
                        help='Check the CDF integrity'
                        'calling the CDFvalidate program')
    parser.add_argument('-O', '--Overwrite', action='store_true',
                        help='Overwrite existing output files')
    parser.add_argument('-V', '--Verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-D', '--Debug', action='store_true',
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

    if args.All:
        args.ISTP = True
        args.Consistency = True
        args.CDFvalidate = True

    # Initialize a Validate object
    cdfvalid = Validate(args.cdf_file,
                          log_file=args.log_file,
                          verbose=args.Verbose,
                          debug=args.Debug)

    if args.ISTP:
        cdfvalid.is_istp_compliant()

    if args.model_file:
        cdfvalid.check_model(args.model_file)

    cdfvalid.close_cdf()

# _________________ Main ____________________________
if __name__ == "__main__":
    main()
