#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS/PPI/Cassini/RPWS and PADC/LESIA/Cassini/Kronos datasets
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "0.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Development"
__date__ = "22-FEB-2017"
__project__ = "MASER/PDS PDS/Cassini/RPWS"

__ALL__ = ['agc_db', 'auto_db', 'cal1']

from pathlib import Path
import numpy
from scipy.io import readsav


def _load_constants():

    p = Path(__file__).parent / '..' / '..' / '..' / '..' / 'support' / 'data' / 'cassini_rpws_hfr_constants.xdr'
    data = readsav(str(p))
    return data['a1h1'], data['a1h2'], data['ai'], data['dbcal_abc'], data['dbcal_h']


def cal1(agc, auto, band, ant, freq, nfilters, ifilter, verbose=False, debug=False):
    """
    Converts [arrays of] (agc,auto) pairs into physical values (dB / Volts.Hz^-1/2)

    :param agc: AGC value(s)
    :param auto: Auto value(s)
    :param band: 0-4 (A,B,C,H1,H2)
    :param ant: 0-3 (+X,-X,Z,Dip)
    :param freq: frequency (kHz) for H1 and H2 only, 0 for ABC
    :param nfilters: 1,2,4,8,16,32 (nb of filter per band)
    :param ifilter: 0-31 (selected filter in band)
    :param verbose:
    :param debug:
    :return:
    """

    _a1h1, _a1h2, _ai, _dBcal_abc, _dBcal_h = _load_constants()

    if isinstance(agc, (list, tuple, numpy.ndarray)):
        ncal = len(agc)
    else:
        ncal = 1
        agc = numpy.array([agc], numpy.uint8)
        auto = numpy.array([auto], numpy.uint8)
        band = numpy.array([band], numpy.int8)
        ant = numpy.array([ant], numpy.int8)
        freq = numpy.array([freq], numpy.float16)
        nfilters = numpy.array([nfilters], numpy.int8)
        ifilter = numpy.array([ifilter], numpy.int8)

    a1 = numpy.zeros((ncal,), dtype=numpy.float32)
    a2 = numpy.zeros((ncal,), dtype=numpy.float32)
    a3 = numpy.zeros((ncal,), dtype=numpy.float32)
    att = numpy.zeros((ncal,), dtype=numpy.int8)
    dBcal = numpy.zeros((ncal,), dtype=numpy.float32)
    dB = numpy.zeros((ncal,), dtype=numpy.float32)

    iant = ant//3
    ifreq = freq

    for i in range(ncal):
        a1[i], a2[i], a3[i] = a123(att[i], band[i], iant[i])

    for cur_index, cur_band in enumerate(band):

        if cur_band > 2:

            if cur_band == 3:
                a1[cur_index] = _a1h1[att[cur_index], int(ifreq[cur_index] / 25), ant[cur_index]]
            else:
                a1[cur_index] = _a1h2[att[cur_index], int((ifreq[cur_index] - 25) / 50), ant[cur_index]]

            dBcal[cur_index] = _dBcal_h[int(numpy.log(nfilters[cur_index]) / numpy.log(2)),
                                        iant[cur_index], ifilter[cur_index]]
        else:
            dBcal[cur_index] = _dBcal_abc[int(numpy.log(nfilters[cur_index]) / numpy.log(2)) - 3,
                                          band[cur_index], ifilter[cur_index], ant[cur_index]]

    for cur_index in range(ncal):
        if agc[cur_index] != 255:
            dB[cur_index] = agc_dB(agc[cur_index], a1[cur_index], a2[cur_index], a3[cur_index],
                                   verbose=verbose, debug=debug)
        if auto[cur_index] != 255:
            dB[cur_index] += auto_dB(auto[cur_index], verbose=verbose, debug=debug) - dBcal[cur_index]

    return dB


def a123(att, band, iant):
    _, _, _ai, _, _= _load_constants()
    return _ai[att, band, iant, 0], _ai[att, band, iant, 1], _ai[att, band, iant, 2]


def agc_dB(agc,  a1, a2, a3, verbose=False, debug=False):
    """
    Converts raw AGC value into (dB / Volts.Hz^-1/2)
    :param agc: agc value (
    :param a1: agc calibration param #1
    :param a2: agc calibration param #2
    :param a3: agc calibration param #3
    :param verbose:
    :param debug:
    :return:
    """
    return -a1 + 40. * numpy.log10(1. + 10.**((agc - a3) / a2))


def auto_dB(auto, verbose=False, debug=False):
    """
    Converts raw Auto value into (dB / Volts.Hz^-1/2)
    :param auto: auto value (ADU)
    :param verbose:
    :param debug:
    :return:
    """
    return 10.*numpy.log10((8.+(auto & 0x07)) * 2.**((auto & 0xf8) >> 3))

