#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to provide ISEE3 constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.01"

__all__ = ["ISEE3_SBH_3D_RADIO_SOURCE_META"]

import astropy.units as u

# metadata block for each data set

ISEE3_SBH_3D_RADIO_SOURCE_META = {
    "FREQUENCY": {
        "unit": u.Unit("kHz"),
        "description": "Observed Frequency",
    },
    "BANDWIDTH": {
        "unit": u.Unit("kHz"),
        "description": "Spectral Bandwidth of S and Z receivers",
    },
    "DATA_QUALITY": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Quality of experimental data ( 1 = valid ; 0 = filler ) ",
    },
    "TIME": {
        "unit": u.Unit("s"),
        "description": "Time of step start relative to time of cycle start",
    },
    "S_DATA": {
        "unit": u.Unit("uV^2/Hz"),
        "description": "S receiver measurements",
    },
    "Z_DATA": {
        "unit": u.Unit("uV^2/Hz"),
        "description": "Z receiver measurements",
    },
    "PHI_DATA": {
        "unit": u.Unit("0.02 V"),
        "description": "Dephasing between S and Z signals, in TM unit ( = 0.02 V)",
    },
}