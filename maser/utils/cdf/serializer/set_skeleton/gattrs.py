#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module cdf.converter.tools.set_skeleton.gattr."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf.serializer.exceptions import InvalidEntry
from maser.utils.cdf.serializer.globals import SHEETS, GATTRS

__all__ = ["add_gattr",
            "set_gattr",
            "rm_gattr"]

# ________________ HEADER _________________________



# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

# ________________ Class Definition __________
# (If required, define here classes)


# ________________ Global Functions __________
# (If required, define here global functions)


def add_gattr(skeleton, attname, entries):
    """
    Add a global attribute into the input skeleton object.

    :param skeleton: input skeleton object
    :param attname: name of the g. attribute to add
    :param entries: List containing the entries for the g.attribute
    :return: updated skeleton
    """

    if attname in skeleton.gattrs:
        logger.warning("{0} already exists!".format(attname))
    else:
        # Check that all the expected fields are in the input entries
        if not skeleton.is_valid_gatt(entries):
            raise InvalidEntry

        skeleton.gattrs[attname] = entries

    return skeleton


def set_gattr(skeleton, attname, entries):
    """set_gattr.

    @author: X.Bonnin, LESIA, Obs. Paris, CNRS

    Update global attribute entries into the input CDF Excel skeleton.

    Positional arguments:
        set_skeleton - CDF Excel skeleton file
        attname - Name of the global attribute
        new_entries - dictionary containing the
                      entry indexes as keys and
                      entry values as values
                      (e.g. {"1":"value1", "2":value2})

    Optional keywords:
        output - Name of the output file
        overwrite - If true, then overwrite existing output file

    """
    # Check if the attribute already exists
    if attname not in skeleton.gattrs:
        logger.error(
            "{0} g.attribute does not exist!".format(
                attname))
        raise IOError
    else:
        if not skeleton.is_valid_gatt(entries):
            raise InvalidEntry

        skeleton.gattrs[attname] = entries

    return skeleton


def rename_gattr(skeleton, old_attname, new_attname):
    """
    Rename a global attr. from the input Skeleton object.

    :param skeleton:
    :param old_attname:
    :param new_attname:
    :return:
    """
    # Check if the zVariable already exists
    if old_attname not in skeleton.gattrs:
        logger.error(
                       "{0} g.attribute does not exist!".format(
                           old_attname))
        raise IOError
    else:
        skeleton.gattrs[new_attname] = skeleton.gattrs[old_attname]
        del skeleton.gattrs[old_attname]

        if old_attname in skeleton.vattrs:
            skeleton.gattrs[new_attname] = skeleton.gattrs[old_attname]
            del skeleton.gattrs[old_attname]

    return skeleton


def rm_gattr(skeleton, attname):
    """
    Remove a global attr. from the input Skeleton object.

    :param skeleton:
    :param attname:
    :return:
    """
    if attname in skeleton.gattrs:
        del skeleton.gattrs[attname]



def main():
    """Main program."""
    logger.info("This is the cdf.converter.tools.set_skeleton.gattrs module.")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
