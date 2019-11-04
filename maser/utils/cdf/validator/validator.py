#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python 3 module to validate a CDF format file."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import json
import logging
from tempfile import TemporaryDirectory

import numpy

from maser.utils.cdf import CDF, zAttr, zAttrList
from maser.utils.toolbox import run_command, quote, move_safe
from maser.utils.cdf.tools import get_cdftype, get_vattrs, get_cdftypename
from maser.settings import SUPPORT_DIR

__all__ = ["Validate", "cdfvalidator", "ValidatorException"]

# ________________ HEADER _________________________



# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

CDF_ENV = {"CDF_LEAPSECONDSTABLE": None,
           "CDF_BIN": None}

ISTP_MOD_FILE = os.path.join(SUPPORT_DIR, "cdf",
                             "validator_model_istp.json")

# Possible values for Issue class types
ISSUE_TYPES = ["zvar", "gatt", "vatt"]

# Possible values for Issue class checks
ISSUE_CHECKS = ["isitem", "hasvalue", "isentry", "istype", "issize", "isdims", "isattrs"]


# ________________ Class Definition __________
# (If required, define here classes)
class ValidatorException(Exception):
    """Exception class for Validator."""

    pass


class Issue:
    """Issue class."""
    def __init__(self, issues=None):
        self.counter = 0
        self.reset()
        if issues:
            self.extend(issues)

    def append(self, name, itype, check, msg, passed,
               varname="",
               num=None):
        """
        Append a new issue element

        :param name: Name of the issue
        :param itype: type of the issue
        :param check: check method of the issue
        :param msg: resulting message of the issue
        :param passed: if issue has succeeded is True, else False
        :param varname: Optional attribute for zvar name (in case vatt issue)
        :param num: gives issue number (if not provided, use counter)
        :return:
        """

        if itype not in ISSUE_TYPES:
            logger.warning("Input Issue type ({0}) is not valid!".format(itype))
            return None

        if check not in ISSUE_CHECKS:
            logger.warning("Input Issue check ({0}) is not valid!".format(check))
            print(name, itype, check, msg, passed)
            x=input()
            return None

        if not num:
            self.num.append(self.counter)
        else:
            self.num.append(num)
        self.name.append(name)
        self.type.append(itype)
        self.msg.append(msg)
        self.passed.append(passed)
        self.check.append(check)
        self.varname.append(varname)
        self.counter += 1

    def extend(self, issues):
        """
        Add issues to Issue object

        :param issues:
        :return:
        """

        if Issue.is_valid(issues):
            for issue in issues:
                self.append(issue[1], issue[2], issue[3], issue[4], issue[5], issue[6])
        else:
            logger.warning("Input argument is not valid Issue object!")

    @staticmethod
    def is_valid(issue):
        """
        Check if input is a valid Issue object

        :param issue: input to verify
        :return: True if is input is a valid Issue object, False otherwise
        """
        return isinstance(issue, Issue)

    def is_passed(self):
        """
        Check if issues are successfully passed or not

        :return: return True if all issues have been passed successfully, else False
        """
        return False not in self.passed

    def __len__(self):
        """Return number of issue elements."""
        return len(self.num)

    def __str__(self):
        """Return string with list of issues"""
        string = ""
        for issue in self:
            string += str(issue) + "\n"
        return string

    def reset(self):
        """
        Reset Issue object.

        :return:
        """
        self.num = []
        self.name = []
        self.type = []
        self.check = []
        self.msg = []
        self.passed = []
        self.varname = []
        self.counter = 0

    def __iter__(self, issues=None):
        """Iterator for Issue class."""

        if not issues:
            issues = self

        for i in range(0, len(issues)):
            yield issues.num[i], issues.name[i], \
                  issues.type[i], issues.check[i], \
                  issues.msg[i], issues.passed[i], \
                  issues.varname[i]

    def to_dict(self):
        """
        Convert issues into dictionary.

        :return:
        """
        # Generate dictionary from Issue object
        issue_dict = dict()
        for issue in self:
            issue_dict[issue[0]] = {
                "name": issue[1],
                "type": issue[2],
                "check": issue[3],
                "msg": issue[4],
                "passed": issue[5],
            }
            if issue[6]:
                issue_dict[issue[0]]["varname"] = issue[6]
        return issue_dict

    def to_json(self, output_file,
                overwrite=False,
                comment=""):
        """
        Write issues into an output json format file.

        :param output_file: Name of the output JSON file
        :param overwrite: If True then overwrite existing file
        :return: Issue dictionary
        """

        if os.path.isfile(output_file):
            if overwrite:
                os.remove(output_file)
            else:
                logger.warning("{0} already exists, aborting!".format(output_file))
                return None

        issue_dict = self.to_dict()
        with open(output_file, 'w') as fw:
            json.dump(issue_dict, fw)

        if os.path.isfile(output_file):
            logger.info("{0} saved".format(output_file))
            return issue_dict
        else:
            logger.warning("Saving {0} has failed!".format(output_file))
            return None




