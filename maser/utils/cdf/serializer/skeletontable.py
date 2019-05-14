#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________

"""skeletontable module.

Program to convert a CDF file into
a skeleton table.

Skeleton table can also be saved into a Excel 2007 format file.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import os.path as osp
import logging

from maser.utils.toolbox import which, run_command

from maser.utils.cdf.serializer.skeleton import Skeleton

# ________________ HEADER _________________________

__all__ = ["skeletontable"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

# ________________ Class Definition __________
# (If required, define here classes)


def skeletontable(input_cdf,
                output_dir=os.getcwd(),
                output_skt=None,
                overwrite=False,
                to_xlsx=False,
                exe=None,
                ):
    """
    Make a skeleton table file from an input CDF file
    using the skeletontable program of the NASA CDF software.

    If the "excel_format" keyword is True, then
    the skeleton table is also saved into an Excel 2007 format file.

    :param input_cdf: Input CDF file to convert
    :param output_dir: Path of the output directory
    :param output_skt: Output skeleton file
    :param overwrite: If True, overwrite existing output file
    :param to_xlsx: If True, also save the skeleton table in an Excel 2007 format file
    :param exe: Path to the "skeletontable" executable
    :return:
    """

    # If output_dir does not provide then use current one
    # If provided, but does not exist, then create it
    if not osp.isdir(output_dir):
        logger.warning(
                "{0} output directory not found, create it!".format(
                    output_dir))
        os.mkdir(output_dir)

    # Get basename, extension of the input CDF
    basename, extension = os.path.splitext(input_cdf)

    # Set output_skt file path
    if output_skt is None:
        output_skt = osp.basename(basename) + ".skt"

    output_skt = osp.join(output_dir, os.path.basename(output_skt))

    # If input file is already a skeleton then skip this step
    if extension != ".skt":

        # Initialize command line
        cmd = []

        # If skeletontable program path is not provided
        # then search it on the $PATH
        if exe is None:
            if "CDF_BIN" in os.environ:
                exe = osp.join(os.environ["CDF_BIN"], "skeletontable")
            else:
                exe = which('skeletontable')
        if exe is None:
            logger.error("skeletontable program is not callable!")
            return None
        cmd.append(exe)
        if os.path.isfile(output_skt) and overwrite:
            logger.warning("%s existing file will be overwritten!",
                           output_skt)
            cmd.append("-delete")
        cmd.append(input_cdf)
        cmd.extend(["-skeleton", os.path.splitext(output_skt)[0]])
        myenv = os.environ.copy()
        logger.info("Executing {0}...".format(" ".join(cmd)))
        res = run_command(cmd, env=myenv)
        output, errors = res.communicate()
        if res.wait() == 0:
            logger.debug(output)
            if os.path.isfile(output_skt):
                logger.info("{0} has been saved correctly!".format(output_skt))
                input_skt = output_skt
            else:
                logger.error("{0} has not been saved correctly!".format(output_skt))
                return None
        else:
            logger.error("ERROR RUNNING COMMAND: ")
            logger.error(" ".join(cmd))
            logger.error("STDOUT - %s", str(output))
            logger.error("STDERR - %s", str(errors))
            logger.error("OUTPUT \"{0}\" HAS NOT BEEN SAVED!".format(output_skt))
            return None
    else:
        logger.warning("Input CDF seems to be already a skeleton table ({0})".format(
            input_cdf))
        input_skt = input_cdf

    # if requested, also save as an Excel file
    if to_xlsx:
        skeleton = Skeleton.from_txt(input_skt)
        output_xlsx = os.path.join(output_dir,
            os.path.basename(os.path.splitext(input_skt)[0] + ".xlsx"))
        skeleton.to_xlsx(output_xlsx)
        if os.path.isfile(output_xlsx):
            logger.info("{0} has been saved correctly!".format(output_xlsx))
        else:
            logger.error("{0} has not been saved correctly!".format(output_xlsx))

    return output_skt