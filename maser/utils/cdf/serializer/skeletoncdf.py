#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________

"""skeletoncdf module.

Program to convert a CDF skeleton table into
a binary CDF ("master").

Skeleton/binary CDF can also be generated from
a formatted Excel skt_editor file.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import os.path as osp
import logging

from maser.utils.toolbox import which, run_command

from maser.utils.cdf.serializer.skeleton import Skeleton

# ________________ HEADER _________________________

__all__ = ["skeletoncdf"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)

# ________________ Class Definition __________
# (If required, define here classes)



def skeletoncdf(input_skt,
                output_dir=os.getcwd(),
                output_cdf=None,
                overwrite=False,
                excel_format=False,
                auto_pad=True,
                exe=None):
    """
    Make a CDF Master binary file from a ASCII
    skeleton table using the skeletoncdf program.

    If the "excel_format" keyword is True, then
    convert first the input Excel skeleton file into a valid CDF skeleton
    table.


    :param input_skt:
    :param output_dir: Path of the output directory
    :param overwrite:
    :param excel_format:
    :param auto_pad:
    :param exe:
    :return:
    """
    # If output_dir does not provide then use current one
    # If provided, but does not exist, then create it
    if not osp.isdir(output_dir):
        logger.warning(
                "{0} output directory not found, create it!".format(
                    output_dir))
        os.mkdir(output_dir)

    if excel_format:
        input_xlsx = input_skt
        logger.info("Converting {0} into skeleton table...".format(input_xlsx))
        skeleton = Skeleton.from_xlsx(input_skt, auto_pad=auto_pad)
        input_skt = skeleton.to_txt(output_path=output_dir,
                        overwrite=overwrite)
        if input_skt is None:
            input_skt = os.path.splitext(input_xlsx)[0] + ".skt"
            logger.error(
                "OUTPUT \"{0}\" HAS NOT BEEN SAVED!".format(input_skt))
            return None

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
