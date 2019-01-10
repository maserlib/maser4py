#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python 3 module to validate a CDF format file."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import json
import logging
from tempfile import TemporaryDirectory

from maser.utils.cdf import CDF

from ...toolbox import run_command, quote, move_safe
from ..tools import get_cdftype, get_vattrs, get_cdftypename
from ....settings import SUPPORT_DIR

__all__ = ["Validate", "cdfvalidator", "ValidatorException"]

# ________________ HEADER _________________________



# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)

CDF_ENV = {"CDF_LEAPSECONDSTABLE": None,
           "CDF_BIN": None}

ISTP_MOD_FILE = os.path.join(SUPPORT_DIR, "cdf",
                             "validator_model_istp.json")


# ________________ Class Definition __________
# (If required, define here classes)
class ValidatorException(Exception):
    """Exception class for Validator."""

    pass


class Validate():
    """Class that provides tools to validate a CDF format file."""

    def __init__(self,cdf_file,
                 cdf_env=CDF_ENV):
        """Validate Init method."""

        self.file = None
        self.cdf = None
        self.open_cdf(cdf_file)
        self.cdf_env = self._init_cdfenv(cdf_env=cdf_env)

    def _init_cdfenv(self, cdf_env=CDF_ENV):
        """Initialize instance."""
        # get CDF program path
        for key, val in cdf_env.items():
            if val is None:
                if key in os.environ:
                    cdf_env[key] = os.environ[key]
                else:
                    logger.error("{0} is not defined!".format(key))
                    raise ValidatorException
        return cdf_env

    def open_cdf(self, file):
        """Open the input cdf file."""
        logger.info("Opening {0}".format(file))
        self.file = file
        try:
            cdf = CDF(self.file)
            cdf.readonly(True)
        except ValidatorException as e:
            logger.error(e)
            raise ValidatorException
        else:
            self.cdf = cdf

    def close_cdf(self):
        """Close current cdf file."""
        logger.info("Closing " + self.file)
        self.cdf.close()

    def is_istp_compliant(self):
        """
        Istp compliant.

        Check that the input CDF is compliant with
            ISTP guidelines
        """
        issues = []

        issues.extend(self.is_model_compliant(ISTP_MOD_FILE))
        issues.extend(self.is_istp_fillval())

        return issues

    def is_model_compliant(self, model_file):
        """Check the CDF content compared to the input mode file."""
        pass

        def check(cdf, items):
            """
            Check CDF items.

            Check items of a given CDF
            GLOBALattributes, VARIABLEattributes, zVariables
            """
            issues = []

            for item in items:
                name = item['name']
                logger.info("Checking \"{0}\"".format(name))
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
                        logger.debug("Checking value existence...")
                        if nentry == 0 or len(cdfitem[0].strip()) == 0:
                            msg = "--> \"{0}\" has no entry value!".format(name)
                            logger.warning(msg)
                            issues.append(msg)

                    if isentry:
                        logger.debug("Checking attribute entries...")
                        if nentry < len(item["entries"]):
                            msg = "--> \"{0}\" has missing entries!".format(name)
                            logger.warning(msg)
                            issues.append(msg)
                        else:
                            for i in range(len(item["entries"])):
                                if cdfitem[i] != item["entries"][i]:
                                    msg = "--> \"{0}\" has a wrong entry value: ".format(name) + \
                                            "\"{0}\" found, but \"{1}\" expected!".format(
                                               cdfitem[i], item["entries"][i])
                                    logging.warning(msg)
                                    issues.append(msg)

                    if istype:
                        logger.debug("Checking data type")
                        cdftype = get_cdftype(item["type"])
                        for j in range(len(cdfitem)):
                            if cdfitem.type(j) != cdftype:
                                msg = "--> \"{0}\" has the wrong data type:".format(name) + \
                                       "\"{0}\" expected!".format(item["type"])
                                logging.warning(msg)
                                issues.append(msg)

                    if issize:
                        logger.debug("Checking data size")
                        if cdfitem.shape != item["size"]:
                            msg = "--> \"{0}\" has the wrong size!".format(name)
                            logging.warning(msg)
                            issues.append(msg)

                    if isdims:
                        if len(cdfitem) != item["dims"]:
                            logger.debug("Checking data dimension(s)")
                            msg = "--> \"{0}\" has the wrong dims size!".format(name)
                            logging.warning(msg)
                            issues.append(msg)

                    if isattrs:
                        logger.info("Checking variable attributes of \"{0}\"...".format(name))
                        check(cdf[name].attrs, item["attributes"])
                else:
                    msg = "--> \"{0}\" required!".format(name)
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
        """
        Is_istp_fillval.

        Check if the FILLVAL variable attribute values
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

    def cdfconvert(self, src, dst,
                   args=None, program=None,
                   overwrite=False):
        """Run the cdfconvert program in the GSFC CDF distribution."""
        cmd = []

        if program is None:
            program = os.path.join(self.cdf_env["CDF_BIN"], "cdfconvert")

        if program is None or not os.path.isfile(program):
            logger.error("cdfconvert not found!")
            return None

        cmd = [program, src, dst]

        if args is not None:
            cmd.append(args)

        if overwrite is True:
            with TemporaryDirectory() as tempdir:
                src = move_safe(src, tempdir)
                self.cdfconvert(src, dst, args=args,
                                program=program,
                                overwrite=False)

        return run_command(cmd)

    def cdfvalidator(self, file, program=None):
        """Run the cdfvalidate program in the GSFC CDF distribution."""
        cmd = []

        if program is None:
            program = os.path.join(self.cdf_env["CDF_BIN"], "cdfvalidate")

        if program is None or not os.path.isfile(program):
            logger.error("cdfvalidate not found!")
            return None
        cmd = [program, file]

        return run_command(cmd)

    @classmethod
    def is_cdf_valid(cls, file, program=None, quiet=False):
        """Call the cdfvalidate program."""
        res = cls(quiet=quiet).cdfvalidate(file, program=program)

        output, errors = res.communicate()
        if res.wait() == 0:
            logger.info(output)
            return True
        else:
            logger.error("ERROR RUNNING COMMAND cdfvalidate: ")
            logger.error("STDOUT - %s", str(output))
            logger.error("STDERR - %s", str(errors))
            return False

    def is_zvar_valid(self, zvarname):
        """
        Is_zvar_valid.

        Check  the values of a zVariable
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
def cdfvalidator(cdf_file,
                 is_istp=False,
                 model_json_file=None,
                 cdfvalidate_bin=None,
                 run_cdf_validate=False):
    """cdfvalidator main program."""

    # Initialize a Validate object
    cdfvalid = Validate(cdf_file=cdf_file)

    # Check ISTP compliance
    if is_istp:
        cdfvalid.is_istp_compliant()

    # Check compliance with input model json file
    if model_json_file:
        cdfvalid.is_model_compliant(model_json_file)

    cdfvalid.close_cdf()

# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)
