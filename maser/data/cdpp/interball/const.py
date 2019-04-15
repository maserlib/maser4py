#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to provide Interball/POLRAD constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.01"

__all__ = ["INT_AUR_POLRAD_RSP_META", "INT_AUR_POLRAD_RSP_CSSDS_EPOCH"]

import astropy.units as u
import datetime

# metadata block for this dataset

INT_AUR_POLRAD_RSP_META = {
    "FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Frequency",
    },
    "EX": {
        "unit": u.Unit("W/(m^2 Hz)"),
        "description": "Flux Density on Antenna EX",
    },
    "EY": {
        "unit": u.Unit("W/(m^2 Hz)"),
        "description": "Flux Density on Antenna EY",
    },
    "EZ": {
        "unit": u.Unit("W/(m^2 Hz)"),
        "description": "Flux Density on Antenna EZ",
    },
}

# CCSDS CDS Level 2 Epoch for this dataset

INT_AUR_POLRAD_RSP_CSSDS_EPOCH = datetime.datetime(1950, 1, 1, 0, 0, 0)