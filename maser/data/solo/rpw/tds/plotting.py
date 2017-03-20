#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""RPW TDS plotting module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

import numpy as np
import matplotlib.pyplot as plt

from .....utils.cdf import CDF
from ..tools import file2cdf

__all__ = ["plot_swf", "plot_cwf"]

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
__project__ = "MASER"
__institute__ = "LESIA, Obs.Paris, CNRS"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

logger = logging.getLogger(__name__)


# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)
# ________________ Global Functions __________
# (If required, define here gobal functions)
def plot_cwf(cdf, channel=[1, 2, 3, 4],
             xmin=None, xmax=None,
             ymin=None, ymax=None,
             no_fillval=False,
             no_time=False):
    """Plot TDS RSWF data."""
    cdf_data = file2cdf(cdf)

    cwf = cdf_data["WAVEFORM_DATA"][:, :]
    epoch = cdf_data["Epoch"][:]

    nrec = cdf_data["Epoch"].shape[0]
    logger.debug("{0} record(s)/sample(s)".format(nrec))

    if no_time:
        time = np.arange(nrec)
        plt.xlabel("Count")
    else:
        time = epoch
        plt.xlabel("{0} {1}".format(
                    cdf_data["Epoch"].attrs["LABLAXIS"],
                    cdf_data["Epoch"].attrs["UNITS"]))

    fillval = cdf_data["WAVEFORM_DATA"].attrs["FILLVAL"]

    if xmin is None:
        xmin = np.min(time)
    if xmax is None:
        xmax = np.max(time)
    if ymin is None:
        ymin = cdf_data["WAVEFORM_DATA"].attrs["SCALEMIN"]
    if ymax is None:
        ymax = cdf_data["WAVEFORM_DATA"].attrs["SCALEMAX"]

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.title(cdf_data.attrs["DATASET_ID"])
    plt.figure(1)
    subid = 100 * len(channel) + 11
    for i, ch in enumerate(channel):
        plt.subplot(subid + i)
        if no_fillval:
            w = np.where(cwf[ch - 1, :] != fillval)
            y = cwf[ch - 1, :][w]
            x = time[w]
        else:
            y = cwf[ch - 1, :]
            x = time

        plt.ylabel("{0} ({1})".format(
                            cdf_data["WAVEFORM_LABEL"][ch - 1],
                            cdf_data["WAVEFORM_DATA"].attrs["UNITS"]))
        plt.plot(x, y, 'k')

    plt.show()


def plot_swf(cdf, snapshot_nr=0, channel=[1, 2, 3, 4],
             xmin=None, xmax=None,
             ymin=None, ymax=None,
             no_fillval=False,
             no_time=False):
    """Plot TDS RSWF data."""
    if type(cdf) == CDF.CDF:
        cdf_data = cdf
    else:
        cdf_data = CDF.CDF(cdf)

    swf = cdf_data["WAVEFORM_DATA"][snapshot_nr, :, :]
    # epoch = cdf_data["Epoch"][snapshot_nr]
    dtime = cdf_data["SAMP_DTIME"][snapshot_nr, :]

    nrec = cdf_data["Epoch"].shape[0]
    nsamp = swf.shape[1]
    logger.debug("{0} record(s)/snapshot(s)".format(nrec))

    if no_time:
        time = np.arange(nsamp)
        plt.xlabel("Count")
    else:
        time = dtime
        plt.xlabel("{0} {1}".format(
                    cdf_data["SAMP_DTIME"].attrs["LABLAXIS"],
                    cdf_data["SAMP_DTIME"].attrs["UNITS"]))

    if xmin is None:
        xmin = np.min(time)
    if xmax is None:
        xmax = np.max(time)
    if ymin is None:
        ymin = cdf_data["WAVEFORM_DATA"].attrs["SCALEMIN"]
    if ymax is None:
        ymax = cdf_data["WAVEFORM_DATA"].attrs["SCALEMAX"]

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    fillval = cdf_data["WAVEFORM_DATA"].attrs["FILLVAL"]

    plt.title(cdf_data.attrs["DATASET_ID"])
    plt.figure(1)
    subid = 100 * len(channel) + 11
    for i, ch in enumerate(channel):
        plt.subplot(subid + i)
        if no_fillval:
            w = np.where(swf[ch - 1, :] != fillval)
            y = swf[ch - 1, :][w]
            x = time[w]
        else:
            y = swf[ch - 1, :]
            x = time

        plt.ylabel("{0} ({1})".format(
                            cdf_data["WAVEFORM_LABEL"][ch - 1],
                            cdf_data["WAVEFORM_DATA"].attrs["UNITS"]))
        plt.plot(x, y, 'k')

    plt.show()


def main():
    """Main program."""
    print("maser.data.solo.rpw.tds.plotting module")

# _________________ Main ____________________________
if (__name__ == "__main__"):
    main()
