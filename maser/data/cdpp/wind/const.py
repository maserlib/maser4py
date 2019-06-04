#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to provide Wind/Waves constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.11"

__all__ = ["WIND_WAVES_RADIO_60S_META", "WIND_WAVES_TNR_L3_BQT_META", "WIND_WAVES_TNR_L3_NN_META"]

import astropy.units as u

# metadata block for each data set

WIND_WAVES_TNR_L3_NN_META = {
    "PLASMA_FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Plasma Frequency from Neural Network",
    },
    "ELEC_DENSITY": {
        "unit": u.Unit("1 / cm^3"),
        "description": "Electronic Density from Neural Network",
    },
}

WIND_WAVES_TNR_L3_BQT_META = {
    "PLASMA_FREQUENCY_NN": {
        "unit": u.Unit("kHz"),
        "description": "Plasma Frequency from Neural Network",
    },
    "PLASMA_FREQUENCY": {
        "unit": u.Unit("kHz"),
        "description": "Plasma Frequency from Fit",
    },
    "COLD_ELECTRONS_TEMPERATURE": {
        "unit": u.Unit("eV"),
        "description": "Cold Electron Temperature from Fit",
    },
    "ELECTRONIC_DENSITY_RATIO": {
        "unit": u.Unit("1 / cm^3") / u.Unit("1 / cm^3"),
        "description": "Electronic Density Ratio from Fit",
    },
    "ELECTRONIC_TEMPERATURE_RATIO": {
        "unit": u.Unit("eV") / u.Unit("eV"),
        "description": "Electronic Temperature Ratio from Fit",
    },
    "PROTON_TEMPERATURE": {
        "unit": u.Unit("eV"),
        "description": "Proton Temperature from 3DP",
    },
    "SOLAR_WIND_VELOCITY": {
        "unit": u.Unit("km/s"),
        "description": "Solar Wind Velocity from 3DP",
    },
    "FIT_ACCUR_PARAM_1": {
        "unit": "%",
        "description": "Fit Accuracy on PLASMA_FREQUENCY (0.0 if not fitted)",
    },
    "FIT_ACCUR_PARAM_2": {
        "unit": "%",
        "description": "Fit Accuracy on COLD_ELECTRONS_TEMPERATURE (0.0 if not fitted)",
    },
    "FIT_ACCUR_PARAM_3": {
        "unit": "%",
        "description": "Fit Accuracy on ELECTRONIC_DENSITY_RATIO (0.0 if not fitted)",
    },
    "FIT_ACCUR_PARAM_4": {
        "unit": "%",
        "description": "Fit Accuracy on ELECTRONIC_TEMPERATURE_RATIO (0.0 if not fitted)",
    },
    "FIT_ACCUR_PARAM_7": {
        "unit": "%",
        "description": "Fit Accuracy on PROTON_TEMPERATURE (0.0 if not fitted)",
    },
    "FIT_ACCUR_PARAM_8": {
        "unit": "%",
        "description": "Fit Accuracy on SOLAR_WIND_VELOCITY (0.0 if not fitted)",
    },
    "FIT_ACCUR_RMS": {
        "unit": "%",
        "description": "Root mean square between measured and fitted spectra",
    },
}

WIND_WAVES_RADIO_60S_META = {
    "FREQ": {
        "unit": u.Unit("kHz"),
        "description": "Frequency",
    },
    "INTENSITY": {
        "unit": u.Unit("uV^2/Hz"),
        "description": "Intensity",
    },
}