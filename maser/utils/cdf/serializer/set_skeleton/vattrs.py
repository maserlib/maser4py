#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module cdf.converter.tools.set_skeleton.vattrs."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf.serializer.exceptions import InvalidEntry

__all__ = ["add_vattr",
            "set_vattr",
            "rm_vattr"]

# ________________ HEADER _________________________



# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)


# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)


def add_vattr(skeleton, attname, entry, varname=None):
    """
    Add a variable attribute into the input skeleton object.

    :param skeleton: input skeleton object
    :
    :param attname: name of the v. attribute to add
    :param entry: List containing the entry for the v.attribute
    :param varname: If provided, contains a list of zvariable for which the v.attribute must be added. If not provided v.attribute is added for all the variables.
    :return: updated skeleton
    """

    if attname in skeleton.vattrList:
        logger.warning("{0} already exists!".format(attname))
    else:
        # Check that all the expected fields are in the input entries
        if not skeleton.is_valid_vattrs(entry):
            raise InvalidEntry

        skeleton.vattrList.append(attname)

        if not varname:
            varname = skeleton.vattrs.keys()
        else:
            for var in varname:
                if var not in skeleton.vattrs:
                    logger.error("{0} not found!".format(var))
                    raise InvalidEntry

        for zvar in varname:
            skeleton.vattrs[zvar][attname] = entry

    return skeleton


def set_vattr(skeleton, attname, entry, varname=None):
    """
    Set a given v.attribute

    :param skeleton: input skeleton object
    :
    :param attname: name of the v. attribute to add
    :param entry: List containing the entry for the v.attribute
    :param varname: If provided, contains a list of zvariable for which the v.attribute must be added. If not provided v.attribute is added for all the variables.
    :return: updated skeleton
    """

    # Check if the attribute already exists
    if attname not in skeleton.vattrList:
        logger.error(
            "{0} v.attribute does not exist!".format(
                attname))
        raise IOError
    else:
        if not skeleton.is_valid_vattrs(entry):
            raise InvalidEntry

        if not varname:
            varname = skeleton.vattrs.keys()
        else:
            for var in varname:
                if var not in skeleton.vattrs:
                    logger.error("{0} not found!".format(var))
                    raise InvalidEntry

        for var in varname:
            skeleton.vattrs[var][attname] = entry

    return skeleton


def rename_vattr(skeleton, old_attname, new_attname):
    """
    Rename a variable attr. from the input Skeleton object.

    :param skeleton:
    :param old_attname:
    :param new_attname:
    :return:
    """
    # Check if the zVariable already exists
    if old_attname not in skeleton.vattrList:
        logger.error(
                       "{0} v.attribute does not exist!".format(
                           old_attname))
        raise IOError
    else:
        skeleton.vattrList[new_attname] = skeleton.vattrList[old_attname]
        del skeleton.vattrList[old_attname]

        if old_attname in skeleton.vattrList:
            skeleton.vattrList[new_attname] = skeleton.vattrList[old_attname]
            del skeleton.vattrList[old_attname]

    # also check for each zvar
    for zvar, entry in skeleton.vattrs.items():
        if old_attname in entry:
            skeleton.vattrs[zvar][new_attname] = skeleton.vattrs[zvar][old_attname]
            del skeleton.vattrs[zvar][old_attname]

    return skeleton


def rm_vattr(skeleton, attname):
    """
    Remove a variable attr. from the input Skeleton object.

    :param skeleton:
    :param attname:
    :return:
    """
    if attname in skeleton.vattrList:
        del skeleton.vattrList[attname]

    # also check for each zvar
    for zvar, entry in skeleton.vattrs.items():
        if attname in entry:
            del skeleton.vattrs[zvar][attname]


def main():
    """Main program."""
    logger.info("This is the cdf.converter.tools.set_skeleton.vattrs module.")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
