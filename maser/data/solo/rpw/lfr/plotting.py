#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""RPW LFR plotting module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging
import os

import numpy as np
from .....utils.cdf.cdf import CDF
import matplotlib.pyplot as plt

from ..tools import file2cdf

__all__ = ["plot_swf", "plot_cwf"]

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = "X.Bonnin"
__date__ = "2016-11-23"

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
def plot_cwf(cdf, component, freq=[1, 2, 3],
             xmin=None, xmax=None,
             ymin=None, ymax=None,
             no_fillval=False,
             no_time=False):
    """Plot LFR CWF data."""
    cdf_data = file2cdf(cdf)

    if type(component) is list:
        component = str(component[0])
    if component is None:
        logger.warning("Input component is None, use component=\"V\"!")

    epoch = cdf_data["Epoch"][:]
    nrec = cdf_data["Epoch"].shape[0]
    logger.debug("{0} record(s)/sample(s)".format(nrec))

    freq = cdf_data["FREQ"][:].astype(int)

    # 2 E-compenents
    component = component.upper()
    if component == "E":
        cwf = cdf_data["E"][:, :]
    elif component == "V":
        cwf = cdf_data["B"][:, :]
    elif component == "B":
        cwf = cdf_data["V"][:].reshape([nrec, 1])
    else:
        logger.error("Unknown compenent (must be \"V\",\"E\" or \"B\")!")

    if no_time:
        time = np.arange(nrec)
        plt.xlabel("Count")
    else:
        time = epoch
        plt.xlabel("{0} {1}".format(
                    cdf_data["Epoch"].attrs["LABLAXIS"],
                    cdf_data["Epoch"].attrs["UNITS"]))

    fillval = cdf_data[component].attrs["FILLVAL"]

    if xmin is None:
        xmin = np.min(time)
    if xmax is None:
        xmax = np.max(time)
    if ymin is None:
        ymin = cdf_data[component].attrs["SCALEMIN"]
    if ymax is None:
        ymax = cdf_data[component].attrs["SCALEMAX"]

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.title(cdf_data.attrs["DATASET_ID"])
    plt.figure(1)

    ndims = cwf.shape[-1]

    subid = 100 * len(freq) + 11
    for i, f in enumerate(freq):
        plt.subplot(subid + i)

        for j in range(ndims):
            w = np.where(np.int(f) == freq)
            if not w:
                logger.warning("No sample for FREQ{0}".format(f))
                continue
            else:
                y = cwf[:, j][w]
                x = time[w]

            if no_fillval:
                w = np.where(y != fillval)
                y = y[w]
                x = x[w]

            plt.ylabel("{0} ({1})".format(
                            component + str(j), # TODO: Add component label
                            cdf_data[component].attrs["UNITS"]))
            plt.plot(x, y, 'k')

    plt.show()


def plot_swf(cdf, snapshot_nr=0, channel=[1, 2, 3, 4],
             xmin=None, xmax=None,
             ymin=None, ymax=None,
             no_fillval=False,
             no_time=False):
    """Plot LFR SWF data."""
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
