#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASER: SolO RPW tools module.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from .rpw import RpwException

__all__ = ["get_dataset_id"]

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
def get_dataset_id(cdf_data):
    """Get RPW dataset id from the cdf data."""
    if "DATASET_ID" in cdf_data.attrs:
        return cdf_data.attrs["DATASET_ID"][0]
    else:
        msg = "Input CDF has no DATASET_ID attribute!"
        logger.error(msg)
        raise RpwException(msg)


def main():
    """Main program."""
    print("maser.data.solo.rpw.tds.tools module")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
