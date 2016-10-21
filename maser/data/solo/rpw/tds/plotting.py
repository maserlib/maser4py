#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
RPW TDS plotting module.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import argparse
import os.path as osp
import logging

import numpy as np
from spacepy import pycdf
import matplotlib.pyplot as plt

from .tds import TdsException
from ..tools import get_dataset_id

__all__ = ["plot_swf"]

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
             xrange=None, yrange=None, no_fillval=False,
             no_time=False):
    """Plot TDS RSWF data."""
    if type(cdf) == pycdf.CDF:
        cdf_data = cdf
    else:
        cdf_data = pycdf.CDF(cdf)

    swf = cdf_data["WAVEFORM_DATA"][snapshot_nr, :, :]
    epoch = cdf_data["Epoch"][snapshot_nr]
    dtime = cdf_data["SAMP_DTIME"][snapshot_nr, :]

    nrec = cdf_data["Epoch"].shape[0]
    nsamp = swf.shape[1]
    logger.debug("{0} record(s)/snapshot(s)".format(nrec))

    if no_time:
        time = np.arange(nsamp)
    else:
        time = dtime

    fillval = cdf_data["WAVEFORM_DATA"].attrs["FILLVAL"]

    plt.figure(1)
    subid = 100 * len(channel) + 11
    for i, ch in enumerate(channel):
        #print(subid + i)
        plt.subplot(subid + i)
        if no_fillval:
            w = np.where(swf[ch - 1, :] != fillval)
            y = swf[ch - 1, :][w]
            x = time[w]
        else:
            y = swf[ch - 1, :]
            x = time
        plt.plot(x, y, 'k')

    plt.show()



def plot_swf(cdf, snapshot_nr=0, channel=[1, 2, 3, 4],
             xmin=None, xmax=None,
             ymin=None, ymax=None,
             no_fillval=False,
             no_time=False):
    """Plot TDS RSWF data."""
    if type(cdf) == pycdf.CDF:
        cdf_data = cdf
    else:
        cdf_data = pycdf.CDF(cdf)

    swf = cdf_data["WAVEFORM_DATA"][snapshot_nr, :, :]
    epoch = cdf_data["Epoch"][snapshot_nr]
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
                    cdf_data["SAMP_DTIME"].attrs("LABLAXIS")
                    cdf_data["SAMP_DTIME"].attrs("UNITS"))

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

    plt.figure(1)
    subid = 100 * len(channel) + 11
    for i, ch in enumerate(channel):
        #print(subid + i)
        plt.subplot(subid + i)
        if no_fillval:
            w = np.where(swf[ch - 1, :] != fillval)
            y = swf[ch - 1, :][w]
            x = time[w]
        else:
            y = swf[ch - 1, :]
            x = time

        plt.ylabel("Amplitude (channel #{0})".format(
                            ch))
        plt.plot(x, y, 'k')

    plt.show()


def main():
    """Main program."""
    parser = argparse.ArgumentParser(add_help=True,
                                     description='RPW TDS plotting module')
    parser.add_argument("cdf_file", nargs=1, type=str,
                        help="TDS CDF file to plot")
    parser.add_argument("-s", "--snapshot", nargs=1, type=int,
                        help="Snapshot index number", default=0)
    parser.add_argument("-c", "--channel", nargs="+", type=int,
                        help="Channel number", default=[1, 2, 3, 4])
    args = parser.parse_args()

    cdf_file = args.cdf_file[0]
    if not osp.isfile(cdf_file):
        msg = "Input CDF file not found [{0}]!".format(cdf_file)
        logger.error(msg)
        raise TdsException(msg)
    else:
        cdf_data = pycdf.CDF(cdf_file)

    ds_id = get_dataset_id(cdf_data)
    if "RPW-TDS" in ds_id and "RSWF":
        plot_swf(cdf_data,
                 snapshot_nr=args.snapshot[0],
                 channel=args.channel)
    elif "RPW-TDS" in ds_id and "TSWF":
        plot_swf(cdf_data,
                 snapshot_nr=args.snapshot[0],
                 channel=args.channel)

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
