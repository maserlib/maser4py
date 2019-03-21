#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to provide Interball/POLRAD constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.01"

__all__ = ["DMT_ICE_N1_1134_ORB_PARAM_META", "DMT_ICE_N1_1134_ATT_PARAM_META", "DMT_ICE_N1_1134_DATA_HEADER_META",
           "DMT_ICE_N1_1134_GEOMAG_PARAM_META", "DMT_ICE_N1_1134_POWER_SPECTRA_META",
           "DMT_ICE_N1_1134_SOLAR_PARAM_META"]

import astropy.units as u

# metadata block for this dataset

# BLOCK 2 Metadata

DMT_ICE_N1_1134_ORB_PARAM_META = {
    "GEOC_LAT": {
        "unit": u.Unit("deg"),
        "description": "Geocentric latitude (-90 deg to +90 deg) ",
    },
    "GEOC_LONG": {
        "unit": u.Unit("deg"),
        "description": "Geocentric longtitude (0 deg to 360 deg) ",
    },
    "ALTITUDE": {
        "unit": u.Unit("km"),
        "description": "Altitude",
    },
    "LOCAL_TIME": {
        "unit": u.Unit("hr"),
        "description": " Local time of the first point of the data array (0 to 24 h) ",
    },
}

DMT_ICE_N1_1134_GEOMAG_PARAM_META = {
    "GEOMAG_LAT": {
        "unit": u.Unit("deg"),
        "description": "Geomagnetic latitude (-90 deg to +90 deg)",
    },
    "GEOMAG_LONG": {
        "unit": u.Unit("deg"),
        "description": "Geomagnetic longtitude (0 deg to 360 deg)",
    },
    "MLT": {
        "unit": u.Unit("hr"),
        "description": "Magnetic local time of the first point",
    },
    "INV_LAT": {
        "unit": u.Unit("deg"),
        "description": "Invariant latitude (-90 deg to +90 deg)",
    },
    "MC_ILWAIN_L": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Mc Ilwain parameter L (0 , 999)",
    },
    "CONJSAT_GEOC_LAT": {
        "unit": u.Unit("deg"),
        "description": "Geocentric latitude of the conjugate point at the satellite altitude (-90 deg to +90 deg)",
    },
    "CONJSAT_GEOC_LONG": {
        "unit": u.Unit("deg"),
        "description": "Geocentric longitude of the conjugate point at the satellite altitude (0 deg to 360 deg)",
    },
    "NCONJ110_GEOC_LAT": {
        "unit": u.Unit("deg"),
        "description": "Geocentric latitude of North conjugate point at altitude 110 km (-90 deg to +90 deg)",
    },
    "NCONJ110_GEOC_LONG": {
        "unit": u.Unit('deg'),
        "description": "Geocentric longitude of North conjugate point at altitude 110 km (0 deg to 360 deg)",
    },
    "SCONJ110_GEOC_LAT": {
        "unit": u.Unit("deg"),
        "Definition": "Geocentric latitude of South conjugate point at altitude 110 km (-90 deg to +90 deg)",
    },
    "SCONJ110_GEOC_LONG": {
        "unit": u.Unit("deg"),
        "description": "Geocentric longitude of South conjugate point at altitude 110 km (0 deg to 360 deg)",
    },
    "B_FIELD_MODEL": {
        "unit": u.Unit("nT"),
        "description": "Components of the magnetic field model at the satellite point (geographic coordinate system)",
        "shape": (3,)
    },
    "GYROFREQ": {
        "unit": u.Unit("Hz"),
        "description": "Proton gyrofrequency at the satellite point",
    },
}

DMT_ICE_N1_1134_SOLAR_PARAM_META = {
    "SOLAR_POSITION": {
        "unit": u.Unit("AU"),
        "description": "Position",
        "shape": (3,)
    },
}

# BLOCK 3 Metadata

DMT_ICE_N1_1134_ATT_PARAM_META = {
    "M_SAT2GEO": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Matrix from satellite coordinate system to geographic coordinate system.",
        "shape": (3, 3)
    },
    "M_GEO2LGM": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Matrix from geographic coordinate system to local geomagnetic coordinate system.",
        "shape": (3, 3)
    },
    "QUALITY": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Quality index of the attitude parameters",
    }
}

# BLOCK 4 Metadata

DMT_ICE_N1_1134_DATA_HEADER_META = {
    "TOTAL_DUR": {
        "unit": u.Unit("s"),
        "description": "Total time duration of NB spectra: 16.384, 4.096 or 1.024 s",
    },
    "FREQ_RES": {
        "unit": u.Unit("kHz"),
        "description": "Frequency resolution (3.255 or 13.021 kHz)",
    },
    "LOWER_FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Lower frequency of the frequency range: 3.255 or 13.021 kHz",
    },
    "UPPER_FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Upper frequency of the frequency range: 3333.3333 kHz",
    },
}

DMT_ICE_N1_1134_POWER_SPECTRA_META = {
    "POWER": {
        "unit": u.LogUnit("uV^2/(m^2 Hz)"),
        "description": "Value of a Power spectrum array element",
    },
}