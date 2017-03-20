#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module for SOLO/RPW global variables.
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)

from .lfr import plotting as lfr_plt
from .tds import plotting as tds_plt

__all__ = ["RPW_PLOT_FUNC"]

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = ""
__date__ = ""

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = ""
__institute__ = ""
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

# RPW data plotting functions by DATASET ID
RPW_PLOT_FUNC = {
        "RPW-LFR-SURV-CWF": lfr_plt.plot_cwf,
        "RPW-LFR-SURV-SWF": lfr_plt.plot_swf,
        "RPW-TDS-LFM-CWF": tds_plt.plot_cwf,
        "RPW-TDS-SURV-RSWF": tds_plt.plot_swf,
        "RPW-TDS-SURV-TSWF": tds_plt.plot_swf,
}


# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)

# _________________ Main ____________________________
if (__name__ == "__main__"):
    #print ""
    main()
