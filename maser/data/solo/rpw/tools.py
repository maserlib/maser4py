#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASER: SolO RPW tools module.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging
import os

from ....utils.cdf.cdf import CDF

from .exception import RpwException

__all__ = ["get_dataset_id", "cdf_info", "file2cdf"]

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = "X.Bonnin"
__date__ = "2016-10-15"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = "MASER, RPW"
__institute__ = "LESIA, Obs.Paris, CNRS"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

logger = logging.getLogger(__name__)


# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)
def file2cdf(cdf):
    """Convert input CDF filepath string into CDF.CDF instance."""
    if type(cdf) == CDF.CDF:
        return cdf
    elif os.path.isfile(str(cdf)):
        return CDF.CDF(cdf)
    else:
        msg = "Unknown input cdf!"
        logger.error(msg)
        raise RpwException(msg)


def get_dataset_id(cdf_data):
    """Get RPW dataset id from the cdf data."""
    if "DATASET_ID" in cdf_data.attrs:
        return cdf_data.attrs["DATASET_ID"][0]
    else:
        msg = "Input CDF has no DATASET_ID attribute!"
        logger.error(msg)
        raise RpwException(msg)


def cdf_info(cdf):
    """Return cdf info."""
    return CDF.CDF(cdf)


def main():
    """Main program."""
    print("maser.data.solo.rpw.tds.tools module")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
