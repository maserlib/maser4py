#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module providing additional tools for the CDF format handling
"""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf import const, zAttr
import numpy
import csv

# ________________ HEADER _________________________

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

# ________________ Global Functions __________
# (If required, define here gobal functions)


def get_cdftype(dtype):
    """
        Return the id of a cdf data type,
        prividing the CDF data type.
    """
    return const.__dict__[dtype].value




def get_cdftypename(dtype=None):
    """
        Return the CDF type name of a given cdf cdf type
        Return the full CDF data type dictionnary if no input
        argument is provided.
    """
    cdftypenames = {
        const.CDF_BYTE.value: 'CDF_BYTE',
        const.CDF_CHAR.value: 'CDF_CHAR',
        const.CDF_INT1.value: 'CDF_INT1',
        const.CDF_UCHAR.value: 'CDF_UCHAR',
        const.CDF_UINT1.value: 'CDF_UINT1',
        const.CDF_INT2.value: 'CDF_INT2',
        const.CDF_UINT2.value: 'CDF_UINT2',
        const.CDF_INT4.value: 'CDF_INT4',
        const.CDF_UINT4.value: 'CDF_UINT4',
        const.CDF_INT8.value: 'CDF_INT8',
        const.CDF_FLOAT.value: 'CDF_FLOAT',
        const.CDF_REAL4.value: 'CDF_REAL4',
        const.CDF_DOUBLE.value: 'CDF_DOUBLE',
        const.CDF_REAL8.value: 'CDF_REAL8',
        const.CDF_EPOCH.value: 'CDF_EPOCH',
        const.CDF_EPOCH16.value: 'CDF_EPOCH16',
        const.CDF_TIME_TT2000.value: 'CDF_TIME_TT2000'}

    if dtype is None:
        return cdftypenames
    else:
        return cdftypenames[dtype]


def get_numpttype(dtype=None):
    """
        Return the numpy data type from a given cdf data type.
        Return the full numpy data type dictionnary if no input
        argument is provided.
    """

    numpytypedict = {
        const.CDF_BYTE.value: numpy.int8,
        const.CDF_CHAR.value: numpy.int8,
        const.CDF_INT1.value: numpy.int8,
        const.CDF_UCHAR.value: numpy.uint8,
        const.CDF_UINT1.value: numpy.uint8,
        const.CDF_INT2.value: numpy.int16,
        const.CDF_UINT2.value: numpy.uint16,
        const.CDF_INT4.value: numpy.int32,
        const.CDF_UINT4.value: numpy.uint32,
        const.CDF_INT8.value: numpy.int64,
        const.CDF_FLOAT.value: numpy.float32,
        const.CDF_REAL4.value: numpy.float32,
        const.CDF_DOUBLE.value: numpy.float64,
        const.CDF_REAL8.value: numpy.float64,
        const.CDF_EPOCH.value: numpy.float64,
        const.CDF_EPOCH16.value:
        numpy.dtype((numpy.float64, 2)),
        const.CDF_TIME_TT2000.value: numpy.int64}

    if dtype is None:
        return numpytypedict
    else:
        return numpytypedict[dtype]


def get_vattrs(cdf):

    """
    Retrieve the list of zVariables attributes
    from a given cdf object
    """

    vattrs = {}

    if len(cdf) == 0:
        logger.warning("No Zvariable found!")
        return vattrs

    for zvar in cdf:
        zattrs = cdf[zvar].attrs
        for vattr in zattrs:
            zattr = zAttr(cdf, vattr)
            vattrs[vattr] = zattr

    return vattrs
