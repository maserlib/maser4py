#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Constants of the maser.utils.time module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
from numpy import datetime64, timedelta64

__all__ = ["MJD_EPOCH",
           "JD_TO_MJD",
           "J2000_EPOCH",
           "TT2000_EPOCH",
           "DELTA_NSEC_TAI_TT"]

# ________________ HEADER _________________________

# # Mandatory
# __version__ = ""
# __author__ = ""
# __date__ = ""

# # Optional
# __license__ = ""
# __credit__ = [""]
# __maintainer__ = ""
# __email__ = ""
# __project__ = ""
# __institute__ = ""
# __changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

# Time conversion factors
SEC_TO_MICROSEC = 1000000
DAY_TO_SEC = 24 * 3600

# Modified Julian day (MDJ) epoch (0h Nov 17, 1858)
MJD_EPOCH = datetime64("1858-11-17T00:00")

# delta time in microsec betwen Julian day (JD) epoch (-4713, 1, 1 at 12h)
# and MDJ epoch
JD_TO_MJD = timedelta64(2400000 * DAY_TO_SEC * SEC_TO_MICROSEC, 'us') \
    + timedelta64(12 * 3600 * SEC_TO_MICROSEC, 'us')

# J2000 epoch
J2000_EPOCH = datetime64("2000-01-01T12:00")

# TT2000 epoch (including leap second)
TT2000_EPOCH = datetime64("2000-01-01T12:01:04.184")

# delta time in nanosec betwen TAI and TT times
# (TT = TAI + 32.184s; TT = UTC + delta_LeapSec + 32.184s)
DELTA_NSEC_TAI_TT = timedelta64(32184000000, 'ns')

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)

# _________________ Main ____________________________
# if (__name__ == "__main__"):
# print ""
# main()
