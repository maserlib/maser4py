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

from ...tools import which, setup_logging, run_command, quote
from ...settings import SUPPORT_DIR

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

ISTP_MOD_FILE = os.path.join(SUPPORT_DIR, "cdf",
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

        # Check global attributes
        gattrlist = cdf.attrs
        for gattr_name in istpfile["GlobalAttributes"]:
            if gattr_name not in gattrlist:
                issues.append(gattr_name + " global attribute required!")
            else:
                gattr_istp = istpfile["GlobalAttributes"][gattr_name]
                if len(gattr_istp[0]) > 0:
                    gattr_cdf = cdf.attrs[gattr_name]
                    if gattr_istp != gattr_cdf:
                        issues.append(gattr_name +
                                      " global attribute entry value(s)"
                                      " mismatched!")

        if zvars is None:
            zvars = cdf.keys()

        # Check that input CDF has the primary Epoch variable
        if ("Epoch" not in zvars and
        "EPOCH" not in zvars and
        "epoch" not in zvars):
            issues.append("No Epoch primary variable found!")

        # Check the list of variable attributes
        for zvar_name in zvars:
            zvar = cdf[zvar_name]
            vattrlist = zvar.attrs
            if "VAR_TYPE" not in vattrlist:
                issues.append(zvar_name +
                              ": VAR_TYPE variable attribute required!")
            else:
                if vattrlist["VAR_TYPE"] != "data":
                    continue
                for vattr_istp in istpfile["VariableAttributes"]:
                    if vattr_istp not in vattrlist:
                        issues.append(zvar_name + ": " +
                                      vattr_istp +
                                      " variable attribute required!")

        # Display issues found
        for issue in issues:
            logger.warning(issue)

    def is_model_compliant(self, model_file):

        """Check the CDF content compared to
        the input mode file"""

        def get_cdftype(dtype):
            """Return id of the CDF data type"""
            return pycdf.const.__dict__[dtype].value

        def get_vattrs(cdf):

            """
            Retrieve the list of zVariables attributes
            """

            vattrs = {}

            if len(cdf) == 0:
                logger.warning("No Zvariable in the " + self.cdf_file)
                return vattrs

            for zvar in cdf:
                zattrs = cdf[zvar].attrs
                for vattr in zattrs:
                    zattr = pycdf.zAttr(cdf, vattr)
                    vattrs[vattr] = zattr

            return vattrs

        def check(cdf, items):

            """
            Check items of a given CDF
            GLOBALattributes, VARIABLEattributes, zVariables
            """
            issues = []

            for item in items:
                name = item['name']
                logger.info("--> " + name)
                istype = ("type" in item)
                isentry = ("entries" in item)
                hasvalue = ("hasvalue" in item)

                issize = ("size" in item)
                isdims = ("dims" in item)
                isattrs = ("attributes" in item)

                if name in cdf:
                    cdfitem = cdf[name]
                    nentry = len(cdfitem)

                    if hasvalue:
                        logger.debug("Checking value existence")
                        if nentry == 0 or len(cdfitem[0].strip()) == 0:
                            msg = (name + " " +
                                          " has no entry value!")
                            logger.warning(msg)
                            issues.append(msg)

                    if isentry:
                        logger.debug("Checking attribute entries")
                        if nentry < len(item["entries"]):
                            msg = (name + " "
                                          + " has missing entries!")
                            logger.warning(msg)
                            issues.append(msg)
                        else:
                            for i in range(len(item["entries"])):
                                if cdfitem[i] != item["entries"][i]:
                                    msg = (quote(name) + " "
                                            + " has a wrong entry value: "
                                            + quote(item["entries"][i]) +
                                            " (" + quote(cdfitem[i])
                                            + " expected)!")
                                    logging.warning(msg)
                                    issues.append(msg)

                    if istype:
                        logger.debug("Checking data type")
                        cdftype = get_cdftype(item["type"])
                        for j in range(len(cdfitem)):
                            if cdfitem.type(j) != cdftype:
                                msg = (quote(name)
                                            + " has the wrong data type:" +
                                            quote(item["type"])
                                            + " expected)!")
                                logging.warning(msg)
                                issues.append(msg)

                    if issize:
                        logger.debug("Checking data size")
                        if cdfitem.shape != item["size"]:
                            msg = (name + " " +
                            " has the wrong size!")
                            logging.warning(msg)
                            issues.append(msg)

                    if isdims:
                        if len(cdfitem) != item["dims"]:
                            logger.debug("Checking data dimension(s)")
                            msg = (name + " " +
                             " has the dims size!")
                            logging.warning(msg)
                            issues.append(msg)

                    if isattrs:
                        logger.info("Checking variable attributes of "
                                    + quote(name) + ":")
                        check(cdf[name].attrs, item["attributes"])
                else:
                    msg = (name + " required!")
                    logging.warning(msg)
                    issues.append(msg)

            return issues

        issues = []

        # Retrieve CDF
        cdf = self.cdf

        # Read JSON format model file
        logger.info("Loading " + model_file)
        with open(model_file, 'r') as fbuff:
            mfile = json.load(fbuff)

        if "GLOBALattributes" in mfile:
            logging.info("Checking GLOBALattributes:")
            issues.extend(check(cdf.attrs, mfile["GLOBALattributes"]))
        if "VARIABLEattributes" in mfile:
            logging.info("Checking VARIABLEattributes:")
            vattrs = get_vattrs(cdf)
            issues.extend(check(vattrs, mfile["VARIABLEattributes"]))
        if "zVariables" in mfile:
            logging.info("Checking zVariables:")
            issues.extend(check(cdf, mfile["zVariables"]))

        return issues

    def cdfvalidate(self, program=None):

        """Run the cdfvalidate program in the GSFC CDF distribution"""

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
        cdfvalid.is_model_compliant(args.model_file)

    cdfvalid.close_cdf()

# _________________ Main ____________________________
if __name__ == "__main__":
    main()
