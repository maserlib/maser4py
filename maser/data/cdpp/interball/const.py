#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to provide Interball/POLRAD constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.01"

__all__ = ["INT_AUR_POLRAD_RSP_META"]

import astropy.units as u

# metadata block for each data set

INT_AUR_POLRAD_RSP_META = {
    "FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Frequency",
    },
    "EX": {
        "unit": u.Unit("W/m^2/Hz"),
        "description": "Flux Density on Antenna EX",
    },
    "EY": {
        "unit": u.Unit("W/m^2/Hz"),
        "description": "Flux Density on Antenna EY",
    },
    "EZ": {
        "unit": u.Unit("W/m^2/Hz"),
        "description": "Flux Density on Antenna EZ",
    },
}