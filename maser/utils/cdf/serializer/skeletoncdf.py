#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________

"""skeletoncdf module.

Program to convert a CDF skeleton table into
a binary CDF ("master").

Skeleton/binary CDF can also be generated from
a formatted Excel xlsx file.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import os.path as osp
from datetime import datetime
import logging

from ...toolbox import which, run_command

# ________________ HEADER _________________________

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)

CURRENT_DATETIME = datetime.now()
ROW_LENGTH_MAX = 79
DEF_INDENT = " " * 16

# Sheets and columns to be found in the Excel file
SHEET_NAMES = {
    "header": [
        "CDF NAME",
        "DATA ENCODING",
        "MAJORITY",
        "FORMAT"
    ],
    "GLOBALattributes": [
        "Attribute Name",
        "Entry Number",
        "Data Type",
        "Value"
    ],
    "zVariables": [
        "Variable Name",
        "Data Type",
        "Number Elements",
        "Dims",
        "Sizes",
        "Record Variance",
        "Dimension Variances"
    ],
    "VARIABLEattributes": [
        "Variable Name",
        "Attribute Name",
        "Data Type",
        "Value"
    ],
    "Options": [
        "CDF_COMPRESSION",
        "CDF_CHECKSUM",
        "VAR_COMPRESSION",
        "VAR_SPARESERECORDS",
        "VAR_PADVALUE"
    ],
    "NRV": [
        "Variable Name",
        "Index",
        "Value"
    ]
}




# ________________ Class Definition __________
# (If required, define here classes)



def skeletoncdf(input_skt,
                output_cdf=None,
                output_dir=None,
                overwrite=False,
                from_xlsx=None,
                ignore_none=True,
                auto_pad=True,
                exe=None):
    """make_cdf.

    Make a CDF Master binary file from a ASCII
    skeleton table using the skeletoncdf program.

    If the "fom_xlsx" keyword is True, then
    convert first the input Excel skeleton file into a valid CDF skeleton
    table.
    """
    if from_xlsx:
        input_xlsx = input_skt
        logger.info("Converting {0} into skeleton table...".format(input_xlsx))
        input_skt = Xlsx2skt.convert(input_xlsx,
                                     output_dir=output_dir,
                                     overwrite=overwrite,
                                     ignore_none=ignore_none,
                                     auto_pad=auto_pad)
        if input_skt is None:
            input_skt = os.path.splitext(input_xlsx)[0] + ".skt"
            logger.error(
                "OUTPUT \"{0}\" HAS NOT BEEN SAVED!".format(input_skt))
            return None

    # If output_dir does not provide then use current one
    # If provided, but does not exist, then create it
    if output_dir is None:
        output_dir = os.getcwd()
    else:
        if not osp.isdir(output_dir):
            logger.warning(
                "{0} output directory not found, create it!".format(
                    output_dir))
            os.mkdir(output_dir)

    # Set output_cdf file path
    if output_cdf is None:
        output_cdf = osp.splitext(input_skt)[0] + ".cdf"
    else:
        output_cdf = osp.join(output_dir, os.path.basename(output_cdf))

    # Initialize command line
    cmd = []

    # If skeletoncdf program path is not provided
    # then search it on the $PATH
    if exe is None:
        if "CDF_BIN" in os.environ:
            exe = osp.join(os.environ["CDF_BIN"], "skeletoncdf")
        else:
            exe = which('skeletoncdf')
    if exe is None:
        logger.error("skeletoncdf program is not callable!")
        return None
    cmd.append(exe)
    if os.path.isfile(output_cdf) and overwrite:
        logger.warning("%s existing file will be overwritten!",
                       output_cdf)
        cmd.append("-delete")
    cmd.append(input_skt)
    cmd.extend(["-cdf", output_cdf])
    myenv = os.environ.copy()
    logger.info("Executing {0}...".format(" ".join(cmd)))
    res = run_command(cmd, env=myenv)
    output, errors = res.communicate()
    if res.wait() == 0:
        logger.debug(output)
        if os.path.isfile(output_cdf):
            logger.info(output_cdf + " has been saved correctly!")
            return output_cdf
        else:
            logger.error(output_cdf + " has not been saved correctly!")
    else:
        logger.error("ERROR RUNNING COMMAND: ")
        logger.error(" ".join(cmd))
        logger.error("STDOUT - %s", str(output))
        logger.error("STDERR - %s", str(errors))
        logger.error("OUTPUT \"{0}\" HAS NOT BEEN SAVED!".format(output_cdf))

    return None


# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)
