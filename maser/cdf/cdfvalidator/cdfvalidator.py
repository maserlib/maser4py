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
from ..tools import get_cdftype, get_vattrs, get_cdftypename
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
__change__ = {"0.1.0": "First beta version"}

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
                 debug=False,
                 quiet=False):

        # Setup the logging
        setup_logging(
            filename=log_file, quiet=quiet,
            verbose=verbose, debug=debug)

        self._setcdf(cdf_file)

    def _setcdf(self, cdf_file):
        """Set the input cdf file"""
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

    def is_istp_compliant(self):

        """Check that the input CDF is compliant with
            ISTP guidelines"""

        issues = []

        issues.extend(self.is_model_compliant(ISTP_MOD_FILE))
        issues.extend(self.is_istp_fillval())

        return issues

    def is_model_compliant(self, model_file):

        """Check the CDF content compared to
        the input mode file"""

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

    def is_istp_fillval(self, zvarnames=None):

        """Check if the FILLVAL variable attribute values
        are ISTP compliant
        """

        issues = []

        if zvarnames is None:
            zvarnames = [key for key in self.cdf]

        # Read JSON format model file
        logger.info("Loading " + ISTP_MOD_FILE)
        with open(ISTP_MOD_FILE, 'r') as fbuff:
            mfile = json.load(fbuff)

        istpfillval = mfile["ISTPMapping"]["FILLVAL"]

        for zvname in zvarnames:
            if zvname in self.cdf:
                zvar = self.cdf[zvname]
                if "FILLVAL" in zvar.attrs:
                    fillval = zvar.attrs["FILLVAL"]
                    zvtype = get_cdftypename(zvar.type())
                    if str(istpfillval[zvtype]) != str(fillval):
                        msg = ("%s has an invalid FILLVAL value: "
                               % (quote(zvname)))
                        msg += ("%s found, but %s expected!" %
                                (quote(fillval), quote(istpfillval[zvtype])))
                        logging.warning(msg)
                        issues.append(msg)
                else:
                    msg = ("%s has no FILLVAL attribute!"
                    % (quote(zvname)))
                    logging.warning(msg)
                    issues.append(msg)
            else:
                logger.warning("%s not found in %s!",
                               quote(zvar), self.cdf_file)

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

    def is_zvar_valid(self, zvarname):

        """ Ckech  the values of a zVariable
        comparing to the its VALIMIN/VALIDMAX attributes
        """

        issues = []

        cdf = self.cdf

        if zvarname not in cdf:
            logger.error("%s not in %s!", zvarname, cdf)
            return False
        else:
            zvar = cdf[zvarname]

        logger.info("Cheching %s", zvarname)

        zattrs = zvar.attrs
        if "VALIDMIN" in zattrs:
            validmin = zattrs["VALIDMIN"]
            logger.info("VALIDMIN=%s", str(validmin))
        else:
            logger.warning("No VALIDMIN attribute for %s", zvarname)
            validmin = None

        if "VALIDMAX" in zattrs:
            validmax = zattrs["VALIDMAX"]
            logger.info("VALIDMAX=%s", str(validmax))
        else:
            logger.warning("No VALIDMAX attribute for %s", zvarname)
            validmax = None

        for i, rec in enumerate(zvar):
            if rec.min() < validmin:
                msg = ("[%i]: Record value(s) lesser than VALIDMIN!") % (i)
                logger.warning(msg)
                issues.append(msg)

            if rec.max() > validmax:
                msg = ("[%i]: Record value(s) greater than VALIDMAX!") % (i)
                logger.warning(msg)
                issues.append(msg)

        return issues


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
    parser.add_argument('-V', '--Verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-Q', '--Quiet', action='store_true',
                        help='Quiet mode')
    parser.add_argument('-D', '--Debug', action='store_true',
                        help='Debug mode')
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

    # Initialize a Validate object
    cdfvalid = Validate(args.cdf_file,
                          log_file=args.log_file,
                          verbose=args.Verbose,
                          quiet=args.Quiet,
                          debug=args.Debug)

    if args.ISTP:
        cdfvalid.is_istp_compliant()

    if args.model_file:
        cdfvalid.is_model_compliant(args.model_file)

    cdfvalid.close_cdf()

# _________________ Main ____________________________
if __name__ == "__main__":
    main()
