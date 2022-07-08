# -*- coding: utf-8 -*-

"""
Python module to provide Viking constant variables.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "15-NOV-2018"
__version__ = "0.01"

__all__ = [
    "VIKING_V1_META",
    "VIKING_V4H_SFA_META",
    "VIKING_V4H_FB_META",
    "VIKING_V4L_FBL_PHYS_META",
    "VIKING_V4L_FBL_DB_META",
    "VIKING_V2_META",
    "VIKING_V4L_NI_META",
    "VIKING_V4L_DFT_PHYS_META",
    "VIKING_V4L_DFT_DB_META",
    "VIKING_V4L_WF_PHYS_META",
    "VIKING_V4L_WF_DB_META",
]

import astropy.units as u

# metadata block for each data set

VIKING_V1_META = {
    "V1_RELATIVE_TIME": {
        "unit": u.Unit("s"),
        "description": "Time relative to the beginning of record",
    },
    "V1_EPAR": {
        "unit": u.Unit("mV/m"),
        "description": "Electric field component parallel to B (magnetic field)",
    },
    "V1_EC": {
        "unit": u.Unit("mV/m"),
        "description": "Electric field component along the direction that completes the coordinate system (PAR, C, D)",
    },
    "V1_ED": {
        "unit": u.Unit("mV/m"),
        "description": "Electric field component perpendiculer to B and S (sun direction), positive along B x S",
    },
    "V1_VFG": {
        "unit": u.Unit("V"),
        "description": "Floating ground potential",
    },
    "V1_EPDIFF": {
        "unit": u.Unit("mV/m"),
        "description": "Difference between max and min electric field magnitude during the following 1.2 seconds",
    },
    "V1_USER_BIAS": {
        "unit": u.Unit("uA"),
        "description": "Bias current",
    },
    "V1_VGUARD": {
        "unit": u.Unit("V"),
        "description": "Guard potential",
    },
    "V1_IFILL": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Status bits",
    },
    "V1_ID": {
        "unit": u.Unit(u.dimensionless_unscaled),
        "description": "Not Used",
    },
}

VIKING_V4H_SFA_META = {
    "FREQUENCY_SFA": {
        "unit": u.Unit("kHz"),
        "description": "Stepped frequencies of the current scanning",
    },
    "ELECTRIC_SFA": {
        "unit": u.Unit("mV^2/(m^2 Hz)"),
        "description": "SFA measurements for an electric field component, either Ey or Ez",
    },
    "MAGNETIC_SFA": {
        "unit": u.Unit("pT^2/Hz"),
        "description": "SFA measurements for the magnetic field component Bx",
    },
}

VIKING_V4H_FB_META = {
    "FREQUENCY_FB": {
        "unit": u.Unit("kHz"),
        "description": "Center frequencies",
    },
    "MAGNETIC_FB": {
        "unit": u.Unit("pT"),
        "description": "Measurements for the magnetic field sensor Bx",
    },
    "ELECTRIC_FB": {
        "unit": u.Unit("mV/m"),
        "description": "Measurements for the electric field sensor Ey",
    },
}

VIKING_V4L_FBL_PHYS_META = {
    "FREQUENCY_FBL": {
        "unit": u.Unit("Hz"),
        "description": "Center frequencies",
    },
    "ELECTRIC_FBL": {
        "unit": u.Unit("mV/m"),
        "description": "Measurements for the electric field sensor",
    },
}

VIKING_V4L_FBL_DB_META = {
    "FREQUENCY_FBL": {
        "unit": u.Unit("Hz"),
        "description": "Center frequencies",
    },
    "ELECTRIC_FBL": {
        "unit": u.Unit("dB"),
        "description": "Measurements for the electric field sensor",
    },
}

VIKING_V2_META = {
    "V2_AMPLITUDE": {
        "unit": u.Unit("nT"),
        "description": "Magnetic field module",
    },
    "V2_PSI": {
        "unit": u.Unit("deg"),
        "description": "Angle between Ey antenna and the projection of magnetic field in the plane perpendicular "
        "to satellite spin axis",
    },
    "V2_PHI": {
        "unit": u.Unit("deg"),
        "description": "Angle between magnetic field and Ey antenna",
    },
    "V2_THETA": {
        "unit": u.Unit("deg"),
        "description": "Angle between magnetic field and satellite spin axis",
    },
}

VIKING_V4L_NI_META = {
    "N1_PROBE": {
        "unit": u.Unit("cm^-3"),
        "description": "Plasma density measurements supplied by N1 probe",
    },
    "N2_PROBE": {
        "unit": u.Unit("cm^-3"),
        "description": "Plasma density measurements supplied by N2 probe",
    },
}

VIKING_V4L_DFT_PHYS_META = {
    "DFT": {
        "unit": u.Unit("mV^2/(m^2 Hz)"),
        "description": "DFT power spectra",
    },
}

VIKING_V4L_DFT_DB_META = {
    "DFT": {
        "unit": u.Unit("dB"),
        "description": "DFT power spectra",
    },
}

VIKING_V4L_WF_PHYS_META = {
    "WF1": {
        "unit": u.Unit("mV/m"),
        "description": "Electric field waveform measurement",
    },
    "WF2": {
        "unit": u.Unit("mV/m"),
        "description": "Electric field waveform measurement",
    },
}

VIKING_V4L_WF_DB_META = {
    "WF1": {
        "unit": u.Unit("dB"),
        "description": "Electric field waveform measurement",
    },
    "WF2": {
        "unit": u.Unit("dB"),
        "description": "Electric field waveform measurement",
    },
}
