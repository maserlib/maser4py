#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains unit tests of maser4py time module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
from datetime import datetime, timedelta

from numpy import datetime64, timedelta64

from .time import get_leapsec, local_to_utc, \
    tt2000_to_utc, utc_to_tt2000, tt2000_to_jd, \
    jd_to_tt2000

# ________________ HEADER _________________________

# Mandatory
# __version__ = ""
# __author__ = ""
# __date__ = ""

# # Optional
# __license__ = ""
# __credit__ = [""]
# __maintainer__ = ""
# __email__ = ""
# __project__ = ""
# __institute__ = ""
# __changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here gobal functions)

# Test time.py methods

def test_get_leapsec():
    """Test get_leapsec()."""
    date = datetime64("2011-03-01T07:00")
    leapsec = get_leapsec(date)
    assert leapsec == timedelta(seconds=34)


def test_get_leapsec64():
    """Test get_leapsec64().

    Same than test_get_leapsec(), but
    with leapsec returned as timedelta64
    """
    date = datetime64("2011-03-01T07:00")
    leapsec = get_leapsec(date, to_timedelta64=True)
    assert leapsec == timedelta64(34, 's')


def test_local_to_utc():
    """Test local_to_utc()."""
    utc = local_to_utc(datetime64("2011-03-01T07:00"), tzone="Europe/Paris")
    assert utc == datetime64("2011-03-01T06:00")


def test_utc_to_tt2000():
    """Test utc_to_tt2000()."""
    tt2000 = utc_to_tt2000(datetime(2011, 3, 1, 7, 0, 0))
    assert tt2000 == timedelta64(352234802000000000, 'ns')


def test_tt2000_to_utc():
    """Test tt2000_to_utc()."""
    tt2000 = timedelta64(352234802000000000, 'ns')
    utc = tt2000_to_utc(tt2000)
    assert utc == datetime64("2011-03-01T07:00")


def test_tt2000_to_jd():
    """Test tt2000_to_jd()."""
    tt2000 = timedelta64(352234802000000000, 'ns')
    jd = tt2000_to_jd(tt2000)
    assert jd == timedelta64(212165722800000000, 'us')


def test_mjd_to_tt2000():
    """Test mjd_to_tt2000()."""
    mjd = timedelta64(80094660, 'm')
    tt2000 = jd_to_tt2000(mjd, from_mjd=True)
    assert tt2000 == timedelta64(352234802000000, 'us')


# _________________ Main ____________________________
# if (__name__ == "__main__"):
# print ""
# main()
