#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python script to modify CDF Excel template files
Required maser4py package https://pypi.org/project/maser4py/.
."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import argparse
from pathlib import Path
import json
import logging

from maser.utils.cdf.serializer import Skeleton

# ________________ HEADER _________________________

# Mandatory
__version__ = "0.3.0"
__author__ = "X.Bonnin"
__date__ = "2019-04-23" \
           ""

# Optional
__license__ = "MIT"
__credit__ = [""]
__maintainer__ = "X.Bonnin"
__email__ = ""
__project__ = "RPW Operations Centre"
__institute__ = "LESIA"
__changes__ = {"0.1.0": "First release",
               "0.2.0": "Add new change possibilities",
               "0.3.0": "Update to be consistent with new Skeleton instance"}


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CURDIR = os.curdir

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)

def rm_zvar(skeleton, zvars):
    """
    Remove zvariables

    :param: input Skeleton object to update
    :param zvars: list of zvariable(s) to remove
    :return: Updated Skeleton object
    """
    for zvar in zvars:
        skeleton.rm_zvar(zvar)
    return skeleton

def add_zvar(skeleton, zvars):
    """
    Add zVariables

    :param: input Skeleton object to update
    :param zvars: zVariables to add
    :return: Updated Skeleton object
    """
    for i, zvar in enumerate(zvars):
        if "Variable Attributes" in zvar:
            vattrs = zvar["Variable Attributes"]
        else:
            vattrs = None
        skeleton.add_zvar(zvar["Variable Name"], zvar, vattrs=vattrs)

    return skeleton

def rename_zvar(skeleton, zvars):
    """
    Add zVariables

    :param: input Skeleton object to update
    :param gattrs: list of zvars to rename
    :return: updated skeleton
    """

    for zvar in zvars:
        skeleton.rename_zvar(zvar["Variable Name"], zvar["New Variable Name"])
    return skeleton


def set_zvar(skeleton, zvars):
    """
    Update zVariable(s)

    :param skeleton: input Skeleton object to update
    :param zvars: list of zvars to update
    :return: updated skeleton
    """
    for zvar in zvars:
        skeleton.set_zvar(zvar["Variable Name"], zvar)
    return skeleton

def add_gattr(skeleton, gattrs):
    """
    Add g.attribute(s)

    :param: input Skeleton object to update
    :param gattrs: list of g.attribute(s) to add
    :return: updated skeleton
    """

    for gattr in gattrs:
        skeleton.add_gattr(gattr["Attribute Name"], reform_gattr(gattr))
    return skeleton


def rm_gattr(skeleton, gattrs):
    """
    Remove g.attribute(s)

    :param: input Skeleton object to update
    :param gattrs: list of g.attribute(s) to remove
    :return: updated skeleton
    """
    for gattr in gattrs:
        skeleton.rm_gattr(gattr)
    return skeleton

def rename_gattr(skeleton, gattrs):
    """
    Rename g.attribute(s)

    :param: input Skeleton object to update
    :param gattrs: list of g.attribute(s) to rename
    :return: updated skeleton
    """
    for gattr in gattrs:
        skeleton.rename_gattr(gattr["Attribute Name"], gattr["New Attribute Name"])
    return skeleton

def set_gattr(skeleton, gattrs):
    """
    Update g.attribute(s)

    :param skeleton: input Skeleton object to update
    :param gattrs: list of g.attribute(s) to update
    :return: updated skeleton
    """
    for gattr in gattrs:
        skeleton.set_gattr(gattr["Attribute Name"], gattr, add=True)
    return skeleton


def add_vattr(skeleton, vattrs):
    """
    Add v.attribute(s)

    :param: input Skeleton object to update
    :param vattrs: list of v.attribute(s) to add
    :return: updated skeleton
    """

    for vattr in vattrs:
        if "Variable Name" in vattr:
            varname = vattr["Variable Name"]
        else:
            varname = None
        skeleton.add_vattr(vattr["Attribute Name"], vattr,
                           varname=[varname])
    return skeleton