class Validate:
    """Class that provides tools to validate a CDF format file."""

    def __init__(self,cdf_file,
                 cdf_env=CDF_ENV):
        """Validate Init method."""

        self.file = None
        self.cdf = None
        self.open_cdf(cdf_file)
        self.cdf_env = self._init_cdfenv(cdf_env=cdf_env)
        self.issues = Issue()

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
        """
        Open the input cdf file.

        :param file:
        :return:
        """
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

        :return:
        """
        issues = Issue()

        issues.extend(self.is_model_compliant(ISTP_MOD_FILE))
        issues.extend(self.is_istp_fillval())

        self.issues.extend(issues)

        return issues

    def is_model_compliant(self, model_file):
        """
        Check the CDF content against a model given as an input JSON file.

        :param model_file: input json file path
        :return:
        """
        pass

        def check(cdf, items,
                  is_vattr=None,
                  is_gattr=None,
                  varname=""):
            """
            Check items of a given CDF
            GLOBALattributes, VARIABLEattributes, zVariables

            :param cdf: CDF object to check
            :param items: List of CDF items to check
            :param vattr: Check variable attributes
            :param gattr: Check global attributes
            :return:
            """
            issues = Issue()

            for item in items:
                name = item['name']
                logger.info('Checking "{0}"'.format(name))
                istype = ("type" in item)
                isentry = ("entries" in item)
                hasvalue = ("hasvalue" in item)
                isexcluded = ("excludes" in item)

                issizes = ("sizes" in item)
                isdims = ("dims" in item)
                isattrs = ("attributes" in item)

                if isexcluded and varname in item['excludes']:
                    logger.info("Checking {0} for {1} is ignored".format(name, varname))
                    return issues

                if is_vattr:
                    issue_type = "vatt"
                    try:
                        entries = self.cdf[varname].attrs
                    except:
                        entries = []
                elif is_gattr:
                    issue_type = "gatt"
                    entries = self.cdf.attrs
                else:
                    issue_type = "zvar"
                    entries = cdf

                if name in entries:
                    cdfitem = entries[name]

                    # If variable attribute...
                    if is_vattr:
                        # Get corresponding zAttr object
                        zattr = zAttr(cdf, name)

                        # Get number of entries
                        nentry = len(zattr)
                        # Get data type (from the max_idx to make sure)
                        dtype = get_cdftypename(zattr.type(zattr.max_idx()))
                    # If global attribute...
                    elif is_gattr:
                        # Get number of entries
                        nentry = len(cdfitem)

                        # Get data type (from the max_idx to make sure)
                        dtype = get_cdftypename(cdfitem.type(cdfitem.max_idx()))
                    # If zvariable...
                    else:
                        # If zVariable, get data type ...
                        dtype = get_cdftypename(cdfitem.type())
                        # and entry number
                        nentry = len(cdfitem)


                    # Store the item existence checking
                    passed = True
                    msg = "{0} CDF item found".format(name)
                    logfunc = logger.info
                    issues.append(name, issue_type, 'isitem', msg, passed, varname=varname)
                    logfunc(msg)

                    # Check if item has a value
                    if hasvalue:
                        logger.info("Checking value existence...")
                        if nentry == 0:
                            msg = '"{0}" has no entry value!'.format(name)
                            logfunc = logger.warning
                            passed = False
                        else:
                            msg = '"{0}" has entry values'.format(name)
                            logfunc = logger.info
                            passed = True
                        issues.append(name, issue_type, 'hasvalue', msg, passed, varname=varname)
                        logfunc(msg)

                    if istype:
                        logger.info("Checking data type")
                        cdftype = get_cdftypename(get_cdftype(item["type"]))
                        if dtype != cdftype:
                            msg = '"{0}\" has the wrong data type: '.format(name) + \
                                   '"{0}" found, but "{1}" expected!'.format(
                                dtype, cdftype)
                            logfunc = logger.warning
                            passed = False
                        else:
                            passed = True
                            logfunc = logger.info
                            msg = '"{0}" data type found'.format(dtype)

                        issues.append(name, issue_type, 'istype', msg, passed, varname=varname)
                        logfunc(msg)

                    if issizes:
                        logger.info("Checking data size")
                        if list(cdfitem.shape[1:]) != list(item["sizes"]):
                            msg = '"{0}" has the wrong sizes: '.format(name) + \
                                   '"{0}" found, but "{1}" expected!'.format(
                                       cdfitem.shape[1:], item["sizes"])
                            passed = False
                            logfunc = logger.warning
                        else:
                            passed = True
                            msg = '"{0}" sizes found'.format(item["sizes"])
                            logfunc = logger.info
                        issues.append(name, issue_type, 'issize', msg, passed, varname=varname)
                        logfunc(msg)

                    if isdims:
                        logger.info("Checking data dimension(s)")
                        if len(cdfitem.dv()) != item["dims"]:
                            msg = '"{0}" has the wrong dims: '.format(name) + \
                                   '"{0}" found, but "{1}" expected!'.format(
                                       len(cdfitem), item["dims"])
                            logfunc = logger.warning
                            passed = False
                        else:
                            passed = True
                            msg = '"{0}" dims found!'.format(item["dims"])
                            logfunc = logger.info
                        issues.append(name, issue_type, 'isdims', msg, passed, varname=varname)
                        logfunc(msg)

                    # Check if item has entries
                    if isentry:
                        logger.info("Checking attribute entries...")
                        if nentry < len(item["entries"]):
                            msg = '"{0}" has missing entries!'.format(name)
                            logger.warning(msg)
                            issues.append(name, issue_type, 'isentry', msg, False, varname=varname)
                        else:
                            # To avoid error in case where cdfitem is a String (for vattr)
                            if isinstance(cdfitem, str):
                                cdfitem = [cdfitem]
                            for i, entry in enumerate(item["entries"]):
                                if cdfitem[i] != entry:
                                    msg = '"{0}" has a wrong entry value: '.format(name) + \
                                            '"{0}" found, but "{1}" expected!'.format(
                                                cdfitem[i], entry)
                                    logfunc = logger.warning
                                    passed = False
                                else:
                                    passed = True
                                    msg = '"{0}" atttribute entry found'.format(entry)
                                    logfunc = logger.info
                                issues.append(name, issue_type, 'isentry', msg, passed, varname=varname)
                                logfunc(msg)

                    if isattrs:
                        logger.info('Checking variable attributes of "{0}"...'.format(name))
                        check(cdf, item["attributes"], is_vattr=True, varname=name)
                else:
                    msg = '"{0}" required!'.format(name)
                    logging.warning(msg)
                    passed = False
                    issues.append(name, issue_type, 'isitem', msg, passed, varname=varname)

            return issues

        issues = Issue()

        # Read JSON format model file
        logger.info("Loading " + model_file)
        with open(model_file, 'r') as fbuff:
            mfile = json.load(fbuff)

        if "GLOBALattributes" in mfile:
            logging.info("Checking GLOBALattributes:")
            issues.extend(check(self.cdf, mfile["GLOBALattributes"],
                                is_gattr=True))
        if "VARIABLEattributes" in mfile:
            #vattrs = get_vattrs(cdf)
            # Loop over all zVariables
            for zvar in self.cdf.keys():
                logging.info("Checking VARIABLEattributes for {0}".format(zvar))
                issues.extend(check(self.cdf, mfile["VARIABLEattributes"],
                                    is_vattr=True,
                                    varname=zvar))
        if "zVariables" in mfile:
            logging.info("Checking zVariables:")
            issues.extend(check(self.cdf, mfile["zVariables"]))

        return issues

    def is_istp_fillval(self, zvarnames=None):
        """
        Is_istp_fillval.

        Check if the FILLVAL variable attribute values
        are ISTP compliant
        """
        issues = Issue()

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
                        issues.append("FILLVAL", "vatt", "isentry", msg, False, varname=zvar)
                    else:
                        msg = "FILLVAL found in {0}".format(zvname)
                        issues.append("FILLVAL", "vatt", "isentry", msg, True, varname=zvar)
                else:
                    msg = ("%s has no FILLVAL attribute!"
                           % (quote(zvname)))
                    logging.warning(msg)
                    issues.append("FILLVAL", "vatt", "isentry", msg, False, varname=zvar)
            else:
                logger.warning("%s not found in %s!",
                               quote(zvar), self.cdf_file)

        return issues

    def cdfconvert(self, src, dst,
                   args=None, program=None,
                   overwrite=False):
        """Run the cdfconvert program in the NASA CDF distribution."""
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

    def cdfvalidate(self, file, program=None):
        """Run the cdfvalidate program in the NASA CDF distribution."""
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
        issues = Issue()

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
                issues.append("VALIDMIN", 'vatt', 'isentry', msg, False, varname=zvarname)

            if rec.max() > validmax:
                msg = ("[%i]: Record value(s) greater than VALIDMAX!") % (i)
                logger.warning(msg)
                issues.append("VALIDMAX", 'vatt', 'isentry', msg, False, varname=zvarname)

        return issues

    def flush_issues(self):
        """
        Reset issue object

        :return:
        """
        self.issues.reset()



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
