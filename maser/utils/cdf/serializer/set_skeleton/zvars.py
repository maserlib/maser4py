#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module cdf.converter.tools.set_skeleton.zvars."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf.serializer.exceptions import InvalidEntry
from maser.utils.cdf.serializer.globals import SHEETS, ZVARS

__all__ = ["add_zvar",
            "set_zvar",
            "rm_zvar",
            "rename_zvar"]

# ________________ HEADER _________________________



# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)


# ________________ Class Definition __________
# (If required, define here classes)
class zVarException(Exception):
    pass

# ________________ Global Functions __________
# (If required, define here global functions)

def add_zvar(skeleton, varname, entry, vattrs=None):
    """
    Add a zVariable into the input skeleton object.

    :param skeleton: skeleton object to update
    ;param varname: name of the zVariable to add
    :param entry: list with fields to add [variable name, data type, number elements,
                dims, sizes, record variance, Dimension variances]. If dims=0, sizes and record variance must be None
    :param vattrs: dictionnary containing variable attribute(s) to load for this zvariable
    :return:
    """

    # Check if the zVariable already exists
    if varname in skeleton.zvars:
        logger.warning(
                       "{0} variable already exists!".format(
                                                    varname))
    else:
        # Check content
        if not skeleton.is_valid_zvar(entry):
            raise InvalidEntry
        # Add the zvariable
        skeleton.zvars[varname] = entry

        if vattrs:
            if not skeleton.is_valid_vattr(vattrs):
                raise InvalidEntry

            skeleton.vattrs[varname] = vattrs

    return skeleton


def set_zvar(skeleton, varname, entry, vattrs=None):
    """set_zvar.
    Update zvariable entry into the input CDF Excel skeleton.

    """

    # Check if the zVariable already exists
    if varname not in skeleton.zvars:
        logger.error(
                       "{0} variable does not exist!".format(
                                                    varname))
        raise IOError
    else:
        # update the zvariable

        for field in SHEETS[ZVARS]:
            if field in entry:
                skeleton.zvars[varname][field] = entry[field]
            else:
                continue

        if vattrs:
            if varname not in skeleton.vattrs:
                logger.error(
                    "{0} variable has no variable attribute!".format(
                        varname))
                raise IOError
            else:
                for key, val in vattrs.items():
                    skeleton.vattrs[varname][key] = val

    return skeleton


def rename_zvar(skeleton, old_varname, new_varname):
    """rename_zvar.

    Rename a variable from the input CDF Excel skeleton file.
    (By default a new file is created.)

    """
    # Check if the zVariable already exists
    if old_varname not in skeleton.zvars:
        logger.error(
                       "{0} variable does not exist!".format(
                           old_varname))
        raise IOError
    else:
        skeleton.zvars[new_varname] = skeleton.zvars[old_varname]
        del skeleton.zvars[old_varname]

        if old_varname in skeleton.vattrs:
            skeleton.vattrs[new_varname] = skeleton.vattrs[old_varname]
            del skeleton.vattrs[old_varname]

    return skeleton

def rm_zvar(skeleton, varname):
    """rm_zvar.

    Remove a variable from the input skeleton object.
    """

    if varname in skeleton.zvar:
        del skeleton.zvars[varname]

    if varname in skeleton.vattrs:
        del skeleton.vattrs[varname]

# _________________ Main ____________________________
if (__name__ == "__main__"):
    print(__file__)