def rm_vattr(skeleton, vattrs):
    """
    Remove v.attribute(s)

    :param: input Skeleton object to update
    :param vattrs: list of v.attribute(s) to remove
    :return: updated skeleton
    """
    for vattr in vattrs:
        if "Variable Name" in vattr:
            varname = vattr["Variable Name"]
        else:
            varname = None
        skeleton.rm_vattr(vattr["Attribute Name"],
                          varname=[varname])
    return skeleton

def rename_vattr(skeleton, vattrs):
    """
    Rename v.attribute(s)

    :param: input Skeleton object to update
    :param vattrs: list of v.attribute(s) to remove
    :return: updated skeleton
    """
    for vattr in vattrs:
        if "Variable Name" in vattr:
            varname = vattr["Variable Name"]
        else:
            varname = None
        skeleton.rename_vattr(vattr["Attribute Name"], vattr["New Attribute Name"],
                              varname=[varname])
    return skeleton


def set_vattr(skeleton, vattrs):
    """
    Update v.attribute(s)

    :param skeleton: input Skeleton object to update
    :param vattrs: list of v.attribute(s) to update
    :return: updated skeleton
    """
    for vattr in vattrs:
        if "Variable Name" in vattr:
            varname = vattr["Variable Name"]
        else:
            varname = None
        skeleton.set_vattr(vattr["Attribute Name"], vattr, varname=[varname])
    return skeleton

def reform_gattr(gattr):
    """
    Re-format input gattr dictionary to be passed as an argument
    to the add_gattr method.

    :param gattr: gattr dictionary to re-format
    :return: re-formatted gattr
    """

    gattr_entries = []
    # Re-format for set_gattr method
    for i, value in enumerate(gattr["Value"]):
        gattr_entries.append(
            {"Attribute Name": gattr["Attribute Name"],
             "Entry Number": str(i+1),
             "Data Type": gattr["Data Type"],
             "Value": value
             }
        )

    return gattr_entries

def main():
    """Main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("setting", nargs=1, type=str,
                        help="JSON file or stream containing the CDF "
                        "header/attributes/zvariables to set")
    parser.add_argument("skeleton_files", type=Path, nargs='+',
                        help="CDF skeleton file(s) to update. Can be .skt or .xlsx format file(s).")
    parser.add_argument("-o", "--output-dir", nargs=1, type=Path,
                        default=[CURDIR], help="output directory")
    parser.add_argument("-O", "--overwrite", action='store_true',
                        help="Overwrite existing output file(s)")
    parser.add_argument("-F", "--force-add", action='store_true',
                        help="Force global attribute adding if not "
                        "found when setting is requested "
                        "(use CDF_CHAR data type by default).")

    args = parser.parse_args()
    outdir = args.output_dir[0]
    overwrite = args.overwrite

    if not outdir.is_dir():
        os.mkdir(outdir)
        print(f"{outdir} output directory created.")

    if os.path.isfile(args.setting[0]):
        with open(str(args.setting[0]), "r") as jfile:
            jdata = json.load(jfile)["update"]
    else:
        jdata = json.loads(args.setting[0])["update"]

    # Loop on input Excel files
    output = None
    for file in args.skeleton_files:

        if outdir is not None:
            output = outdir / file.name

        print(f"Processing {file}")

        # Instantiate the Skeleton class
        basename, extension = os.path.splitext(file)

        # Load skeleton content (Excel or skeleton table text file are accepted as input)
        if extension == ".skt":
            skeleton = Skeleton.from_txt(file)
        elif extension == ".xlsx":
            skeleton = Skeleton.from_xlsx(file)

        # Update the skeleton object content
        for key, val in jdata.items():
            try:
                func = getattr(sys.modules[__name__], key)
                skeleton = func(skeleton, val)
            except Exception as e:
                print("ERROR: {0}".format(e))

        if extension == ".skt":
            skeleton.to_txt(output, overwrite=overwrite)
        elif extension == ".xlsx":
            skeleton.to_xlsx(output, overwrite=overwrite)

    # _________________ Main ____________________________
if __name__ == "__main__":
    # print ""
    main()
